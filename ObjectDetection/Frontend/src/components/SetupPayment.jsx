// import React, { useState } from 'react';
// import axios from 'axios';
// import { useNavigate } from 'react-router-dom';

// function SetupPayment() {
//   const [nameOnCard, setNameOnCard] = useState('');
//   const [cardNumber, setCardNumber] = useState('');
//   const [expiryDate, setExpiryDate] = useState('');
//   const [cvc, setCvc] = useState('');
//   const navigate = useNavigate();

//   const handleDoneClick = async (e) => {
//       e.preventDefault();
//       try {
//           const response = await axios.post('http://localhost:8000/backend/setuppay/', {
//             name_on_card: nameOnCard,
//             card_number: cardNumber,
//             expiry_date: expiryDate,
//             cvc,
//           }, {
//             headers: {
//                 'Authorization': `Token ${userToken}`,  // Assuming you have the token stored in `userToken`
//                 'Content-Type': 'application/json',
//             }
//         });
//           console.log(response.data); // Logging the response data
//           if (response.status === 200) {
//               // Handle successful setup here
//               console.log('Payment setup successful');
//               // Optionally navigate to another route on success
//               // navigate('/success-route');
//           } else {
//               // Handle errors here, if any
//               console.log('Failed to setup payment');
//           }
//       } catch (error) {
//           console.error('Error during payment setup:', error);
//           if (error.response) {
//             // The request was made and the server responded with a status code
//             // that falls out of the range of 2xx
//             console.log(error.response.data);
//             console.log(error.response.status);
//             console.log(error.response.headers);
//           } else if (error.request) {
//             // The request was made but no response was received
//             console.log(error.request);
//           } else {
//             // Something happened in setting up the request that triggered an Error
//             console.log('Error', error.message);
//           }
//           alert('Failed to setup payment. Please check your input and try again.');
//       }
//   };

//   const handleSkipClick = () => {
//       console.log('Payment setup skipped');
//       navigate('/signin'); // Or wherever you want to navigate on skip
//   };

//   return (
//       <div className="payment-container">
//           <h2>Setup Payment</h2>
//           <input
//               type="text"
//               value={nameOnCard}
//               onChange={(e) => setNameOnCard(e.target.value)}
//               placeholder="Name on Card"
//           />
//           <input
//               type="text"
//               value={cardNumber}
//               onChange={(e) => setCardNumber(e.target.value)}
//               placeholder="Card Number"
//           />
//           <input
//               type="text"
//               value={expiryDate}
//               onChange={(e) => setExpiryDate(e.target.value)}
//               placeholder="Expiry Date (MM/YY)"
//           />
//           <input
//               type="text"
//               value={cvc}
//               onChange={(e) => setCvc(e.target.value)}
//               placeholder="CVC"
//           />
//           <button onClick={handleDoneClick}>Done</button>
//           <button onClick={handleSkipClick} className="skip-button">Skip</button>
//       </div>
//   );
// }

// export default SetupPayment;
