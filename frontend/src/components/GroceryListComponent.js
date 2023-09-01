import React, { useState, useEffect } from 'react';
import GroceryListComponent from '../components/GroceryListComponent';

// GroceryListPage is responsible for managing the grocery lists
const GroceryListPage = () => {
  // State to hold the grocery lists
  const [groceryLists, setGroceryLists] = useState([]);
  // State to hold the new grocery list to be added
  const [newGroceryList, setNewGroceryList] = useState('');

  // Function to fetch grocery lists from the backend
  const fetchGroceryLists = async () => {
    // TODO: Make an API call to fetch grocery lists from the backend
    // For now, we'll use some dummy data
    const dummyGroceryLists = ['Grocery List 1', 'Grocery List 2'];
    setGroceryLists(dummyGroceryLists);
  };

  // Fetch grocery lists when the component mounts
  useEffect(() => {
    fetchGroceryLists();
  }, []);

  // Function to add a new grocery list
  const addGroceryList = () => {
    if (newGroceryList === '') {
      alert('Grocery List cannot be empty');
      return;
    }

    // TODO: Make an API call to add the grocery list in the backend
    // For now, we'll just add it to the local state
    setGroceryLists([...groceryLists, newGroceryList]);
    setNewGroceryList('');
  };

  return (
    <div>
      <GroceryListComponent groceryLists={groceryLists} />
      <input
        type="text"
        value={newGroceryList}
        onChange={(e) => setNewGroceryList(e.target.value)}
        placeholder="Add a new grocery list"
      />
      <button onClick={addGroceryList}>Add Grocery List</button>
    </div>
  );
};

export default GroceryListPage;
