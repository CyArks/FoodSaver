import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SustainabilityScore = () => {
    const [score, setScore] = useState(0);

    useEffect(() => {
        // Fetch the current score from the API
        axios.get('/api/get_sustainability_score')
            .then(response => {
                setScore(response.data.score);
            })
            .catch(error => {
                console.log('Error fetching score:', error);
            });
    }, []);

    return (
        <div>
            <h1>Your Sustainability Score</h1>
            <p>{score}</p>
        </div>
    );
};

export default SustainabilityScore;
