import React from 'react';
import PropTypes from 'prop-types';

const Profile = ({ profile, isLoading, username, email, dietaryPreferences, setUsername, setEmail, setDietaryPreferences, updateProfile }) => {
  if (isLoading) {
    return <div className="profile-container"><p>Loading...</p></div>;
  }

  return (
    <div className="profile-container">
      <h1>{profile.username}'s Profile</h1>
      <div className="profile-details">
        <p><strong>Email:</strong> {profile.email}</p>
        <p><strong>Dietary Preferences:</strong> {profile.dietaryPreferences}</p>
      </div>
      <div className="profile-update-form">
        <h2>Update Profile</h2>
        <div className="input-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="input-group">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="input-group">
          <label htmlFor="dietaryPreferences">Dietary Preferences</label>
          <input
            id="dietaryPreferences"
            type="text"
            placeholder="Dietary Preferences"
            value={dietaryPreferences}
            onChange={(e) => setDietaryPreferences(e.target.value)}
          />
        </div>
        <button className="update-button" onClick={updateProfile}>Update Profile</button>
      </div>
    </div>
  );
};

Profile.propTypes = {
  profile: PropTypes.object.isRequired,
  isLoading: PropTypes.bool.isRequired,
  username: PropTypes.string.isRequired,
  email: PropTypes.string.isRequired,
  dietaryPreferences: PropTypes.string.isRequired,
  setUsername: PropTypes.func.isRequired,
  setEmail: PropTypes.func.isRequired,
  setDietaryPreferences: PropTypes.func.isRequired,
  updateProfile: PropTypes.func.isRequired,
};

export default Profile;
