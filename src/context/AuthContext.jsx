// src/context/AuthContext.js
import React, { createContext, useState } from "react";

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [users, setUsers] = useState([]); // Store registered users

  const login = (username, role) => {
    setUser({ username, role });
  };

  const logout = () => {
    setUser(null);
  };

  const register = (username, email, password, role, first_name, middle_name, last_name) => {
    const newUser = { username, email, password, role, first_name, middle_name, last_name };
    setUsers([...users, newUser]); // Add new user to the users array
    alert("Registration successful!");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
