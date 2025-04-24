import React, {useState} from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ClientSideRowModelModule } from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { Tabs, Tab, Box } from '@mui/material';

const PathPointTable = ({ paths, setPaths, selectedPathIndex, setSelectedPathIndex }) => {
  const [selectedTab, setSelectedTab] = [selectedPathIndex, setSelectedPathIndex];
  const [modules] = React.useState([ClientSideRowModelModule]);

  // Column definitions with editing and delete button
  const columnDefs = [
    {
      headerName: '#',
      valueGetter: 'node.rowIndex + 1',
      width: 60,
      sortable: false,
      filter: false
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
      }
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

  return (
    <div className="path-point-editor">
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

      <Box sx={{ height: 400 }} className="ag-theme-alpine">
        <AgGridReact
          modules={modules}
          columnDefs={columnDefs}
          rowData={paths[selectedTab] || []}
          onCellValueChanged={onCellValueChanged}
          singleClickEdit={true}
          stopEditingWhenCellsLoseFocus={true}
          key={`grid-${selectedTab}-${paths[selectedTab]?.length}`} // Force re-render on tab change
          defaultColDef={{
            resizable: true,
            sortable: true,
            filter: true,
            flex: 1,
          }}
        />
      </Box>
    </div>
  );
};

export default PathPointTable;