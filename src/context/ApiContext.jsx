import React, { createContext, useState, useEffect, useContext } from 'react';
import { AuthContext } from './AuthContext';  // Import AuthContext

// Create context for API data
const ApiContext = createContext();

// API Provider component
export const ApiProvider = ({ children }) => {
  const { accessToken } = useContext(AuthContext);  // Access the token from AuthContext
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!accessToken) {
        setError('No authentication token found');
        setLoading(false);
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:8000/api/courses/teacher_courses/', {
          method: 'GET',
          headers: {
            'Authorization': `Token ${accessToken}`,  // Use the token with 'Token' prefix (since you're using DRF token authentication)
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }

        const result = await response.json();
        setData(result);  // Set the API response data
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [accessToken]);  // Re-run if accessToken changes

  return (
    <ApiContext.Provider value={{ data, loading, error }}>
      {children}
    </ApiContext.Provider>
  );
};

export default ApiContext;
