import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MealPlanComponent = () => {
  const [mealPlans, setMealPlans] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {

        const response = await axios.get('/api/meal_plan');
        if (response.status === 200) {
          setMealPlans(response.data);
          setIsLoading(false);
        }
      } catch (error) {
        alert('An error occurred while fetching the meal plans');
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Meal Plans</h1>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {mealPlans.map((plan, index) => (
            <li key={index}>
              Plan {index + 1}: {plan.recipe_ids.join(', ')}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MealPlanComponent;
