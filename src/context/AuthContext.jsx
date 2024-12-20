import { createContext, useState, useEffect } from "react";

// Create context for authentication
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(localStorage.getItem("access_token"));  // Get token from localStorage

   
    useEffect(() => {
      if (accessToken) {  
        const userFromToken = localStorage.getItem("user"); 
        setUser(userFromToken ? JSON.parse(userFromToken) : null);
      } else {
        setUser(null);
      }
    }, [accessToken]);
    
  // Store token in state and localStorage
  const login = (username, role, token) => {
    const userDetails = { username, role };
    setUser(userDetails);
    setAccessToken(token);  // Store the token

    // Store the token and user details in localStorage
    localStorage.setItem("access_token", token);
    localStorage.setItem("user", JSON.stringify(userDetails));  // Storing user details
  };


  // Logout function
  const logout = () => {
    setUser(null);
    setAccessToken(null);
    localStorage.removeItem("access_token");  // Remove token on logout
    localStorage.removeItem("user");  // Remove user details
  };
  

  // Register function
  const register = (username, email, password, role, first_name, middle_name, last_name) => {
    console.log("User registered:", {
      username,
      email,
      password,
      role,
      first_name,
      middle_name,
      last_name,
    });
  };

  // Ensure token is updated when the accessToken state changes
  useEffect(() => {
    if (accessToken) {
      localStorage.setItem("access_token", accessToken);
    }
  }, [accessToken]);

  const refreshToken = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/refresh-token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: storedRefreshToken }),
      });
  
      if (response.ok) {
        const result = await response.json();
        // Update the accessToken state with the new token
        setAccessToken(result.access_token);
        return result.access_token;
      } else {
        throw new Error('Failed to refresh token');
      }
    } catch (err) {
      console.error('Token refresh error:', err);
      setError('Failed to refresh token. Please log in again.');
      // Optionally log out user or redirect to login page
    }
  };

  return (
    <AuthContext.Provider value={{ refreshToken, user, login, register, logout, accessToken }}>
      {children}
    </AuthContext.Provider>
  );
};
