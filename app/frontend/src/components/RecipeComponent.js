import React from 'react';

const MealPlanComponent = ({ recipes }) => {
    if (!recipes) {
        return <div>Loading...</div>;
    }

    if (recipes.length === 0) {
        return <div>No meal plans available.</div>;
    }

    return (
        <div className="meal-plan">
            {recipes.map((recipe) => (
                <div key={recipe.id} className="meal-plan-item">
                    <span>{recipe.name}</span>
                    <span>Ingredients: {recipe.ingredients}</span>
                    <span>Steps: {recipe.steps}</span>
                </div>
            ))}
        </div>
    );
};

export default MealPlanComponent;
