import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProfileComponent = () => {
  const [profile, setProfile] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [dietaryPreferences, setDietaryPreferences] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/profile/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });
        if (response.status === 200) {
          setProfile(response.data);
          setUsername(response.data.username);
          setEmail(response.data.email);
          setDietaryPreferences(response.data.dietaryPreferences);
          setIsLoading(false);
        }
      } catch (error) {
        alert('An error occurred while fetching the profile');
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  const updateProfile = async () => {
    try {
      await axios.put('/profile/api/update_profile', {
        username,
        email,
        dietary_preferences: dietaryPreferences,
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      alert('Profile updated successfully');
    } catch (error) {
      alert('Failed to update profile');
    }
  };

  return (
    <div>
      <h1>User Profile</h1>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <div>
          <h2>{profile.username}</h2>
          <p>Email: {profile.email}</p>
          <p>Dietary Preferences: {profile.dietaryPreferences}</p>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="text"
            placeholder="Dietary Preferences"
            value={dietaryPreferences}
            onChange={(e) => setDietaryPreferences(e.target.value)}
          />
          <button onClick={updateProfile}>Update Profile</button>
        </div>
      )}
    </div>
  );
};

export default ProfileComponent;
