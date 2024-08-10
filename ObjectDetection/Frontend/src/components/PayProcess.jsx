import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function PaymentProcessingPage() {
  const [userCreditCardInfo, setUserCreditCardInfo] = useState({
    nameOnCard: '',
    cardNumber: '',
    expiryDate: '',
  });
  const [cvc, setCvc] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserCreditCardInfo = async () => {
      try {
        const token = localStorage.getItem('token'); // Retrieve the token from localStorage
        const response = await axios.get('http://localhost:8000/backend/fetch_credit_card_info/', {
          headers: {
            'Authorization': `Token ${token}` // Include the token in the request headers
          }
        });
        const data = response.data;
        setUserCreditCardInfo({
          nameOnCard: data.nameOnCard,
          cardNumber: data.cardNumber,
          expiryDate: data.expiryDate,
        });
      } catch (error) {
        console.error('Failed to fetch user credit card information:', error);
      }
    };
  
    fetchUserCreditCardInfo();
  }, []);

  const handleCvcChange = (e) => {
    setCvc(e.target.value);
  };

  const confirmPayment = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/backend/verify_cvc', {
        userCreditCardInfo,
        cvc,
      });
      
      if (response.status === 200) {
        alert('Payment Confirmed');
        navigate('/guitable/receipt');
      } else {
        alert('CVC does not match. Please confirm your CVC.');
      }
    } catch (error) {
      console.error('Error confirming payment:', error);
      alert('Error confirming payment. Please try again.');
    }
  };

  return (
    <div className="payment-container">
      <h1>Payment Information</h1>
      <div className="payment-details">
        <p>Name on Card: {userCreditCardInfo.nameOnCard}</p>
        <p>Credit Card Number: **** **** **** {userCreditCardInfo.cardNumber.slice(-4)}</p>
        <p>Expiry Date: {userCreditCardInfo.expiryDate}</p>
      </div>
      <form onSubmit={confirmPayment} className="cvc-confirmation-form">
        <div className="form-field">
          <label htmlFor="cvc">Confirm CVC:</label>
          <input type="text" id="cvc" value={cvc} onChange={handleCvcChange} maxLength="4" />
        </div>
        <button type="submit" className="confirm-button">Confirm Payment</button>
      </form>
    </div>
  );
}

export default PaymentProcessingPage;
