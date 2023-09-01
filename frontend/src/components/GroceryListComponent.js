import React, { useState, useEffect } from 'react';
import axios from 'axios';

const GroceryListComponent = () => {
  const [groceryList, setGroceryList] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Replace with your API endpoint
        const response = await axios.get('/api/grocery_list');
        if (response.status === 200) {
          setGroceryList(response.data);
        }
      } catch (error) {
        alert('An error occurred while fetching the grocery list');
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Your Grocery List</h1>
      <ul>
        {groceryList.map((item, index) => (
          <li key={index}>
            {item.name} - {item.weight}g
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GroceryListComponent;
