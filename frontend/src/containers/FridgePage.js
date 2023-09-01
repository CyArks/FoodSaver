import React, { useState } from 'react';
import FridgeComponent from '../components/FridgeComponent';

// FridgePage is responsible for managing the fridge items
const FridgePage = () => {
  // State to hold the fridge items
  const [fridgeItems, setFridgeItems] = useState([]);
  // State to hold the new item to be added
  const [newItem, setNewItem] = useState('');

  // Function to add a new item to the fridge
  const addItem = () => {
    if (newItem === '') {
      alert('Item cannot be empty');
      return;
    }

    // TODO: Make an API call to add the item to the fridge in the backend
    // For now, we'll just add it to the local state
    setFridgeItems([...fridgeItems, newItem]);
    setNewItem('');
  };

  return (
    <div>
      <FridgeComponent fridgeItems={fridgeItems} />
      <input
        type="text"
        value={newItem}
        onChange={(e) => setNewItem(e.target.value)}
        placeholder="Add a new item"
      />
      <button onClick={addItem}>Add Item</button>
    </div>
  );
};

export default FridgePage;
