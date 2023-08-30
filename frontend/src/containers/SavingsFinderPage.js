import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SavingsFinder from '../components/SavingsFinder';

const SavingsPage = () => {
  const [deals, setDeals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/fetch_deals')
      .then(response => {
        setDeals(response.data);
        setLoading(false);
      })
      .catch(error => {
        alert('Error fetching deals. Please try again.');
        console.error('Error fetching deals:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <SavingsFinder deals={deals} />
  );
};

export default SavingsPage;
