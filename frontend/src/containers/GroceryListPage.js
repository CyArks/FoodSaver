import React, { useState, useEffect } from 'react';
import axios from 'axios';
import GroceryListComponent from './GroceryListComponent';

const GroceryListPage = () => {
  const [groceryLists, setGroceryLists] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/grocery_list')
      .then(response => {
        setGroceryLists(response.data);
        setLoading(false);
      })
      .catch(error => {
        alert('Error fetching grocery lists. Please try again.');
        console.error('Error fetching grocery lists:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <GroceryListComponent items={groceryLists} />
  );
};

export default GroceryListPage;
