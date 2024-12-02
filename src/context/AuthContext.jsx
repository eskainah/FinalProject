import { createContext, useState, useEffect } from "react";

// Create context for authentication
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(localStorage.getItem("access_token"));  // Get token from localStorage

  // Store token in state and localStorage
  const login = (username, role, token) => {
    const userDetails = { username, role };
    setUser(userDetails);
    setAccessToken(token);  // Store the token

    // Store the token in localStorage
    localStorage.setItem("access_token", token);
  };

  // Logout function
  const logout = () => {
    setUser(null);
    setAccessToken(null);
    localStorage.removeItem("access_token");  // Remove token on logout
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

  return (
    <AuthContext.Provider value={{ user, login, register, logout, accessToken }}>
      {children}
    </AuthContext.Provider>
  );
};
