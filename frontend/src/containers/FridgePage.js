import React, { useState } from 'react';
import FridgeComponent from '../components/FridgeComponent';

const FridgePage = () => {
    const [fridgeItems, setFridgeItems] = useState([
        { name: 'Milk', expirationDate: '2023-08-30' },
        { name: 'Cheese', expirationDate: '2023-09-15' },
    ]);
    const [newItem, setNewItem] = useState({ name: '', expirationDate: '' });

    const addItem = () => {
        if (!newItem.name || !newItem.expirationDate) {
            alert('Both name and expiration date are required.');
            return;
        }
        setFridgeItems([...fridgeItems, newItem]);
        setNewItem({ name: '', expirationDate: '' });
    };

    return (
        <div className="fridge-page">
            <h1>Your Fridge</h1>
            <FridgeComponent items={fridgeItems} />
            <input type="text" placeholder="Item Name" value={newItem.name} onChange={(e) => setNewItem({ ...newItem, name: e.target.value })} />
            <input type="date" placeholder="Expiration Date" value={newItem.expirationDate} onChange={(e) => setNewItem({ ...newItem, expirationDate: e.target.value })} />
            <button onClick={addItem}>Add New Item</button>
        </div>
    );
};

export default FridgePage;
