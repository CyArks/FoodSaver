// ExpirationAlerts.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ExpirationAlerts = () => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.get('/api/expiration-alerts'); // Replace with your API endpoint
      setAlerts(response.data);
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Expiration Alerts</h1>
      <ul>
        {alerts.map((alert, index) => (
          <li key={index}>{alert.message}</li>
        ))}
      </ul>
    </div>
  );
};

export default ExpirationAlerts;
