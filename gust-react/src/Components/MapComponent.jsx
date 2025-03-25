import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const MapComponent = () => {
  const [positions, setPositions] = useState([
    { "latitude": 51.505, "longitude": -0.09, "name": "Location 1" },
    { "latitude": 51.51, "longitude": -0.1, "name": "Location 2" },
    { "latitude": 0.51, "longitude": -0.1, "name": "Location 2" }
  ]);

  // useEffect(() => {
  //   // Fetch data from your API
  //   const fetchData = async () => {
  //     try {
  //       const response = await fetch('https://your-api-endpoint.com/positions');
  //       const data = await response.json();
  //       setPositions(data); // Assuming the API returns an array of positions
  //     } catch (error) {
  //       console.error('Error fetching data:', error);
  //     }
  //   };

  //   fetchData();
  // }, []);
  
  //Sets the center to the first returned pos or defaults to UA
  const center = positions.length > 0 ? [positions[0].latitude, positions[0].longitude] : [33.215, -87.538];

  //Returning the MapContainer with Open Street map cred and the positions mapped
  return (
    <MapContainer center={center} zoom={13} style={{ height: "575px", width: "45%" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      {positions.map((position, index) => (
        <Marker key={index} position={[position.latitude, position.longitude]}>
          <Popup>
            <strong>{position.name}</strong> <br />
            Lat: {position.latitude}, Lng: {position.longitude}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default MapComponent;