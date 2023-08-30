import React from 'react';

const GroceryListComponent = ({ items }) => {
    if (!items) {
        return <div>Loading...</div>;
    }

    if (items.length === 0) {
        return <div>Your grocery list is empty.</div>;
    }

    return (
        <div className="grocery-list">
            {items.map((item) => (
                <div key={item.id} className="grocery-item">
                    <span>{item.name}</span>
                    <span>Quantity: {item.quantity}</span>
                </div>
            ))}
        </div>
    );
};

export default GroceryListComponent;
