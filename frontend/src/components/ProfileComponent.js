import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Profile = () => {
  const [profileData, setProfileData] = useState({});

  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem('jwtToken');
      const config = {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      };

      try {
        const response = await axios.get('/api/profile', config);
        setProfileData(response.data);
      } catch (error) {
        if (error.response.status === 401) {
          localStorage.removeItem('jwtToken');
          alert('Unauthorized. Please login again.');
        } else {
          alert('An error occurred');
        }
      }
    };

    fetchProfile();
  }, []);

  return (
    <div>
      <h1>{profileData.name}</h1>
      <p>{profileData.email}</p>
      {/* Add more profile fields here */}
    </div>
  );
};

export default Profile;
