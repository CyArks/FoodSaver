import React from 'react';

const RecipeComponent = ({ recipes }) => (
    <div className="recipe-list">
        {recipes.map((recipe, index) => (
            <div key={index} className="recipe-item">
                <span>{recipe.name}</span>
                <span>Rating: {recipe.rating}</span>
            </div>
        ))}
    </div>
);

export default RecipeComponent;
