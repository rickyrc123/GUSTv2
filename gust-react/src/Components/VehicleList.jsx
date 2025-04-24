import React, { useState, useEffect } from 'react';

const VehicleList = ({ onSelectVehicle }) => {
  const [vehicles, setVehicles] = useState([]);
  const [selectedVehicle, setSelectedVehicle] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchVehicles = async () => {
      setIsLoading(true);
      try {
        const response = await fetch('http://localhost:8000/drones');
        if (!response.ok) throw new Error('Failed to fetch vehicles');
        const data = await response.json();
        setVehicles(data.Drones);
        console.log(data);
        console.log('got them drones!');
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchVehicles();
  }, []);

  const handleSelectVehicle = (vehicle) => {
    setSelectedVehicle(vehicle);
    onSelectVehicle(vehicle.name);
  };

  return (
    <div className="vehicle-list">
      <h3>Vehicle Selection</h3>
      
      {error && <div className="error-message">{error}</div>}
      
      {isLoading ? (
        <p>Loading vehicles...</p>
      ) : (
        <ul>
          {vehicles.map(vehicle => (
            <li
              key={vehicle.name}
              className={selectedVehicle?.name === vehicle.name ? 'selected' : ''}
              onClick={() => handleSelectVehicle(vehicle)}
            >
              {vehicle.name} (ID: {vehicle.name})
              {vehicle.model && <span> - {vehicle.model}</span>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default VehicleList;