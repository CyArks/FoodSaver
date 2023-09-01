import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MealPlanComponent = () => {
  const [mealPlans, setMealPlans] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {

        const response = await axios.get('/api/meal_plan');
        if (response.status === 200) {
          setMealPlans(response.data);
        }
      } catch (error) {
        alert('An error occurred while fetching the meal plans');
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Your Meal Plans</h1>
      <ul>
        {mealPlans.map((plan, index) => (
          <li key={index}>
            {plan.name} - {plan.description}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MealPlanComponent;
