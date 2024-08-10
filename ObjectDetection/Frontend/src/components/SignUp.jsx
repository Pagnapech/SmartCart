import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function SignUpPage() {
  // Combined state for both sign-up and payment setup forms
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    nameOnCard: '',
    cardNumber: '',
    expiryDate: '',
    cvc: '',
  });

  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({ ...prevState, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Single API call with both the sign-up and payment data
      await axios.post('http://localhost:8000/backend/signup/', formData);
      navigate('/SignIn'); // Navigate to a success page or handle next steps
    } catch (error) {
      console.error('Error submitting data', error);
      // Handle error
    }
  };

  return (
    <div className="signup-payment-container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ display: 'flex', width: '100%' }}>
        {/* Sign-up form */}
        <div className="signup-form" style={{ flex: 1, marginRight: '20px' }}>
          <h2>Sign Up</h2>
          <input type="text" name="name" value={formData.name} onChange={handleInputChange} placeholder="Name" />
          <input type="email" name="email" value={formData.email} onChange={handleInputChange} placeholder="Email" />
          <input type="password" name="password" value={formData.password} onChange={handleInputChange} placeholder="Password" />
        </div>

        {/* Payment setup form */}
        <div className="payment-setup-form" style={{ flex: 1 }}>
          <h2>Setup Payment</h2>
          <input type="text" name="nameOnCard" value={formData.nameOnCard} onChange={handleInputChange} placeholder="Name on Card" />
          <input type="text" name="cardNumber" value={formData.cardNumber} onChange={handleInputChange} placeholder="Card Number" />
          <input type="text" name="expiryDate" value={formData.expiryDate} onChange={handleInputChange} placeholder="Expiry Date" />
          <input type="text" name="cvc" value={formData.cvc} onChange={handleInputChange} placeholder="CVC" />
        </div>
      </div>

      {/* Sign Up button */}
      <button onClick={handleSubmit} style={{ marginTop: '20px', padding: '10px 20px', width: 'calc(100% - 40px)', maxWidth: '600px', borderRadius: '5px', backgroundColor: '#007bff', color: 'white', fontSize: '16px', border: 'none', cursor: 'pointer' }}>
        Sign Up
      </button>
    </div>
  );
}

export default SignUpPage;
