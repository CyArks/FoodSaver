import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MealPlanComponent from './MealPlanComponent';

const MealPlanPage = () => {
  const [mealPlans, setMealPlans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/meal_plan')
      .then(response => {
        setMealPlans(response.data);
        setLoading(false);
      })
      .catch(error => {
        alert('Error fetching meal plans. Please try again.');
        console.error('Error fetching meal plans:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <MealPlanComponent recipes={mealPlans} />
  );
};

export default MealPlanPage;
