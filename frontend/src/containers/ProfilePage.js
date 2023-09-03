import React, { useState } from 'react';
import axios from 'axios';

const Profile = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [dietaryPreferences, setDietaryPreferences] = useState('');

  const updateProfile = async () => {
    try {
      await axios.put('/update_profile', {
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
      <h1>Profile</h1>
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
  );
};

export default Profile;
