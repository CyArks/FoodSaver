import React from 'react';

const FridgeComponent = ({ items }) => (
    <div className="fridge">
        {items.map((item, index) => (
            <div key={index} className="fridge-item">
                <span>{item.name}</span>
                <span>Expires on: {item.expirationDate}</span>
            </div>
        ))}
    </div>
);

export default FridgeComponent;
