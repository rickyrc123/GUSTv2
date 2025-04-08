import React, { useState, useCallback } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { Tabs, Tab, Box } from '@mui/material';

// Add to PlanningWidget component
const PathPointTable = ({ paths, setPaths }) => {
  const [selectedTab, setSelectedTab] = useState(0);

  const columnDefs = [
    { 
      field: 'order',
      headerName: '#',
      width: 60,
      rowDrag: true,
      suppressMenu: true,
      filter: false,
      sortable: false
    },
    {
      field: 'lat',
      headerName: 'Latitude',
      editable: true,
      valueFormatter: params => params.value.toFixed(6),
      cellRenderer: params => params.value.toFixed(6),
      valueParser: params => parseFloat(params.newValue)
    },
    {
      field: 'lng',
      headerName: 'Longitude',
      editable: true,
      valueFormatter: params => params.value.toFixed(6),
      cellRenderer: params => params.value.toFixed(6),
      valueParser: params => parseFloat(params.newValue)
    },
    {
      field: 'alt',
      headerName: 'Altitude',
      editable: true,
      valueParser: params => parseFloat(params.newValue)
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

  const onRowDragEnd = (e) => {
    const newPath = [...paths[selectedTab]];
    const movedRow = newPath.splice(e.oldIndex, 1)[0];
    newPath.splice(e.newIndex, 0, movedRow);
    
    const newPaths = [...paths];
    newPaths[selectedTab] = newPath.map((p, i) => ({ ...p, order: i + 1 }));
    setPaths(newPaths);
  };

  const onCellValueChanged = (e) => {
    const newPaths = [...paths];
    newPaths[selectedTab][e.rowIndex] = {
      ...newPaths[selectedTab][e.rowIndex],
      [e.colDef.field]: e.newValue
    };
    setPaths(newPaths);
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

      <Box sx={{ height: 300 }} className="ag-theme-alpine">
        <AgGridReact
          columnDefs={columnDefs}
          rowData={paths[selectedTab]?.map((p, i) => ({ ...p, order: i + 1 })) || []}
          onRowDragEnd={onRowDragEnd}
          onCellValueChanged={onCellValueChanged}
          rowDragManaged={true}
          animateRows={true}
          suppressMoveWhenRowDragging={true}
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