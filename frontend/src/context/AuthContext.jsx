import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [userId, setUserId] = useState(localStorage.getItem('currentUserId'));

  const login = (id) => {
    localStorage.setItem('currentUserId', id);
    setUserId(id);
  };

  const logout = () => {
    localStorage.removeItem('currentUserId');
    setUserId(null);
  };

  return (
    <AuthContext.Provider value={{ userId, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
