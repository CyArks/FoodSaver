import React, { useState } from 'react';
import axios from 'axios';

const CreateRecipe = () => {
  const [formData, setFormData] = useState({
    name: '',
    ingredients: '',
    steps: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem('jwtToken');
    const config = {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    };

    try {
      const response = await axios.post('/api/recipes', formData, config);
      alert('Recipe created successfully');
    } catch (error) {
      if (error.response.status === 401) {
        localStorage.removeItem('jwtToken');
        alert('Unauthorized. Please login again.');
      } else {
        alert('An error occurred');
      }
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="Recipe Name"
        />
        <textarea
          name="ingredients"
          value={formData.ingredients}
          onChange={handleChange}
          placeholder="Ingredients"
        ></textarea>
        <textarea
          name="steps"
          value={formData.steps}
          onChange={handleChange}
          placeholder="Steps"
        ></textarea>
        <button type="submit">Create Recipe</button>
      </form>
    </div>
  );
};

export default CreateRecipe;
