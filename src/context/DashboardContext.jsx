import { createContext, useState, useEffect, useContext } from 'react';
import localdata from './localData';// Adjust the import path based on your folder structure

// Create a context for the dashboard data
const DashboardContext = createContext();

// Provider component
export const DashboardProvider = ({ children }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Simulate fetching data
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Simulate a delay to mimic an API call
        await new Promise((resolve) => setTimeout(resolve, 500));
        setData(localdata); // Use the imported local data
      } catch (err) {
        setError('Failed to load local data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <DashboardContext.Provider value={{ data, loading, error }}>
      {children}
    </DashboardContext.Provider>
  );
};

// Custom hook to use the context
export const useDashboardData = () => {
  return useContext(DashboardContext);
};
