import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ListRecipes = () => {
    const [recipes, setRecipes] = useState([]);

    useEffect(() => {
        axios.get('/api/recipes')
            .then(response => {
                setRecipes(response.data);
            })
            .catch(error => {
                console.log('Error fetching recipes:', error);
            });
    }, []);

    return (
        <div>
            <h1>All Recipes</h1>
            {recipes.map(recipe => (
                <div key={recipe.id}>
                    <h2>{recipe.name}</h2>
                    <p>{recipe.ingredients}</p>
                    <p>{recipe.steps}</p>
                </div>
            ))}
        </div>
    );
};

export default ListRecipes;
