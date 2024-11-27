// src/components/LoginSignup.js
import { useEffect, useRef, useState, useContext } from 'react';
import './LoginSignup.css';
import { AuthContext } from '../../context/AuthContext';

function LoginSignup({ onClose }) {
  const modalRef = useRef(null);

  // Close the modal when clicking outside of the modal (outside the overlay and content)
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (modalRef.current && !modalRef.current.contains(e.target)) {
        onClose();
      }
    };
    document.addEventListener('mousedown', handleClickOutside); // Add event listener to document
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);  // Cleanup event listener on unmount
    };
  }, [onClose]);

  const [activeSection, setActiveSection] = useState('login'); // 'login' or 'createAcc'

  const handleButtonClick = (section) => {
    setActiveSection(section);
    setError(""); // Clear the error when switching tabs
    if (section === 'createAcc') {
      // Reset the new user form if switching to 'createAcc'
      setNewUser({
        username: "",
        email: "",
        password: "",
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
    role: "student",
    first_name: "",
    middle_name: "",
    last_name: "",
  });
  const [error, setError] = useState("");

  const handleLoginSubmit = (e) => {
    e.preventDefault();
    if (credentials.username === "admin" && credentials.password === "password") {
      login(credentials.username, "admin");
      alert("Login successful!");
    } else {
      setError("Invalid credentials");
    }
  };

  const handleRegisterSubmit = (e) => {
    e.preventDefault();
    if (
      !newUser.username ||
      !newUser.email ||
      !newUser.password ||
      !newUser.first_name ||
      !newUser.last_name
    ) {
      setError("Please fill in all required fields.");
      return;
    }
    // Register the user
    register(newUser.username, newUser.email, newUser.password, newUser.role, newUser.first_name, newUser.middle_name, newUser.last_name);
    setNewUser({
      username: "",
      email: "",
      password: "",
      role: "student",
      first_name: "",
      middle_name: "",
      last_name: "",
    }); // Reset form
    setError("");
  };

  return (
    <div className="modalOverlay" ref={modalRef}>
      <section className='toggleBtn'>
        <button
          className={`signInBtn ${activeSection === 'login' ? 'active' : ''}`}
          onClick={() => handleButtonClick('login')}
        >
          Sign In
        </button>
        <button
          className={`createAcc ${activeSection === 'createAcc' ? 'active' : ''}`}
          onClick={() => handleButtonClick('createAcc')}
        >
          Create Account
        </button>
      </section>
      
      <section className='frmContainer'>
        <form onSubmit={activeSection === 'login' ? handleLoginSubmit : handleRegisterSubmit}>
          <section className={`login ${activeSection === 'login' ? 'show' : ''}`}>
            <p>
              {error && <p className="error">{error}</p>}
            </p>
            <label htmlFor="username">Username</label>
            <input
              type="text"
              name="username"
              placeholder="Username"
              onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
            />
             <label htmlFor="password">Password</label>
            <input
              type="password"
              name="password"
              placeholder="Password"
              onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
            />
            <button type="submit">Login</button>
          </section>
          
          <section className={`createNewAcc ${activeSection === 'createAcc' ? 'show' : ''}`}>
            <p>
            {error && <p className="error">{error}</p>}
            </p>
            <section className='row'>
              <div className='row-items'>
              <label htmlFor="first_name">First Name</label>
              <input
                type="text"
                name="first_name"
                placeholder="First Name"
                value={newUser.first_name}
                onChange={(e) => setNewUser({ ...newUser, first_name: e.target.value })}
              />
              </div>
              <div className='row-items'>
                <label htmlFor="middle_name">Middle Name</label>
                <input
                  type="text"
                  name="middle_name"
                  placeholder="Middle Name (Optional)"
                  value={newUser.middle_name}
                  onChange={(e) => setNewUser({ ...newUser, middle_name: e.target.value })}
                />
              </div>
              <div className='row-items'>
                <label htmlFor="last_name">Last Name</label>
                <input
                type="text"
                name="last_name"
                placeholder="Last Name"
                value={newUser.last_name}
                onChange={(e) => setNewUser({ ...newUser, last_name: e.target.value })}
              />
              </div>
            </section>

            <section className='row' >
              <div className='row-items' style={{ width: "49%" }}>
                <label htmlFor="role">Role</label>
                <select
                    name="role"
                    value={newUser.role}
                    onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                  >
                    <option value="student">Student</option>
                    <option value="teacher">Teacher</option>
                    <option value="admin">Admin</option>
                </select>
              </div>
              <div className='row-items' style={{ width: "49%" }}>
                <label htmlFor="email">Email</label>
                <input
                type="email"
                name="email"
                placeholder="Email"
                value={newUser.email}
                onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                />
              </div>
              
            </section>
            
           <div className='row'>
            <div className='row-items'  style={{ width: "49%" }}>
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  name="username"
                  placeholder="Username"
                  value={newUser.username}
                  onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                />
            
            </div>
            <div className='row-items'  style={{ width: "49%" }}>
              <label htmlFor="password">Password</label>
                <input
                  type="password"
                  name="password"
                  placeholder="Password"
                  value={newUser.password}
                  onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                />
            </div>
           </div>
            
            <button type="submit">Create Account</button>
          </section>
        </form>
      </section>
    </div>
  );
}

export default LoginSignup;
