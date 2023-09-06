import React, { useState, useEffect } from 'react';
import axios from 'axios';

const GroceryListComponent = () => {
  const [groceryLists, setGroceryLists] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Replace with your API endpoint
        const response = await axios.get('/api/grocery_list');
        if (response.status === 200) {
          setGroceryLists(response.data);
          setIsLoading(false);
        }
      } catch (error) {
        alert('An error occurred while fetching the grocery lists');
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Grocery Lists</h1>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <div>
          {groceryLists.map((list, index) => (
            <div key={index}>
              <h2>{list.name}</h2>
              <p>Items: {list.items.join(', ')}</p>
              <p>Weight: {list.weight} kg</p>
              {/* Add more grocery list details here */}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GroceryListComponent;
