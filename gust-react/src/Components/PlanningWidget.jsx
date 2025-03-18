import React, { useState } from 'react';
import {
  MapContainer,
  TileLayer,
  Marker,
  Polyline,
  useMapEvents
} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function PlanningWidget() {
  // Example initial data: two paths with a couple of points each.
  // Each path is just an array of { lat, lng } objects.
  const [paths, setPaths] = useState([
    [
      { lat: 51.505, lng: -0.09 },
      { lat: 51.51, lng: -0.1 }
    ],
    [
      { lat: 51.49, lng: -0.07 },
      { lat: 51.52, lng: -0.08 }
    ]
  ]);

  // This component listens for clicks on the map and
  // adds a new marker to the last path in `paths`.
  function AddMarkerOnClick() {
    useMapEvents({
      click(e) {
        setPaths((currentPaths) => {
          // If no paths exist yet, create the first path
          if (currentPaths.length === 0) {
            return [[e.latlng]];
          }
          // Otherwise, add to the last path
          const newPaths = [...currentPaths];
          const lastIndex = newPaths.length - 1;
          newPaths[lastIndex] = [...newPaths[lastIndex], e.latlng];
          return newPaths;
        });
      },
    });
    return null;
  }

  // Delete a marker from a specific path by its index
  const handleDeleteMarker = (pathIndex, markerIndex) => {
    setPaths((currentPaths) => {
      const newPaths = [...currentPaths];
      // Remove just that one coordinate
      newPaths[pathIndex] = newPaths[pathIndex].filter(
        (_, i) => i !== markerIndex
      );
      return newPaths;
    });
  };

  return (
    <div style={{ width: '100%', height: '400px' }}>
      <MapContainer
        center={[51.505, -0.09]}
        zoom={13}
        style={{ width: '100%', height: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        
        {/* Hook to add markers on map click */}
        <AddMarkerOnClick />

        {/* For each path, render its markers & connecting polyline */}
        {paths.map((path, pathIndex) => (
          <React.Fragment key={pathIndex}>
            {/* One Marker per coordinate, with a right-click (contextmenu) to delete */}
            {path.map((position, markerIndex) => (
              <Marker
                key={markerIndex}
                position={position}
                eventHandlers={{
                  contextmenu: () => handleDeleteMarker(pathIndex, markerIndex),
                }}
              />
            ))}
            
            {/* Draw a line if there's more than one coordinate in the path */}
            {path.length > 1 && <Polyline positions={path} />}
          </React.Fragment>
        ))}
      </MapContainer>
    </div>
  );
}

export default PlanningWidget;
