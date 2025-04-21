import React, { useState, useEffect } from 'react';

const ManeuverSelector = ({ 
  selectedManeuver, 
  onSelectManeuver, 
  onAddToManeuver,
  vehicleID,
  paths,
  refreshTrigger
}) => {
  const [maneuvers, setManeuvers] = useState([]);
  const [newManeuverName, setNewManeuverName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [maneuverDetails, setManeuverDetails] = useState(null);

  // Fetch maneuvers from API
  useEffect(() => {
    const fetchManeuvers = async () => {
      setIsLoading(true);
      try {
        const response = await fetch('/maneuvers');
        if (!response.ok) throw new Error('Failed to fetch maneuvers');
        const data = await response.json();
        setManeuvers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchManeuvers();
  }, [refreshTrigger]);

  // Fetch details for selected maneuver
  // useEffect(() => {
  //   if (selectedManeuver) {
  //     const fetchManeuverDetails = async () => {
  //       try {
  //         const response = await fetch(`/maneuvers/${selectedManeuver.maneuver_id}`);
  //         if (!response.ok) throw new Error('Failed to fetch maneuver details');
  //         const data = await response.json();
  //         setManeuverDetails(data);
  //       } catch (err) {
  //         setError(err.message);
  //       }
  //     };
      
  //     fetchManeuverDetails();
  //   }
  // }, [selectedManeuver]);

  // Create new maneuver
  const handleCreateManeuver = async () => {
    if (!newManeuverName.trim()) {
      setError('Maneuver name cannot be empty');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('/create_maneuver', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: newManeuverName }),
      });

      if (!response.ok) throw new Error('Failed to create maneuver');
      
      const newManeuver = await response.json();
      setManeuvers([...maneuvers, newManeuver]);
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
      setManeuverDetails(null);
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
    try {
      const response = await fetch('/new_maneuver_path', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          maneuver_id: selectedManeuver.maneuver_id,
          vehicleID,
          paths,
        }),
      });

      if (!response.ok) throw new Error('Failed to add path to maneuver');
      
      onAddToManeuver();
      setError(null);
    } catch (err) {
      setError(err.message);
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
          maneuver_id: selectedManeuver.maneuver_id,
          vehicleID: vehicleId
        }),
      });

      if (!response.ok) throw new Error('Failed to delete path from maneuver');
      
      // Refresh maneuver details
      const detailsResponse = await fetch(`/maneuvers/${selectedManeuver.maneuver_id}`);
      if (!detailsResponse.ok) throw new Error('Failed to fetch updated maneuver details');
      setManeuverDetails(await detailsResponse.json());
      
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
            {maneuvers.map(maneuver => (
              <li 
                key={maneuver.maneuver_id}
                className={selectedManeuver?.maneuver_id === maneuver.maneuver_id ? 'selected' : ''}
                onClick={() => onSelectManeuver(maneuver)}
              >
                {maneuver.name} (ID: {maneuver.maneuver_id})
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
          <h4>Maneuver Details: {selectedManeuver.name}</h4>
          
          <button 
            className="delete-maneuver"
            onClick={handleDeleteManeuver}
            disabled={isLoading}
          >
            Delete Maneuver
          </button>
          
          <h5>Associated Paths:</h5>
          {maneuverDetails?.paths?.length > 0 ? (
            <ul className="path-list">
              {maneuverDetails.paths.map((path, index) => (
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
        {isLoading ? 'Processing...' : vehicleID && maneuverDetails?.paths?.some(p => p.vehicleID === vehicleID) 
          ? 'Update Path in Maneuver' 
          : 'Add Path to Maneuver'}
      </button>
    </div>
  );
};

export default ManeuverSelector;