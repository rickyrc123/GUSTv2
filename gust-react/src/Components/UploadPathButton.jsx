import React from 'react';

function UploadPathButton({ vehicleID, paths }) {
  const handleUpload = () => {
    if (!vehicleID) {
      alert('Please select a vehicle first.');
      return;
    }

    if (paths.length === 0 || paths.every((path) => path.length === 0)) {
      alert('Please draw a path first.');
      return;
    }

    // Prepare the data to send
    const data = {
      vehicleID,
      paths,
    };

    // Send the data to the API
    fetch('/paths', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((result) => {
        alert('Path uploaded successfully!');
        console.log('Upload result:', result);
      })
      .catch((error) => {
        console.error('Error uploading path:', error);
        alert('Failed to upload path.');
      });
  };

  return (
    <button onClick={handleUpload} style={{ marginTop: '10px' }}>
      Upload Path
    </button>
  );
}

export default UploadPathButton;