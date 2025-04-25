import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import PropTypes from "prop-types";
import L from "leaflet";
import droneIconPng from "./../assets/drone.png"

const MapComponent = ({drones = [], selectedDrone }) => {
 
	//Sets the center to the first returned pos or defaults to UA
	let center = [33.215, -87.538];

	// If selectedDrone is valid, center on that drone’s coordinates
	if (selectedDrone) {
		center = [selectedDrone.current_lat, selectedDrone.current_long];
	} else if (drones.length > 0) {
		center = [drones[0].current_lat, drones[0].current_long];
	}

	const droneIcon = L.icon({
		iconUrl: droneIconPng,
		iconSize: [40, 40],
		iconAnchor: [20, 20],
		popupAnchor: [0, -20]
	  });
  	//Returning the MapContainer with Open Street map cred and the positions mapped
  	return (
		<MapContainer key={`${center[0]}-${center[1]}`} center={center} zoom={13} style={{ height: "575px", width: "40%" }}>
		<TileLayer
			url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
			attribution="&copy; OpenStreetMap contributors"
		/>
		{drones.map((drone, index) => (
			<Marker key={index} position={[drone.current_lat, drone.current_long]} icon={droneIcon}>
			<Popup>
				<strong>{drone.name}</strong> <br />
				Lat: {drone.current_lat}, Lng: {drone.current_long}
			</Popup>
			</Marker>
		))}
		</MapContainer>
	);
};

MapComponent.propTypes = {
  	drones: PropTypes.arrayOf(
		PropTypes.shape({
			name: PropTypes.string,
			model: PropTypes.string,
			current_lat: PropTypes.number,
			current_long: PropTypes.number,
			current_alt: PropTypes.number,
			current_yaw: PropTypes.number
		})
  ),
  	selectedDrone: PropTypes.shape({
		name: PropTypes.string,
		model: PropTypes.string,
		current_lat: PropTypes.number,
		current_long: PropTypes.number,
		current_alt: PropTypes.number,
		current_yaw: PropTypes.number
	}),
};


export default MapComponent;