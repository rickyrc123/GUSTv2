import React, { useState, useEffect } from 'react';
import {
  List,
  ListItem,
  ListItemText,
  Button,
  TextField,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import "./ConnectionScreen.css"

const ConnectionScreen = () => {
  const [connections, setConnections] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [manualConnection, setManualConnection] = useState('');
  const [advancedOpen, setAdvancedOpen] = useState(false);
  const [portRange, setPortRange] = useState({
    start: 14550,
    end: 14560
  });

  // Fetch available connections
  const fetchConnections = async () => {
    setLoading(true);
    try {
      const response = await fetch('/available_connections');
      if (!response.ok) throw new Error('Failed to fetch connections');
      const data = await response.json();
      setConnections(data);
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    fetchConnections();
  }, []);

  // Handle connection attempt
  const handleConnect = async (droneId) => {
    try {
      const response = await fetch('/connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ drone_id: droneId })
      });
      
      if (!response.ok) throw new Error('Connection failed');
      alert(`Successfully connected to ${droneId}`);
    } catch (err) {
      setError(err.message);
    }
  };

  // Handle manual connection
  const handleManualConnect = () => {
    if (manualConnection.trim()) {
      handleConnect(manualConnection.trim());
    }
  };

  // Handle port configuration
  const configurePorts = async () => {
    try {
      const response = await fetch('/configure_connection', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          start_port: portRange.start,
          end_port: portRange.end
        })
      });
      
      if (!response.ok) throw new Error('Port configuration failed');
      await fetchConnections(); // Refresh connections after config change
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="connection-screen">
      <div className="header-section">
        <h2>Drone Connections</h2>
        <Button 
          variant="contained" 
          onClick={fetchConnections}
          disabled={loading}
        >
          {loading ? 'Refreshing...' : 'Refresh Connections'}
        </Button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="connection-list">
        <h3>Available Connections</h3>
        <List>
          {connections.length > 0 ? (
            connections.map(({ drone_id }, index) => (
              <ListItem 
                button 
                key={index}
                onClick={() => handleConnect(drone_id)}
              >
                <ListItemText primary={drone_id} />
              </ListItem>
            ))
          ) : (
            <ListItem>
              <ListItemText primary="No connections available" />
            </ListItem>
          )}
        </List>
      </div>

      <div className="manual-connection">
        <h3>Manual Connection</h3>
        <div className="input-group">
          <TextField
            fullWidth
            label="Enter Connection String"
            value={manualConnection}
            onChange={(e) => setManualConnection(e.target.value)}
            variant="outlined"
          />
          <Button
            variant="contained"
            onClick={handleManualConnect}
            disabled={!manualConnection.trim()}
          >
            Connect
          </Button>
        </div>
      </div>

      <Accordion expanded={advancedOpen} onChange={() => setAdvancedOpen(!advancedOpen)}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography>Advanced Connection Settings</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <div className="port-configuration">
            <h4>UDP Port Range</h4>
            <div className="port-inputs">
              <TextField
                label="Start Port"
                type="number"
                value={portRange.start}
                onChange={(e) => setPortRange({...portRange, start: parseInt(e.target.value)})}
              />
              <TextField
                label="End Port"
                type="number"
                value={portRange.end}
                onChange={(e) => setPortRange({...portRange, end: parseInt(e.target.value)})}
              />
              <Button
                variant="outlined"
                onClick={configurePorts}
                disabled={portRange.start > portRange.end}
              >
                Update Port Range
              </Button>
            </div>
          </div>
        </AccordionDetails>
      </Accordion>
    </div>
  );
};

export default ConnectionScreen;