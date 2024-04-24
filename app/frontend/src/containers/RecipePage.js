<<<<<<< HEAD:frontend/src/containers/RecipePage.js
import React, { useState } from 'react';
import RecipeComponent from '../components/RecipeComponent';

const RecipePage = () => {
    const [recipes, setRecipes] = useState([
        { name: 'Pasta', rating: 4.5 },
        { name: 'Pizza', rating: 4.7 },
    ]);

    const [searchTerm, setSearchTerm] = useState('');

    const handleSearch = () => {
        // Simulating a search query, replace this with an actual API call
        const newRecipes = [
            { name: 'Spaghetti', rating: 4.2 },
            { name: 'Salad', rating: 3.8 },
        ];
        setRecipes(newRecipes);
    };

    return (
        <div className="recipe-page">
            <h1>Find a Recipe</h1>
            <input
                type="text"
                placeholder="Search..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            <button onClick={handleSearch}>Search</button>
            <RecipeComponent recipes={recipes} />
        </div>
    );
};

export default RecipePage;
=======
import React, { useState } from 'react';
import RecipeComponent from '../components/RecipeComponent';

const RecipePage = () => {
    const [recipes, setRecipes] = useState([
        { name: 'Pasta', rating: 4.5 },
        { name: 'Pizza', rating: 4.7 },
    ]);

    const [searchTerm, setSearchTerm] = useState('');

    const handleSearch = () => {
        // TODO: Replace this with an actual API call
        const newRecipes = [
            { name: 'Spaghetti', rating: 4.2 },
            { name: 'Salad', rating: 3.8 },
        ];
        setRecipes(newRecipes);
    };

    return (
        <div className="recipe-page">
            <h1>Find a Recipe</h1>
            <input
                type="text"
                placeholder="Search..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            <button onClick={handleSearch}>Search</button>
            {recipes.length > 0 ? (
                <RecipeComponent recipes={recipes} />
            ) : (
                <p>No recipes found for "{searchTerm}"</p>
            )}
        </div>
    );
};

export default RecipePage;
>>>>>>> b2281d0f31a00b7a805a9cd78fa2455b23fec8b5:app/frontend/src/containers/RecipePage.js
