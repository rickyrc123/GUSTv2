import React, { useState, useEffect } from 'react';

const ManeuverSelector = ({ 
  selectedManeuver, 
  onSelectManeuver, 
  onAddToManeuver,
  selectedPathIndex,
  vehicleID,
  paths,
  refreshTrigger
}) => {
  const [maneuvers, setManeuvers] = useState([]);
  const [newManeuverName, setNewManeuverName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [maneuverDetailsNames, setManeuverDetailsNames] = useState(null);
  const [maneuverDetailsPaths, setManeuverDetailsPaths] = useState(null);

  // Fetch maneuvers from API
  useEffect(() => {
    const fetchManeuvers = async () => {
      setIsLoading(true);
      try {
        const response = await fetch('http://localhost:8000/maneuvers');
        if (!response.ok) throw new Error('Failed to fetch maneuvers');
        console.log("got them mans");
        console.log(maneuvers);
        const data = await response.json();
        console.log(data);
        setManeuvers(Array.from(data['maneuvers']));
        console.log("mans are in ");
        console.log(maneuvers);
        console.log("-----");
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchManeuvers();
  }, [refreshTrigger]);

  //Fetch details for selected maneuver
  useEffect(() => {
    if (selectedManeuver) {
      const fetchManeuverDetails = async () => {
        console.log('Selected Man');
        console.log(selectedManeuver);
        console.log('-----');
        try {
          const response = await fetch(`http://localhost:8000/programs/manuevers/get_drones_in_maneuver?maneuver_name=${selectedManeuver}`,
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
            }
          );
          console.log('fetch worked');
          if (!response.ok) throw new Error('Failed to fetch maneuver details');
          const data = await response.json();
          console.log(data);
          setManeuverDetailsNames(Array.from(data['Drones']));
          console.log('after assign');

          const fetchDronePath = async (droneName) => {
            const resp = await fetch(`http://localhost:8000/programs/get_path_by_drone?drone_name=${droneName}`,
              {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                
              }
            )
            const path = await resp.json();
            if (!resp.ok) throw new Error(`Failed to get path for ${droneName}`);
            return path;
          }
          console.log('before eval');

          if (maneuverDetailsNames?.length > 0 && maneuverDetailsNames !== null) {
            paths = [];
            for (const drone_name of maneuverDetailsNames) {
              const d_path = await fetchDronePath(drone_name);
              paths = [...paths, d_path];
            }
            setManeuverDetailsPaths(paths);
          }
          else {
            console.log('no drone so no path');
            setManeuverDetailsPaths([]);
          }

        } catch (err) {
          console.log(err.message);
          setError(err.message);
        }
      };
      
      fetchManeuverDetails();
    }
  }, [selectedManeuver]);

  // Create new maneuver
  const handleCreateManeuver = async () => {
    if (!newManeuverName.trim()) {
      setError('Maneuver name cannot be empty');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/maneuvers/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: newManeuverName, drones: [] }),
      });

      if (!response.ok) throw new Error('Failed to create maneuver');
      
      const newManeuver = await response.json();
      setManeuvers([...maneuvers, newManeuverName]);
      setNewManeuverName('');
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Delete maneuver
  const handleDeleteManeuver = async () => {
    if (!selectedManeuver) {
      setError('Please select a maneuver first');
      return;
    }

    if (!window.confirm(`Are you sure you want to delete "${selectedManeuver.name}"?`)) {
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch(`/delete_maneuver`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          maneuver_id: selectedManeuver.maneuver_id
        }),
      });

      if (!response.ok) throw new Error('Failed to delete maneuver');
      
      setManeuvers(maneuvers.filter(m => m.maneuver_id !== selectedManeuver.maneuver_id));
      setSelectedManeuver(null);
      setManeuverDetailsNames(null);
      setManeuverDetailsPaths(null);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Add/update path in maneuver
  const handleAddToManeuver = async () => {
    if (!selectedManeuver) {
      setError('Please select a maneuver first');
      return;
    }
    if (!vehicleID) {
      setError('Please select a vehicle first');
      return;
    }
    if (paths.length === 0) {
      setError('Please draw a path first');
      return;
    }

    setIsLoading(true);
    console.log(selectedPathIndex);
    console.log('abt to send');
    console.log(paths[selectedPathIndex]);
    let payload = [];
    for (const point of paths[selectedPathIndex]) {
      payload = [...payload, {"long": point['lng'], "lat": point['lat'], "alt": point['alt']}]
    }
    try {
      const response = await fetch(`http://localhost:8000/maneuvers/assign_to_drone?maneuver_name=${selectedManeuver}&drone_name=${vehicleID}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: paths.length > 0 ? JSON.stringify(payload) : JSON.stringify([{ lat: 0.0, long: 0.0, alt: 0.0 }])
        
      });

      if (!response.ok) throw new Error('Failed to add path to maneuver');
      console.log('looks like it worked?');
      onAddToManeuver();
      setError(null);
    } catch (err) {
      setError(err.message);
      console.log(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Delete path from maneuver
  const handleDeletePathFromManeuver = async (vehicleId) => {
    if (!selectedManeuver) {
      setError('Please select a maneuver first');
      return;
    }

    if (!window.confirm('Are you sure you want to delete this path?')) {
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('/delete_maneuver_path', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          maneuver_id: selectedManeuver,
          vehicleID: vehicleId
        }),
      });

      if (!response.ok) throw new Error('Failed to delete path from maneuver');
      
      // Refresh maneuver details
      // const detailsResponse = await fetch(`/maneuvers/${selectedManeuver}`);
      // if (!detailsResponse.ok) throw new Error('Failed to fetch updated maneuver details');
      // setManeuverDetails(await detailsResponse.json());
      
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="maneuver-selector">
      <h3>Maneuver Management</h3>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="maneuver-list">
        <h4>Available Maneuvers</h4>
        {isLoading ? (
          <p>Loading maneuvers...</p>
        ) : (
          <ul>
            {Array.isArray(maneuvers) && maneuvers?.map(manny => (
              <li 
                key={manny}
                className={selectedManeuver === manny ? 'selected' : ''}
                onClick={() => onSelectManeuver(manny)}
              >
                {manny}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="create-maneuver">
        <h4>Create New Maneuver</h4>
        <input
          type="text"
          value={newManeuverName}
          onChange={(e) => setNewManeuverName(e.target.value)}
          placeholder="Enter maneuver name"
          disabled={isLoading}
        />
        <button 
          onClick={handleCreateManeuver}
          disabled={isLoading || !newManeuverName.trim()}
        >
          {isLoading ? 'Creating...' : 'Create Maneuver'}
        </button>
      </div>

      {selectedManeuver && (
        <div className="maneuver-details">
          <h4>Maneuver Details: {selectedManeuver}</h4>
          
          <button 
            className="delete-maneuver"
            onClick={handleDeleteManeuver}
            disabled={isLoading}
          >
            Delete Maneuver
          </button>
          
          <h5>Associated Paths:</h5>
          {maneuverDetailsPaths?.length > 0 ? (
            <ul className="path-list">
              {maneuverDetailsPaths.map((path, index) => (
                <li key={index}>
                  <div>
                    <strong>Vehicle ID:</strong> {path.vehicleID}
                  </div>
                  <div>
                    <strong>Points:</strong> {path.points.length}
                  </div>
                  <button
                    onClick={() => handleDeletePathFromManeuver(path.vehicleID)}
                    disabled={isLoading}
                  >
                    Delete Path
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <p>No paths associated with this maneuver</p>
          )}
        </div>
      )}

      <button 
        className="add-to-maneuver"
        onClick={handleAddToManeuver}
        disabled={isLoading || !selectedManeuver || !vehicleID || paths.length === 0}
      >
        {isLoading ? 'Processing...' : vehicleID && maneuverDetailsPaths?.some(p => p.vehicleID === vehicleID) 
          ? 'Update Path in Maneuver' 
          : 'Add Path to Maneuver'}
      </button>
    </div>
  );
};

export default ManeuverSelector;