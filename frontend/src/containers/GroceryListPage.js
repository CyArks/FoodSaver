import React, { useState, useEffect } from 'react';
import axios from 'axios';
import GroceryListComponent from './GroceryListComponent';

const GroceryListPage = () => {
  const [groceryLists, setGroceryLists] = useState([]);

  useEffect(() => {
    // Fetch grocery lists for the current user
    axios.get('/api/grocery_list')
      .then(response => {
        setGroceryLists(response.data);
      })
      .catch(error => {
        console.log('Error fetching grocery lists:', error);
      });
  }, []);

  return (
    <GroceryListComponent items={groceryLists} />
  );
};

export default GroceryListPage;
