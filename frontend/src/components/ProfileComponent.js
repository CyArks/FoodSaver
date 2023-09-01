import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MealPlanComponent = () => {
  const [mealPlans, setMealPlans] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Replace with your API endpoint
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
        <div>
          {mealPlans.map((plan, index) => (
            <div key={index}>
              <h2>{plan.name}</h2>
              <p>Recipes: {plan.recipes.join(', ')}</p>
              {/* Add more meal plan details here */}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MealPlanComponent;
