import { useEffect, useRef, useState, useContext } from "react";
import "./LoginSignup.css";
import { AuthContext } from "../../context/AuthContext";
import UserRegistrationForm from "./UserRegistrationForm";

function LoginSignup({ onClose, onLoginSuccess }) {
  const modalRef = useRef(null);

  // Close the modal when clicking outside of the modal (outside the overlay and content)
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (modalRef.current && !modalRef.current.contains(e.target)) {
        onClose();
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [onClose]);

  const [activeSection, setActiveSection] = useState("login"); // 'login' or 'createAcc'

  const handleButtonClick = (section) => {
    setActiveSection(section);
    setError(""); // Clear the error when switching tabs
    if (section === 'createAcc') {
      // Reset the new user form if switching to 'createAcc'
      setNewUser({
        username: "",
        email: "",
        password: "",
        school_name: "",
        role: "student",
        first_name: "",
        middle_name: "",
        last_name: "",
      });
    } else if (section === 'login') {
      // Reset login form fields when switching to 'login'
      setCredentials({ username: "", password: "" });
    }
  };

  const { login, register } = useContext(AuthContext);
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [newUser, setNewUser] = useState({
    username: "",
    email: "",
    password: "",
    school_name: "",
    role: "student",
    first_name: "",
    middle_name: "",
    last_name: "",
  });
  const [error, setError] = useState("");

// Custom login handler
const handleLoginSubmit = async (e) => {
  e.preventDefault();

  if (!credentials.username || !credentials.password) {
    setError("Please enter both username and password.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/api/auth/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    });

    const data = await response.json();
    console.log("API Response:", data); // Debug log

    if (response.ok) {
      if (data && data.token) {
        // On success, store the token using the login function from context
        login(data.username, data.role, data.token); // Assuming login saves token to context
        alert("Login successful!");
        onLoginSuccess(); // Notify App about login success
        setError(""); // Clear error
      } else {
        setError("Unexpected response from server.");
      }
    } else {
      setError(data.message || "Invalid credentials.");
    }
  } catch (error) {
    setError("An error occurred. Please try again.");
    console.error("Login error:", error);
  }
};

  
  
  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
  
    // Validate that all required fields are filled
    if (
      !newUser.username ||
      !newUser.email ||
      !newUser.password ||
      newUser.role !== "admin" || // Only allow 'admin' role for registration
      !newUser.first_name ||
      !newUser.last_name ||
      !newUser.school_name // Ensure 'school_name' is filled
    ) {
      if (newUser.role !== "admin") {
        setError("Only Admin role can register.");
        return;
      }
      setError("Please fill in all required fields.");
     
      return;
    }
  
    try {
      const response = await fetch("http://127.0.0.1:8000/api/auth/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newUser),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        alert("Registration successful!");
        setNewUser({
          username: "",
          email: "",
          password: "",
          role: "admin", // Default to 'admin' after successful registration
          first_name: "",
          middle_name: "",
          last_name: "",
          school_name: "",
        });
        setError("");
      } else {
        setError(data.error || "Failed to register.");
      }
    } catch (error) {
      setError("An error occurred. Please try again.");
      console.error("Registration error:", error);
    }
  };
  

  return (
    <div className="modalOverlay" ref={modalRef}>
      <section className="toggleBtn">
        <button
          className={`signInBtn ${activeSection === "login" ? "active" : ""}`}
          onClick={() => handleButtonClick("login")}
        >
          Sign In
        </button>
        <button
          className={`createAcc ${activeSection === "createAcc" ? "active" : ""}`}
          onClick={() => handleButtonClick("createAcc")}
        >
          Create Account
        </button>
      </section>

      <section className="frmContainer">
        <form
          onSubmit={
            activeSection === "login" ? handleLoginSubmit : handleRegisterSubmit
          }
        >
          <section 
          className={`login ${activeSection === "login" ? "show" : ""}`}>
           <p>
            {error && <p className="error">{error}</p>}
           </p>
            <section className="row">
              <div className="row-items" style={{ width: "49%", margin: "5px auto" }}>
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  name="username"
                  value={credentials.username} 
                  placeholder="Username"
                  onChange={(e) =>
                    setCredentials({ ...credentials, username: e.target.value })
                  }
                />
              </div>
            </section>
            
            <section className="row">
              <div className="row-items" style={{ width: "49%", margin: "5px auto" }}>
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  name="password"
                  value={credentials.password}
                  placeholder="Password"
                  onChange={(e) =>
                    setCredentials({ ...credentials, password: e.target.value })
                  }
                />
              </div>
              
            </section>

            <section className="row">
              <div className="row-items" style={{ width: "49%", margin: "0 auto" }}>
              <button type="submit">Login</button>
              </div>
            </section>
           
          </section>

          <section
            className={`createNewAcc ${
              activeSection === "createAcc" ? "show" : ""
            }`}
          >
            <UserRegistrationForm
              newUser={newUser}
              setNewUser={setNewUser}
              error={error}
            />
             <button type="submit">Create Account</button>
          </section>

        </form>
      </section>
    </div>
  );
}

export default LoginSignup;
