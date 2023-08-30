import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ListRecipes = () => {
    const [recipes, setRecipes] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get('/api/recipes')
            .then(response => {
                setRecipes(response.data);
                setLoading(false);
            })
            .catch(error => {
                alert('Error fetching recipes. Please try again.');
                console.error('Error fetching recipes:', error);
                setLoading(false);
            });
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (recipes.length === 0) {
        return <div>No recipes available.</div>;
    }

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
