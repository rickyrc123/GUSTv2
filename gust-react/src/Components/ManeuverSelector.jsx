import React, { useState, useEffect } from 'react';

const ManeuverSelector = ({ 
  selectedManeuver, 
  onSelectManeuver, 
  onAddToManeuver,
  selectedPathIndex,
  vehicleID,
  paths,
  setPaths,
  refreshTrigger,
  setRefreshTrigger
}) => {
  const [maneuvers, setManeuvers] = useState([]);
  const [newManeuverName, setNewManeuverName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [maneuverDetailsNames, setManeuverDetailsNames] = useState([]);
  const [maneuverDetailsPaths, setManeuverDetailsPaths] = useState([]);
  const [selectedPath, setSelectedPath] = useState(null);

  const convertPathFormat = (path) => {
    return path.map(point => {
      if(Array.isArray(point)) {
        return {
          lat: point[1],
          lng: point[0],
          alt: point[2] || 0,
        }
      }
      return {
        lat: point.lat,
        lng: point.long,
        alt: point.alt || 0,
      }
    });
  }

  // Fetch maneuvers from API
  useEffect(() => {
    const fetchManeuvers = async () => {
      setIsLoading(true);
      try {
        const response = await fetch('http://localhost:8000/maneuvers');
        if (!response.ok) throw new Error('Failed to fetch maneuvers');
        // console.log("got them mans");
        // console.log(maneuvers);
        const data = await response.json();
        // console.log(data);
        setManeuvers(Array.from(data['maneuvers']));
        // console.log("mans are in ");
        // console.log(maneuvers);
        // console.log("-----");
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
    let isMounted = true; // Track component mount status
    const controller = new AbortController(); // For aborting fetch
  
    const fetchManeuverDetails = async () => {
      try {
        if (!selectedManeuver || !isMounted) return;

        setPaths([]);
  
        // 1. Fetch drones in maneuver
        const dronesResponse = await fetch(
          `http://localhost:8000/programs/manuevers/get_drones_in_maneuver?maneuver_name=${selectedManeuver}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            signal: controller.signal
          }
        );
  
        if (!dronesResponse.ok) throw new Error('Failed to fetch drones');
        const dronesData = await dronesResponse.json();
        
        // Update drone names immediately
        const newDroneNames = Array.from(dronesData.Drones);
        setManeuverDetailsNames(newDroneNames);
        console.log('before state');
        console.log(newDroneNames);
        console.log('-----');
  
        // 2. Fetch paths for each drone
        if (newDroneNames.length > 0) {
          const pathsPromises = newDroneNames.map(async (droneName) => {
            const pathResponse = await fetch(
              `http://localhost:8000/programs/get_path_by_drone?drone_name=${droneName}`,
              {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                signal: controller.signal
              }
            );
            if (!pathResponse.ok) throw new Error(`Failed to fetch path for ${droneName}`);
            return pathResponse.json();
          });
  
          const pathsResults = await Promise.all(pathsPromises);
          const formattedPaths = pathsResults.map(result => 
            convertPathFormat(Array.from(result.Path?.path || []))
          );
  
          if (isMounted) {
            setPaths(formattedPaths)
            //setManeuverDetailsNames(newDroneNames);
            
            setManeuverDetailsPaths(formattedPaths);
            console.log('mounted and set');
            console.log(maneuverDetailsPaths);
            console.log('-----');
          }
        } else {
          if (isMounted) {
            setPaths([]);
            //setManeuverDetailsNames([]);
            setManeuverDetailsPaths([]);
          }
        }
      } catch (err) {
        if (err.name !== 'AbortError' && isMounted) {
          console.error('Fetch error:', err);
          setError(err.message);
        }
      }
    };
  
    // Initial fetch
    fetchManeuverDetails();
    console.log('drone names');
    console.log(maneuverDetailsNames);
    console.log('-----');
    // Cleanup function
    return () => {
      isMounted = false;
      controller.abort();
    };
    
  }, [selectedManeuver, refreshTrigger]);

  


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

    if (!window.confirm(`Are you sure you want to delete "${selectedManeuver}"?`)) {
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/maneuvers/delete?name=${selectedManeuver}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        
      });

      if (!response.ok) throw new Error('Failed to delete maneuver');
      
      setManeuvers(maneuvers.filter(m => m !== selectedManeuver));
      onSelectManeuver(null);
      setManeuverDetailsNames(null);
      setManeuverDetailsPaths(null);
      setError(null);
      setRefreshTrigger(prev => prev + 1);
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
  const handleDeletePathFromManeuver = async (index) => {
    console.log('indel');
    console.log(maneuverDetailsNames);
    console.log(index);
    console.log(maneuverDetailsNames[index]);
    console.log('-------');
    if (!selectedManeuver) {
      setError('Please select a maneuver first');
      return;
    }

    if (!window.confirm('Are you sure you want to delete this path?')) {
      return;
    }

    setIsLoading(true);
    let droneName = maneuverDetailsNames[index];
    try {
      const response = await fetch(`http://localhost:8000/programs/manuevers/remove_drone_from_maneuver?drone_name=${droneName}&maneuver_name=${selectedManeuver}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) throw new Error('Failed to delete path from maneuver');
      
      // Refresh maneuver details
      // const detailsResponse = await fetch(`/maneuvers/${selectedManeuver}`);
      // if (!detailsResponse.ok) throw new Error('Failed to fetch updated maneuver details');
      // setManeuverDetails(await detailsResponse.json());
      setRefreshTrigger(prev => prev + 1);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePathOnClick = (index) => {
    //setSelectedPathIndex(index);
    console.log('bump');
  };
  console.log(maneuverDetailsNames);
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
          {maneuverDetailsNames?.length > 0 ? (
            <ul className="path-list">
              {maneuverDetailsPaths.map((path, index) => (
                <li key={index}
                  onClick={handlePathOnClick(index)}
                >
                  <div>
                    <strong>Vehicle ID:</strong> {maneuverDetailsNames[index]}
                  </div>
                  <div>
                    <strong>Points:</strong> {maneuverDetailsPaths[index].length}
                  </div>
                  <button
                    onClick={() => handleDeletePathFromManeuver(index)}
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