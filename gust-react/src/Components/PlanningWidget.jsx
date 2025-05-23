import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Polyline, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import VehicleList from './VehicleList';
import UploadPathButton from './UploadPathButton';
import ManeuverSelector from './ManeuverSelector';
import PathPointTable from './PathPointTable';
import './PlanningWidget.css';

const PlanningWidget = () => {
  const [paths, setPaths] = useState([
    [
      {lat: 51.505, lng: -0.09, alt: 100},
      {lat: 51.51, lng: -0.1, alt: 150}
    ]
  ]);
  console.log(paths);
  const [selectedVehicleID, setSelectedVehicleID] = useState(null);
  const [selectedManeuver, setSelectedManeuver] = useState(null);
  const [mapCenter] = useState([33.1823705, -87.5111005]);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [selectedPathIndex, setSelectedPathIndex] = useState(0);

  const getHue = (index, total) => (index * (360 / total)) % 360;
  const generateColor = (index, total, saturation=100, lightness=50) => `hsl(${getHue(index, total)}, ${saturation}%, ${lightness}%)`

  // Handle adding markers to the map
  const AddMarkerOnClick = () => {
    useMapEvents({
      click(e) {
        setPaths((currentPaths) => {
          const newPoint = {
            lat: e.latlng.lat,
            lng: e.latlng.lng,
            alt: 0
          }
          if (currentPaths.length === 0) return [[e.latlng]];
          const newPaths = [...currentPaths];
          const lastIndex = newPaths.length - 1;
          newPaths[lastIndex] = [...newPaths[lastIndex], newPoint];
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
    setPaths([[]]);
  };

  // Add new path
  const handleAddNewPath = () => {
    setPaths([...paths, []]);
    setSelectedPathIndex(paths.length - 1);
  };

  // Handle successful addition to maneuver
  const handleAddToManeuverSuccess = () => {
    setRefreshTrigger(prev => prev + 1);
  };


  console.log("Paths!");
  console.log(paths);
  console.log("---");
  return (
    <div className="planning-widget">
      <div className="control-panel">
        
        <ManeuverSelector
          selectedManeuver={selectedManeuver}
          onSelectManeuver={setSelectedManeuver}
          onAddToManeuver={handleAddToManeuverSuccess}
          selectedPathIndex={selectedPathIndex}
          vehicleID={selectedVehicleID}
          paths={paths}
          setPaths={setPaths}
          refreshTrigger={refreshTrigger}
          setRefreshTrigger={setRefreshTrigger}
        />
        <VehicleList onSelectVehicle={setSelectedVehicleID} selectedManeuver={selectedManeuver} />
        <div className="path-actions">
          <button onClick={handleAddNewPath} disabled={selectedVehicleID == null}>Start New Path</button>
          <button onClick={handleClearPaths}>Clear All Paths</button>
          {/* <UploadPathButton vehicleID={selectedVehicleID} paths={paths} /> */}
        </div>
      </div>

      <div className="map-container">
        <MapContainer center={mapCenter} zoom={13} style={{ height: '100%', width: '80%' }}>
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
              {path.length > 1 && <Polyline positions={path} pathOptions={{color: generateColor(pathIndex, paths.length), weight: 4}}/>}
            </React.Fragment>
          ))}
        </MapContainer>
      </div>
      <div className="path-data-section">
        <h3>Path Point Editor</h3>
        <PathPointTable paths={paths} setPaths={setPaths} selectedPathIndex={selectedPathIndex} setSelectedPathIndex={setSelectedPathIndex} />
      </div>
    </div>
  );
};

export default PlanningWidget;