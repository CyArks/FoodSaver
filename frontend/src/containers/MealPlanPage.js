import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MealPlanComponent from './MealPlanComponent';

const MealPlanPage = () => {
  const [mealPlans, setMealPlans] = useState([]);

  useEffect(() => {
    // Fetch meal plans for the current user
    axios.get('/api/meal_plan')
      .then(response => {
        setMealPlans(response.data);
      })
      .catch(error => {
        console.log('Error fetching meal plans:', error);
      });
  }, []);  // Empty dependency array means this useEffect runs once when the component mounts

  return (
    <MealPlanComponent recipes={mealPlans} />
  );
};

export default MealPlanPage;
