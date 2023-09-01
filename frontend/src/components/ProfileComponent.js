import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProfileComponent = () => {
  const [profile, setProfile] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Replace with your API endpoint
        const response = await axios.get('/api/profile');
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
          <p>Name: {profile.name}</p>
          <p>Email: {profile.email}</p>
          <p>Sustainability Score: {profile.sustainability_score}</p>
          {/* Add more profile details here */}
        </div>
      )}
    </div>
  );
};

export default ProfileComponent;
