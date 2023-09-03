import React, { useState } from 'react';
import axios from 'axios';

const ChangePassword = () => {
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleChangePassword = async () => {
    try {
      const response = await axios.post('/change_password', {
        new_password: newPassword,
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`, // Replace with your JWT token
        },
      });

      setMessage(response.data.message);
    } catch (error) {
      setMessage('Failed to change password');
    }
  };

  return (
    <div>
      <h1>Change Password</h1>
      <input
        type="password"
        placeholder="New Password"
        value={newPassword}
        onChange={(e) => setNewPassword(e.target.value)}
      />
      <button onClick={handleChangePassword}>Change Password</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default ChangePassword;
