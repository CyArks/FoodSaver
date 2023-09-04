import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProfileComponent = () => {
  const [profile, setProfile] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/profile', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });
        if (response.status === 200) {
          setProfile(response.data);
          setIsLoading(false);
        }
      } catch (error) {
        alert('An error occurred while fetching the profile');
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Your Profile</h1>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <div>
          <p>Username: {profile.username}</p>
          <p>Email: {profile.email}</p>
          <p>Dietary Preferences: {profile.dietary_preferences}</p>
        </div>
      )}
    </div>
  );
};

const MealPlanComponent = () => {
  const [mealPlans, setMealPlans] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/meal_plan', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });
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
      <h1>Your Meal Plans</h1>
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

const ProfilePage = () => {
  return (
    <div>
      <ProfileComponent />
      <hr />
      <MealPlanComponent />
    </div>
  );
};

export default ProfilePage;
