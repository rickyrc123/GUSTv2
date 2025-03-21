import React, { useState } from 'react';
import {
  MapContainer,
  TileLayer,
  Marker,
  Polyline,
  useMapEvents,
} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import VehicleList from './VehicleList';
import UploadPathButton from './UploadPathButton';

function PlanningWidget() {
  const [paths, setPaths] = useState([
    [
      { lat: 51.505, lng: -0.09 },
      { lat: 51.51, lng: -0.1 },
    ],
    [
      { lat: 51.49, lng: -0.07 },
      { lat: 51.52, lng: -0.08 },
    ],
  ]);
  const [selectedVehicleID, setSelectedVehicleID] = useState(null);

  function AddMarkerOnClick() {
    useMapEvents({
      click(e) {
        setPaths((currentPaths) => {
          if (currentPaths.length === 0) {
            return [[e.latlng]];
          }
          const newPaths = [...currentPaths];
          const lastIndex = newPaths.length - 1;
          newPaths[lastIndex] = [...newPaths[lastIndex], e.latlng];
          return newPaths;
        });
      },
    });
    return null;
  }

  const handleDeleteMarker = (pathIndex, markerIndex) => {
    setPaths((currentPaths) => {
      const newPaths = [...currentPaths];
      newPaths[pathIndex] = newPaths[pathIndex].filter(
        (_, i) => i !== markerIndex
      );
      return newPaths;
    });
  };

  return (
    <div style={{ width: '100%', height: '400px' }}>
      <VehicleList onSelectVehicle={setSelectedVehicleID} />
      <MapContainer
        center={[51.505, -0.09]}
        zoom={13}
        style={{ width: '100%', height: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        <AddMarkerOnClick />
        {paths.map((path, pathIndex) => (
          <React.Fragment key={pathIndex}>
            {path.map((position, markerIndex) => (
              <Marker
                key={markerIndex}
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
      <UploadPathButton vehicleID={selectedVehicleID} paths={paths} />
    </div>
  );
}

export default PlanningWidget;