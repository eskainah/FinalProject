import React, { createContext, useState, useEffect, useContext } from 'react';
import { AuthContext } from './AuthContext';  // Import AuthContext

// Create context for API data
const ApiContext = createContext();

// API Provider component
export const ApiProvider = ({ children }) => {
  const { accessToken } = useContext(AuthContext);  // Access the token from AuthContext
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [enrolledStudents, setEnrolledStudents] = useState([]);
  const [error, setError] = useState(null);
  const [fetchingStudents, setFetchingStudents] = useState(false);  // To track if students are being fetched
  const [fetchError, setFetchError] = useState(null);  // For student fetch errors
  const [savingAttendance, setSavingAttendance] = useState(false);  // Track saving state
  const [saveError, setSaveError] = useState(null);  // Track save error

  // Fetch course data for the teacher
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
          throw new Error('Failed to fetch course data');
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

  // Fetch enrolled students for a specific course
  const fetchEnrolledStudents = async (courseCode) => {
    if (!accessToken) {
      setFetchError('No authentication token found');
      setFetchingStudents(false);
      return;
    }

    setFetchingStudents(true);  // Set fetching to true
    setFetchError(null);  // Reset fetch error

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/courses/${courseCode}/enrolled_students/`, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch enrolled students');
      }

      const students = await response.json();

      const formattedStudents = students.enrolled_students.map(student => ({
        name: student.student_name, // Combine first and last name
        std_ID: student.student_id, // Map student ID
        photo: student.photo || 'https://via.placeholder.com/60', // Default photo if none provided
      }));

      setEnrolledStudents(formattedStudents); // Store the enrolled students data
    } catch (err) {
      setFetchError(err.message);  // Set fetch error message
    } finally {
      setFetchingStudents(false);  // Set fetching to false once done
    }
  };

  // Function to upsert attendance data
  const upsertAttendance = async (attendanceData) => {
    if (!accessToken) {
      setSaveError("No authentication token found");
      setSavingAttendance(false);
      return false; // Indicate failure
    }
  
    setSavingAttendance(true); // Set saving to true
    setSaveError(null); // Reset save error
  
    try {
      const response = await fetch("http://127.0.0.1:8000/api/attendance/upsert-attendance/", {
        method: "POST",
        headers: {
          Authorization: `Token ${accessToken}`, // Use token in the headers
          "Content-Type": "application/json",
        },
        body: JSON.stringify(attendanceData), // Send the attendance data
      });
  
      if (!response.ok) {
        throw new Error("Failed to save attendance");
      }
  
      const result = await response.json();
      console.log("Attendance response:", result);
  
      // Return whether attendance was updated or created
      return result.message.includes("updated") ? true : false;
    } catch (err) {
      setSaveError(err.message); // Set save error message
      return false; // Indicate failure
    } finally {
      setSavingAttendance(false); // Set saving to false once done
    }
  };
  

  return (
    <ApiContext.Provider value={{
      data,
      enrolledStudents,
      loading,
      error,
      fetchEnrolledStudents,
      fetchingStudents,
      fetchError,
      upsertAttendance,  // Provide the upsertAttendance function
      savingAttendance,
      saveError,
    }}>
      {children}
    </ApiContext.Provider>
  );
};

export default ApiContext;
