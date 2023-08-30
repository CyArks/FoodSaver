import React from 'react';

const FridgeComponent = ({ items }) => {
    if (!items) {
        return <div className="fridge">Loading...</div>;
    }

    if (items.length === 0) {
        return <div className="fridge">Your fridge is empty.</div>;
    }

    return (
        <div className="fridge">
            {items.map((item) => (
                <div key={item.id} className="fridge-item">
                    <span>{item.name}</span>
                    <span>Expires on: {item.expirationDate}</span>
                </div>
            ))}
        </div>
    );
};

export default FridgeComponent;
