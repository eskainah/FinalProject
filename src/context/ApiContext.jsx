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
  
  const [attendanceSummary, setAttendanceSummary] = useState([]);
  const [totalPresentPercentage, setTotalPresentPercentage] = useState(0);
  const [totalAbsentPercentage, setTotalAbsentPercentage] = useState(0);
  const [totalExcusedPercentage, setTotalExcusedPercentage] = useState(0);
  
  const [dailyPresentPercentage, setDailyPresentPercentage] = useState(0);
  const [dailyAbsentPercentage, setDailyAbsentPercentage] = useState(0);
  const [dailyExcusedPercentage, setDailyExcusedPercentage] = useState(0);

  const [weeklyPresentPercentage, setWeeklyPresentPercentage] = useState(0);
  const [weeklyAbsentPercentage, setWeeklyAbsentPercentage] = useState(0);
  const [weeklyExcusedPercentage, setWeeklyExcusedPercentage] = useState(0);

  const [monthlyPresentPercentage, setMonthlyPresentPercentage] = useState(0);
  const [monthlyAbsentPercentage, setMonthlyAbsentPercentage] = useState(0);
  const [monthlyExcusedPercentage, setMonthlyExcusedPercentage] = useState(0);

  // Function to fetch course data for the teacher
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
          'Authorization': `Token ${accessToken}`,  // Use the token with 'Token' prefix
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

  // Function to fetch enrolled students for a specific course
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

  // Function to fetch attendance summary data
const fetchAttendanceSummary = async () => {
  if (!accessToken) {
    setError('No authentication token found');
    setLoading(false);
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/attendance/attendance-summary/', {
      method: 'GET',
      headers: {
        Authorization: `Token ${accessToken}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch attendance summary');
    }

    const result = await response.json();
    setAttendanceSummary(result.attendance_summary); // Store attendance summary data
    setTotalPresentPercentage(result.total_present_percentage); // Set summary percentages
    setTotalAbsentPercentage(result.total_absent_percentage);
    setTotalExcusedPercentage(result.total_excused_percentage);
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};

// Function to fetch attendance trends data
const fetchAttendanceTrends = async () => {
  if (!accessToken) {
    setError('No authentication token found');
    setLoading(false);
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/attendance/attendance-trends/', {
      method: 'GET',
      headers: {
        Authorization: `Token ${accessToken}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch attendance trends');
    }

    const result = await response.json();

    // Set daily percentages
    setDailyPresentPercentage(result.daily_present_percentage);
    setDailyAbsentPercentage(result.daily_absent_percentage);
    setDailyExcusedPercentage(result.daily_excused_percentage);

    // Set weekly percentages
    setWeeklyPresentPercentage(result.weekly_present_percentage);
    setWeeklyAbsentPercentage(result.weekly_absent_percentage);
    setWeeklyExcusedPercentage(result.weekly_excused_percentage);

    // Set monthly percentages
    setMonthlyPresentPercentage(result.monthly_present_percentage);
    setMonthlyAbsentPercentage(result.monthly_absent_percentage);
    setMonthlyExcusedPercentage(result.monthly_excused_percentage);
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};

// Use `useEffect` to fetch data when the component loads
useEffect(() => {
  fetchData();
  if (accessToken) {
    console.log("Fetching attendance summary...");
   
    fetchAttendanceSummary();
    fetchAttendanceTrends();
  }
}, [accessToken]);
 
  return (
    <ApiContext.Provider value={{
      data,
      enrolledStudents,
      loading,
      error,
      fetchEnrolledStudents,  // This will be called manually when needed
      fetchingStudents,
      fetchError,
      upsertAttendance,
      savingAttendance,
      saveError,
      attendanceSummary,
       fetchAttendanceSummary,
      totalPresentPercentage,
      totalAbsentPercentage,
      totalExcusedPercentage,
      dailyPresentPercentage,
      dailyAbsentPercentage,
      dailyExcusedPercentage,
      weeklyPresentPercentage,
      weeklyAbsentPercentage,
      weeklyExcusedPercentage,
      monthlyPresentPercentage,
      monthlyAbsentPercentage,
      monthlyExcusedPercentage,
    }}>
      {children}
    </ApiContext.Provider>
  );
};

export default ApiContext;
