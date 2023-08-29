import React, { useState } from 'react';
import axios from 'axios';

const CreateRecipe = () => {
    const [formData, setFormData] = useState({
        name: '',
        ingredients: '',
        steps: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = () => {
        axios.post('/api/recipes', formData)
            .then(response => {
                alert('Recipe created successfully!');
            })
            .catch(error => {
                console.log('Error creating recipe:', error);
            });
    };

    return (
        <div>
            <h1>Create a New Recipe</h1>
            <form onSubmit={handleSubmit}>
                <input type="text" name="name" placeholder="Recipe name" onChange={handleChange} />
                <textarea name="ingredients" placeholder="Ingredients" onChange={handleChange}></textarea>
                <textarea name="steps" placeholder="Steps" onChange={handleChange}></textarea>
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default CreateRecipe;
