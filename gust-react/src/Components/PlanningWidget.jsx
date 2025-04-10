import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Polyline, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import VehicleList from './VehicleList';
import UploadPathButton from './UploadPathButton';
import ManeuverSelector from './ManeuverSelector';
import './PlanningWidget.css';

const PlanningWidget = () => {
  const [paths, setPaths] = useState([]);
  const [selectedVehicleID, setSelectedVehicleID] = useState(null);
  const [selectedManeuver, setSelectedManeuver] = useState(null);
  const [mapCenter] = useState([51.505, -0.09]);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  // Handle adding markers to the map
  const AddMarkerOnClick = () => {
    useMapEvents({
      click(e) {
        setPaths((currentPaths) => {
          if (currentPaths.length === 0) return [[e.latlng]];
          const newPaths = [...currentPaths];
          const lastIndex = newPaths.length - 1;
          newPaths[lastIndex] = [...newPaths[lastIndex], e.latlng];
          return newPaths;
        });
      },
    });
    return null;
  };

  // Handle deleting markers
  const handleDeleteMarker = (pathIndex, markerIndex) => {
    setPaths((currentPaths) => {
      const newPaths = [...currentPaths];
      newPaths[pathIndex] = newPaths[pathIndex].filter((_, i) => i !== markerIndex);
      return newPaths;
    });
  };

  // Clear all paths
  const handleClearPaths = () => {
    setPaths([]);
  };

  // Add new path
  const handleAddNewPath = () => {
    setPaths([...paths, []]);
  };

  // Handle successful addition to maneuver
  const handleAddToManeuverSuccess = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="planning-widget">
      <div className="control-panel">
        <VehicleList onSelectVehicle={setSelectedVehicleID} />
        <ManeuverSelector
          selectedManeuver={selectedManeuver}
          onSelectManeuver={setSelectedManeuver}
          onAddToManeuver={handleAddToManeuverSuccess}
          vehicleID={selectedVehicleID}
          paths={paths}
          refreshTrigger={refreshTrigger}
        />
        
        <div className="path-actions">
          <button onClick={handleAddNewPath}>Start New Path</button>
          <button onClick={handleClearPaths}>Clear All Paths</button>
          <UploadPathButton vehicleID={selectedVehicleID} paths={paths} />
        </div>
      </div>

      <div className="map-container">
        <MapContainer center={mapCenter} zoom={13} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          <AddMarkerOnClick />
          
          {paths.map((path, pathIndex) => (
            <React.Fragment key={`path-${pathIndex}`}>
              {path.map((position, markerIndex) => (
                <Marker
                  key={`marker-${pathIndex}-${markerIndex}`}
                  position={position}
                  eventHandlers={{
                    contextmenu: () => handleDeleteMarker(pathIndex, markerIndex),
                  }}
                />
              ))}
              {path.length > 1 && <Polyline positions={path} />}
            </React.Fragment>
          ))}
        </MapContainer>
      </div>
    </div>
  );
};

export default PlanningWidget;