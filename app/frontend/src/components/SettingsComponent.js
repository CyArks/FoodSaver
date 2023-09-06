import React, { useState } from 'react';
import axios from 'axios';

const Settings = () => {
  const [message, setMessage] = useState('');

  const fetchSettings = async () => {
    try {
      const config = {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      };
      const response = await axios.get('/settings', config);
      setMessage(response.data.message);
    } catch (error) {
      console.error('An error occurred:', error);
    }
  };

  return (
    <div className="settings-container">
      <h1>Settings</h1>
      <button onClick={fetchSettings}>Fetch Settings</button>
      <div className="settings-message">
        {message ? <p>{message}</p> : <p>No settings available.</p>}
      </div>
    </div>
  );
};

export default Settings;
