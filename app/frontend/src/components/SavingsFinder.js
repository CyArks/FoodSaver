<<<<<<< HEAD:frontend/src/components/SavingsFinder.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SavingsFinder = () => {
    const [deals, setDeals] = useState({});

    useEffect(() => {
        axios.get('/api/fetch_deals')
            .then(response => {
                setDeals(response.data);
            })
            .catch(error => {
                console.error('Error fetching deals:', error);
            });
    }, []);

    return (
        <div>
            <h1>Savings Finder & Local Deal Alerts</h1>
            <div>
                <h2>Too Good To Go Deals</h2>
                {/* Render "Too Good To Go" deals */}
                {deals.too_good_to_go && deals.too_good_to_go.map(deal => (
                    <div key={deal.id}>
                        <h3>{deal.name}</h3>
                        <p>{deal.description}</p>
                    </div>
                ))}
            </div>

            {/* Uncomment below when adding more local stores */}
            {/* <div>
                <h2>Local Store Deals</h2>
                {deals.local_store && deals.local_store.map(deal => (
                    <div key={deal.id}>
                        <h3>{deal.name}</h3>
                        <p>{deal.description}</p>
                    </div>
                ))}
            </div> */}
        </div>
    );
};

export default SavingsFinder;
=======
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SavingsFinder = () => {
    const [deals, setDeals] = useState({});
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

    if (!deals.too_good_to_go || deals.too_good_to_go.length === 0) {
        return <div>No deals available.</div>;
    }

    return (
        <div>
            <h1>Savings Finder & Local Deal Alerts</h1>
            <div>
                <h2>Too Good To Go Deals</h2>
                {deals.too_good_to_go.map(deal => (
                    <div key={deal.id}>
                        <h3>{deal.name}</h3>
                        <p>{deal.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SavingsFinder;
>>>>>>> b2281d0f31a00b7a805a9cd78fa2455b23fec8b5:app/frontend/src/components/SavingsFinder.js
