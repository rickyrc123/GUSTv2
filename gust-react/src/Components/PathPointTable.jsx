import React, { useState, useCallback } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ClientSideRowModelModule } from 'ag-grid-community';
import { ModuleRegistry } from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { Tabs, Tab, Box } from '@mui/material';

ModuleRegistry.registerModules([ClientSideRowModelModule]);



// Add to PlanningWidget component
const PathPointTable = ({ paths, setPaths }) => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [draggedRowIndex, setDraggedRowIndex] = useState(null);

  const safePaths = paths.length === 0 ? [[]] : paths.map(path => 
    path.map(p => ({
      lat: p?.lat || 0,
      lng: p?.lng || 0,
      alt: p?.alt || 0
    }))
  );

  const columnDefs = [

    {
      field: 'lat',
      headerName: 'Latitude',
      editable: true,
      valueFormatter: params => params.value?.toFixed(6) || '0.000000',
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
      valueFormatter: params => params.value?.toFixed(6) || '0.000000',
      valueParser: params => {
        const value = parseFloat(params.newValue);
        return isNaN(value) ? params.oldValue : value;
      },
      cellRenderer: params => params.value?.toFixed(6) || '0.000000'
    },
    {
      field: 'alt',
      headerName: 'Altitude',
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
          onClick={() => handleDeletePoint(params.rowIndex)}
          className="delete-point-button"
        >
          Delete
        </button>
      ),
      suppressMenu: true,
      sortable: false,
      filter: false
    }
  ];

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


  const handleDeletePoint = (rowIndex) => {
    setPaths(prev => {
      const newPaths = [...prev];
      if (newPaths[selectedTab]?.[rowIndex]) {
        newPaths[selectedTab] = newPaths[selectedTab].filter((_, i) => i !== rowIndex);
      }
      return newPaths;
    });
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    const rect = e.currentTarget.getBoundingClientRect();
    const hoveredRowIndex = Math.floor((e.clientY - rect.top) / 28);
    
    if (draggedRowIndex !== null && 
        hoveredRowIndex !== draggedRowIndex &&
        safePaths[selectedTab]?.[draggedRowIndex] &&
        hoveredRowIndex >= 0 && 
        hoveredRowIndex < safePaths[selectedTab].length) {
      const newPath = [...safePaths[selectedTab]];
      const [removed] = newPath.splice(draggedRowIndex, 1);
      newPath.splice(hoveredRowIndex, 0, removed);
      
      const newPaths = [...safePaths];
      newPaths[selectedTab] = newPath;
      setPaths(newPaths);
      setDraggedRowIndex(hoveredRowIndex);
    }
  };

  const onCellValueChanged = (e) => {
    const newPaths = [...paths];
    newPaths[selectedTab][e.rowIndex] = {
      ...newPaths[selectedTab][e.rowIndex],
      [e.colDef.field]: e.newValue
    };
    setPaths(newPaths);
  };

  console.log(paths[selectedTab]?.map((p, i) => ({ ...p, order: i + 1 })) || [])

  return (
    <div className="path-point-editor">
      <div className="table-controls">
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
          className='export-csv-button'
          onClick={handleExportCSV}
          disabled={!paths[selectedTab].length}
        >
          Export to CSV
        </button>
      </div>

      <Box 
        sx={{ height: 300 }} 
        className="ag-theme-alpine"
        onDragOver={handleDragOver}
        onDragEnd={() => setDraggedRowIndex(null)}
      >
        <AgGridReact
          key={`${selectedTab}-${safePaths[selectedTab]?.length}`}
          columnDefs={columnDefs}
          rowData={safePaths[selectedTab] || []}
          onCellValueChanged={onCellValueChanged}
          getRowId={params => params.data.lat + '-' + params.data.lng}
          defaultColDef={{
            sortable: true,
            filter: true,
            resizable: true,
            flex: 1,
          }}
        />
      </Box>
    </div>
  );
};

export default PathPointTable;