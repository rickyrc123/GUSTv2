import React, { useEffect, useState } from 'react';

function VehicleList({ onSelectVehicle }) {
  const [vehicles, setVehicles] = useState([]);
  const [selectedVehicle, setSelectedVehicle] = useState(null);

  useEffect(() => {
    // Fetch vehicles from the API
    fetch('/vehicles')
      .then((response) => response.json())
      .then((data) => setVehicles(data))
      .catch((error) => console.error('Error fetching vehicles:', error));
  }, []);

  const handleSelectVehicle = (vehicle) => {
    setSelectedVehicle(vehicle);
    onSelectVehicle(vehicle.vehicleID); // Pass the selected vehicleID to the parent
  };

  return (
    <div>
      <h3>Select a Vehicle</h3>
      <ul>
        {vehicles.map((vehicle) => (
          <li
            key={vehicle.vehicleID}
            onClick={() => handleSelectVehicle(vehicle)}
            style={{
              cursor: 'pointer',
              fontWeight: selectedVehicle?.vehicleID === vehicle.vehicleID ? 'bold' : 'normal',
            }}
          >
            {vehicle.vehicleID} - {vehicle.name || 'Unnamed Vehicle'}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default VehicleList;