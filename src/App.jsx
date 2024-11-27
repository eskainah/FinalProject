import { useState } from 'react'
import LoginSignup from './components/Auth/LoginSignup'
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";

import './App.css'

function App() {
  const logo = "/logo.png";
  const [showLoginSignup, setShowLoginSignup] = useState(false);

  const toggleLoginSignup = () => {
    setShowLoginSignup((prev) => !prev);
  };

  return (
    <AuthProvider>
    <Router>
      <Routes>
        <Route
          path="/"
          element={
    <div className="container">
      <header>
        <section>
          <img src={logo} alt=""/>
        </section>
        <nav>
        
          <a href="">Home</a>
          <a href="">About</a>
          <a href="">Contact Us</a>
        
        </nav>
      </header> 
      <div className='hero'>
        <p><strong>Attendance Simplified, Results amplified <br />
          Be here now, thrive everywhere  </strong>
        </p>
        <button className="signinBtn" onClick={toggleLoginSignup}>Sign In</button>
        {showLoginSignup && <LoginSignup onClose={toggleLoginSignup} />}
      </div>
     
  </div>
   }
   />
 </Routes>
</Router>
</AuthProvider>
)}
  
export default App
