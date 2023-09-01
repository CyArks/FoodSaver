import React, { useState, useEffect } from 'react';
import MealPlanComponent from '../components/MealPlanComponent';

// MealPlanPage is responsible for managing the meal plans
const MealPlanPage = () => {
  // State to hold the meal plans
  const [mealPlans, setMealPlans] = useState([]);
  // State to hold the new meal plan to be added
  const [newMealPlan, setNewMealPlan] = useState('');

  // Function to fetch meal plans from the backend
  const fetchMealPlans = async () => {
    // TODO: Make an API call to fetch meal plans from the backend
    // For now, we'll use some dummy data
    const dummyMealPlans = ['Meal Plan 1', 'Meal Plan 2'];
    setMealPlans(dummyMealPlans);
  };

  // Fetch meal plans when the component mounts
  useEffect(() => {
    fetchMealPlans();
  }, []);

  // Function to add a new meal plan
  const addMealPlan = () => {
    if (newMealPlan === '') {
      alert('Meal Plan cannot be empty');
      return;
    }

    // TODO: Make an API call to add the meal plan in the backend
    // For now, we'll just add it to the local state
    setMealPlans([...mealPlans, newMealPlan]);
    setNewMealPlan('');
  };

  return (
    <div>
      <MealPlanComponent mealPlans={mealPlans} />
      <input
        type="text"
        value={newMealPlan}
        onChange={(e) => setNewMealPlan(e.target.value)}
        placeholder="Add a new meal plan"
      />
      <button onClick={addMealPlan}>Add Meal Plan</button>
    </div>
  );
};

export default MealPlanPage;
