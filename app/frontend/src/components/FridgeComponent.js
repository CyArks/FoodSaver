import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FridgeComponent = () => {
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Replace with your API endpoint
        const response = await axios.get('/api/fridge');
        if (response.status === 200) {
          setItems(response.data);
        }
      } catch (error) {
        alert('An error occurred while fetching fridge items');
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Your Fridge</h1>
      <ul>
        {items.map((item, index) => (
          <li key={index}>
            {item.name} - {item.weight}g
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FridgeComponent;
