import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Home } from './components/Home.jsx';
import { GUITable } from './components/Display.jsx';
import { Receipt } from './components/Receipt.jsx';
import { MyComponent } from './components/SignIn.jsx';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import SignUpPage from './components/SignUp.jsx';
// import SetupPayment from './components/SetupPayment.jsx';
import PaymentProcessingPage from './components/PayProcess.jsx';

function App() {
  return (
    <div>
      
      <BrowserRouter>
      <div>
        {/* <Navigation/> */}
          <Routes>
            <Route path="/SignUp" element={<SignUpPage />} />
            <Route path="/SignIn" element={<MyComponent />} />
            <Route path="/" element={<Home />}  exact/>
            <Route path="/guitable" element={<GUITable />} />
            <Route path="/PayProcess" element={<PaymentProcessingPage />} />
            <Route path="/guitable/receipt" element={<Receipt />} /> 


          </Routes>
      
      </div>
      </BrowserRouter >
      
      </div>
    
  );
}

export default App;



/**hello my name is kaavian
 * Whats up homie.
 */

//wazzaaaa


