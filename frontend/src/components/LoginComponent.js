import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ListRecipes = () => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecipes = async () => {
      const token = localStorage.getItem('jwtToken');
      const config = {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      };

      try {
        const response = await axios.get('/api/login', config);
        setRecipes(response.data);
        setLoading(false);
      } catch (error) {
        if (error.response.status === 401) {
          localStorage.removeItem('jwtToken');
          alert('Unauthorized. Please login again.');
        } else {
          alert('An error occurred');
        }
        setLoading(false);
      }
    };

    fetchRecipes();
  }, []);

  return (
    <div>
      {loading ? (
        <div>Loading...</div>
      ) : (
        recipes.map((recipe) => (
          <div key={recipe.id}>
            <h2>{recipe.name}</h2>
            <p>{recipe.ingredients}</p>
            <p>{recipe.steps}</p>
          </div>
        ))
      )}
    </div>
  );
};

export default ListRecipes;
