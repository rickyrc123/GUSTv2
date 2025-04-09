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

  const columnDefs = [
    { 
      headerName: '↕',
      width: 60,
      cellRenderer: (params) => (
        <div 
          draggable
          onDragStart={(e) => {
            e.dataTransfer.effectAllowed = 'move';
            setDraggedRowIndex(params.rowIndex);
          }}
          onDragOver={(e) => e.preventDefault()}
          style={{ cursor: 'move', padding: '5px' }}
        >
          ⋮⋮
        </div>
      ),
      suppressMenu: true,
      filter: false,
      sortable: false
    },
    {
      field: 'lat',
      headerName: 'Latitude',
      editable: true,
      valueFormatter: params => params.value.toFixed(6),
      valueParser: params => {
        const value = parseFloat(params.newValue);
        return isNaN(value) ? params.oldValue : value;
      }
    },
    {
      field: 'lng',
      headerName: 'Longitude',
      editable: true,
      valueFormatter: params => params.value.toFixed(6),
      valueParser: params => {
        const value = parseFloat(params.newValue);
        return isNaN(value) ? params.oldValue : value;
      }
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

  const handleDeletePoint = (rowIndex) => {
    const newPaths = [...paths];
    newPaths[selectedTab] = newPaths[selectedTab].filter((_, i) => i !== rowIndex);
    setPaths(newPaths);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    const rect = e.currentTarget.getBoundingClientRect();
    const hoveredRowIndex = Math.floor((e.clientY - rect.top) / 28);

    if (draggedRowIndex !== null && hoveredRowIndex !== draggedRowIndex)    {
        const newPath = [...paths[selectedTab]];
        const [removed] = newPath.splice(draggedRowIndex, 1);
        newPath.splice(hoveredRowIndex, 0, removed);
        const newPaths = [...paths];
        newPaths[selectedTab] = newPath;
        setPaths(newPaths);
        setDraggedRowIndex(hoveredRowIndex);
    }
  }

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

      <Box 
        sx={{ height: 300 }} 
        className="ag-theme-alpine"
        onDragOver={handleDragOver}
        onDragEnd={() => setDraggedRowIndex(null)}
      >
        <AgGridReact
          modules={[ClientSideRowModelModule]}
          columnDefs={columnDefs}
          rowData={paths[selectedTab] || []}
          onCellValueChanged={onCellValueChanged}
          suppressDragLeaveHidesColumns={true}
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