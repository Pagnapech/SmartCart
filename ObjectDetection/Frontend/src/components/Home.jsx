import React from 'react';
import { useNavigate } from 'react-router-dom';
import logo from './SClogo.png'; // Adjust this path as necessary


export function Home() {

    const navigate = useNavigate();

    const handleNewCustomer = () => {
        navigate('/signup');
    };

    const handleReturnCustomer = () => {
        navigate('/signin');
    };

    return (
        <div className="home-container">
            <img src={logo} alt="Smart Cart Logo" className="home-logo" />
            <h1>Hello! Choose One to Continue.</h1>
            <div className="home-buttonContainer">
                <button onClick={handleNewCustomer} className="home-button">New Customer</button>
                <button onClick={handleReturnCustomer} className="home-button">Return Customer</button>
            </div>
        </div>
    );
}
