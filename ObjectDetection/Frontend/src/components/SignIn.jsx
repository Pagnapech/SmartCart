import React, { useState } from 'react';
import axios from 'axios';

import { useNavigate } from 'react-router-dom';

export const MyComponent = () => {

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  
  const handleSignIn = async (e) => {
    e.preventDefault();
    try {
      // Adjusted the API endpoint to match your backend's expected endpoint for sign-in
      const response = await axios.post('http://localhost:8000/backend/signin/', { email, password });
      // Assuming the token is returned in response.data.token
      localStorage.setItem('token', response.data.token);
      console.log(response.data)
      // Redirect to the "guicart" page on successful sign-in
      navigate('/guitable');
    } catch (error) {
      console.log(error.response)
      console.error('Sign-in error', error.response || error);
      alert('Failed to sign in. Please check your credentials and try again.'); // Providing user feedback on failure
    }
  };
  
  return (
    <>
      <h2 className="welcome-message">Welcome!</h2>
      <form onSubmit={handleSignIn}>
        <input 
          type="email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          placeholder="Email" 
          required 
        />
        <input 
          type="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          placeholder="Password" 
          required 
        />
        <button type="submit">Sign In</button>
      </form>
    </>
  );
}


export default MyComponent;