import { createContext, useState } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = (username, role) => {
    setUser({ username, role });
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
