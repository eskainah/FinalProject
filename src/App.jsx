import { useState, useContext } from "react";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";

import { ApiProvider } from "./context/ApiContext"; 
import  './App.css';


function App() {
  const logo = "/logo.png";
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Track login status

  // const handleLoginSuccess = () => {
  //   console.log("Login successful, updating state...");
  //   setIsLoggedIn(true); // Update login status
  // };

  return (
    <AuthProvider>
      <ApiProvider>
      
            <div className="container">
              <header>
                <section>
                  <img src={logo} alt="Logo" />
                </section>
                  <nav>
                    <a href="#">Home</a>
                    <a href="#">About</a>
                    <a href="#">Contact Us</a>
                  </nav>
              </header>
              <div className="hero">
                <p>
                  <strong>
                    Attendance Simplified, Results amplified <br />
                    Be here now, thrive everywhere
                  </strong>
                </p>
                <button className="signinBtn">Sign In</button>
                  {/* <LoginSignup onLoginSuccess={handleLoginSuccess} /> */}
              </div>
            </div>
       
      </ApiProvider>
    </AuthProvider>
  
  
   
   
  );
}

export default App;
