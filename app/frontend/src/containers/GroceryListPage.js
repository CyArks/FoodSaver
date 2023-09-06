import React, { useState, useEffect } from 'react';
import axios from 'axios';
import GroceryListComponent from '../components/GroceryListComponent';

const GroceryListPage = () => {
  const [groceryLists, setGroceryLists] = useState([]);
  const [newGroceryList, setNewGroceryList] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const fetchGroceryLists = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get('/api/get_grocery_lists', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      setGroceryLists(response.data);
    } catch (error) {
      setErrorMessage('Failed to fetch grocery lists');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchGroceryLists();
  }, []);

  const validateInput = () => {
    if (newGroceryList.trim() === '') {
      setErrorMessage('Grocery List cannot be empty');
      return false;
    }
    return true;
  };

  const addGroceryList = async () => {
    if (!validateInput()) return;

    try {
      await axios.post('/api/create_grocery_list', { name: newGroceryList }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      setNewGroceryList('');
      setErrorMessage('');
      fetchGroceryLists();  // Refresh the list
    } catch (error) {
      setErrorMessage('Failed to add grocery list');
    }
  };

  return (
    <div>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <>
          <GroceryListComponent groceryLists={groceryLists} />
          <input
            type="text"
            value={newGroceryList}
            onChange={(e) => setNewGroceryList(e.target.value)}
            placeholder="Add a new grocery list"
          />
          <button onClick={addGroceryList}>Add Grocery List</button>
          {errorMessage && <p className="error-message">{errorMessage}</p>}
        </>
      )}
    </div>
  );
};

export default GroceryListPage;
