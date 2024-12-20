import { useState, useEffect } from "react";
import LoginSignup from "./components/Auth/LoginSignup";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Dashboard from "./components/DashBoard/Dashboard";
import { ApiProvider } from "./context/ApiContext"; 
import Attendance from "./components/DashBoard/Attendance";
import AttendanceOverview from "./components/DashBoard/TeacherDashboard/TeacherAttendanceOverView";
import './App.css'

function App() {
  const logo = "/logo.png";
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Track login status
  const [showLogin, setShowLogin] = useState(false); // State to toggle login/signup form

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      setIsLoggedIn(true); // If the token exists, consider the user logged in
    } else {
      setIsLoggedIn(false); // If no token, consider the user logged out
    }
  }, []);

  const handleLoginSuccess = () => {
    console.log("Login successful, updating state...");
    setIsLoggedIn(true); // Update login status
    setShowLogin(false); // Close the login form after successful login
    window.location.reload();
  };

  const handleSignInClick = () => {
    setShowLogin(true); // Show the LoginSignup form when the "Sign In" button is clicked
  };

  const handleCloseModal = () => {
    setShowLogin(false); // Close the modal when clicking outside or on close
  };

  return (
    <AuthProvider>
      <ApiProvider>
        <Router>
          <Routes>
            {/* Dashboard Route */}
            <Route
              path="/"
              element={
                isLoggedIn ? (
                  <Dashboard />
                ) : (
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
                        </strong> <br />
                       
                      </p>
                      <button className="signinBtn" onClick={handleSignInClick}>
                        Sign In
                      </button>
                      {showLogin && (
                        <LoginSignup onClose={handleCloseModal} onLoginSuccess={handleLoginSuccess} />
                      )}
                    </div>
                  </div>
                )
              }
            >

              <Route path="/course/:courseName" element={<Attendance />} />
              <Route path="/attendance-overview" element={<AttendanceOverview />} />
            </Route>
          </Routes>
        </Router>
      </ApiProvider>
    </AuthProvider>
  );
}

export default App;
