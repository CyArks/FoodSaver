import React, { useState, useEffect } from 'react';

const DarkModeToggle = () => {
  const [darkMode, setDarkMode] = useState(false);

  // Toggle dark mode
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  // Apply dark mode settings
  useEffect(() => {
    if (darkMode) {
      document.documentElement.style.setProperty('--bg-color', '#333');
      document.documentElement.style.setProperty('--text-color', '#FFF');
    } else {
      document.documentElement.style.setProperty('--bg-color', '#FFF');
      document.documentElement.style.setProperty('--text-color', '#333');
    }
  }, [darkMode]);

  return (
    <button onClick={toggleDarkMode}>
      {darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
    </button>
  );
};

export default DarkModeToggle;
