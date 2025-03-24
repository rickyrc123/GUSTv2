import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";

  const MapComponent = () => {
    return (
      <MapContainer 
        center={[40.7128, -74.0060]} // New York City
        zoom={13} 
        style={{ height: "575px", width: "40%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />
      </MapContainer>
    );
  };

export default MapComponent;