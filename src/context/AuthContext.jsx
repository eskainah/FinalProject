import { createContext, useState } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = (username, role) => {
    const userDetails = { username, role };
    console.log("Logging in user:", userDetails); // Debug log
    setUser(userDetails);
  };

  const register = (
    username,
    email,
    password,
    role,
    first_name,
    middle_name,
    last_name
  ) => {
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

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};


  

