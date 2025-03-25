import React, { useState } from 'react';

const UploadPathButton = ({ vehicleID, paths }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleUpload = async () => {
    if (!vehicleID) {
      setError('Please select a vehicle first');
      return;
    }
    if (paths.length === 0) {
      setError('Please draw a path first');
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const response = await fetch('/paths', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          vehicleID,
          paths,
        }),
      });

      if (!response.ok) throw new Error('Failed to upload path');
      
      setSuccess(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="upload-path">
      <button 
        onClick={handleUpload}
        disabled={isLoading || !vehicleID || paths.length === 0}
      >
        {isLoading ? 'Uploading...' : 'Upload Path'}
      </button>
      
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">Path uploaded successfully!</div>}
    </div>
  );
};

export default UploadPathButton;