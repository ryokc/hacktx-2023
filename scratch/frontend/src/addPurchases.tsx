import React, { useState, useEffect } from 'react';

function AppAddPurchase() {
  const [newPurchase, setNewPurchase] = useState('');
  const [purchases, setPurchases] = useState([]);
  
  const addPurchase = () => {
    // Send a POST request to Flask to add a new purchase
    fetch('http://127.0.0.1:5000/add_purchase', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ purchase: newPurchase }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Purchase added:', data);
      })
      .catch(error => {
        console.error('Error adding purchase:', error);
      });
  };

  return (
    <div>
      <input
        type="text"
        value={newPurchase}
        onChange={e => setNewPurchase(e.target.value)}
        placeholder="Enter a new purchase"
      />
      <button onClick={addPurchase}>Add Purchase</button>
    </div>
  );
}

export default AppAddPurchase;