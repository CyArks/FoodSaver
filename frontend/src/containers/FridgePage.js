import React, { useState } from 'react';
import FridgeComponent from '../components/FridgeComponent';

const FridgePage = () => {
    const [fridgeItems, setFridgeItems] = useState([
        { name: 'Milk', expirationDate: '2023-08-30' },
        { name: 'Cheese', expirationDate: '2023-09-15' },
    ]);

    const addItem = () => {
        // Simulating adding a new item to the fridge
        const newItem = { name: 'Eggs', expirationDate: '2023-08-25' };
        setFridgeItems([...fridgeItems, newItem]);
    };

    return (
        <div className="fridge-page">
            <h1>Your Fridge</h1>
            <FridgeComponent items={fridgeItems} />
            <button onClick={addItem}>Add New Item</button>
        </div>
    );
};

export default FridgePage;
