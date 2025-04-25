import React, {useState} from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ClientSideRowModelModule } from 'ag-grid-community';
import { ModuleRegistry } from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { Tabs, Tab, Box } from '@mui/material';

ModuleRegistry.registerModules([ClientSideRowModelModule]);

const PathPointTable = ({ paths, setPaths, selectedPathIndex, setSelectedPathIndex }) => {
  const [selectedTab, setSelectedTab] = [selectedPathIndex, setSelectedPathIndex];
  const [modules] = React.useState([ClientSideRowModelModule]);

  const getRowId = (params) => {
    // Use AG Grid's built-in node ID as fallback
    return params.data?.lat && params.data?.lng && params.data?.alt 
      ? `${params.data.lat}-${params.data.lng}-${params.data.alt}-${params.node.rowIndex}`
      : params.node.id;
  };

  // Column definitions with editing and delete button
  const columnDefs = [
    {
      headerName: '#',
      valueGetter: 'node.rowIndex + 1',
      width: 60,
      sortable: false,
      filter: false,
      supressMovable: true
    },
    {
      field: 'lat',
      headerName: 'Latitude',
      editable: true,
      cellEditor: 'agTextCellEditor',
      valueFormatter: params => params.value?.toFixed(6) || '',
      valueParser: params => {
        const value = parseFloat(params.newValue);
        return isNaN(value) ? params.oldValue : value;
      },
      cellRenderer: params => params.value?.toFixed(6) || '0.000000'
    },
    {
      field: 'lng',
      headerName: 'Longitude',
      editable: true,
      valueFormatter: params => params.value?.toFixed(6) || '',
      valueParser: params => {
        const value = parseFloat(params.newValue);
        return isNaN(value) ? params.oldValue : value;
      }
    },
    {
      field: 'alt',
      headerName: 'Altitude (m)',
      editable: true,
      valueParser: params => {
        const value = parseFloat(params.newValue);
        return isNaN(value) ? params.oldValue : value;
      }
    },
    {
      headerName: 'Actions',
      cellRenderer: params => (
        <button 
          className="delete-point-button"
          onClick={() => handleDeletePoint(params.node.rowIndex)}
        >
          Delete
        </button>
      ),
      sortable: false,
      filter: false,
      width: 100
    }
  ];

  // Handle point deletion
  const handleDeletePoint = (rowIndex) => {
    console.log(rowIndex);
    setPaths(prevPaths => {
      const newPaths = [...prevPaths];
      if (newPaths[selectedTab] && newPaths[selectedTab][rowIndex]) {
        newPaths[selectedTab] = newPaths[selectedTab].filter((_, i) => i !== rowIndex);
      }
      return newPaths;
    });
  };

  // Handle cell value changes
  const onCellValueChanged = (params) => {
    setPaths(prevPaths => {
      const newPaths = [...prevPaths];
      if (newPaths[selectedTab] && newPaths[selectedTab][params.rowIndex]) {
        newPaths[selectedTab][params.rowIndex] = {
          ...newPaths[selectedTab][params.rowIndex],
          [params.colDef.field]: params.newValue
        };
      }
      return newPaths;
    });
  };

  const handleExportCSV = () => {
    const currentPath = paths[selectedTab];
    if (!currentPath || currentPath.length === 0) return;
  
    // Create CSV content
    const csvHeader = 'Latitude,Longitude,Altitude\n';
    const csvRows = currentPath.map(point => 
      `${point.lat},${point.lng},${point.alt}`
    ).join('\n');
    
    const csvString = csvHeader + csvRows;
  
    // Create download link
    const blob = new Blob([csvString], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `path_${selectedTab + 1}_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="path-point-editor">
      <div className='table-controls'>
        <Tabs
          value={selectedTab}
          onChange={(e, newValue) => setSelectedTab(newValue)}
          variant="scrollable"
          scrollButtons="auto"
        >
          {paths.map((_, index) => (
            <Tab 
              key={index}
              label={`Path ${index + 1}`}
              sx={{ minWidth: 100 }}
            />
          ))}
        </Tabs>
        <button 
          className="export-csv-button"
          onClick={handleExportCSV}
          disabled={!paths[selectedTab]?.length}
        >
          Export to CSV
        </button>
      </div>
      <Box sx={{ height: 400 }} className="ag-theme-alpine">
        <AgGridReact
          modules={modules}
          columnDefs={columnDefs}
          rowData={paths[selectedTab] || []}
          onCellValueChanged={onCellValueChanged}
          singleClickEdit={true}
          supressClickEdit={false}
          stopEditingWhenCellsLoseFocus={true}
          key={`grid-${selectedTab}-${paths[selectedTab]?.length}`} // Force re-render on tab change
          defaultColDef={{
            resizable: true,
            sortable: true,
            filter: true,
            flex: 1,
            editable: true,
          }}
        />
      </Box>
    </div>
  );
};

export default PathPointTable;