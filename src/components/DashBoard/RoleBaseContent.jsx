import React, { useContext } from 'react';
import { AuthContext } from '../../context/AuthContext'; // Assuming the context is used to store user data
import Card from "./Card";
import { useDashboardData } from '../../context/DashboardContext';

const RoleBasedContent = () => {
const { user } = useContext(AuthContext); // Getting user data from context
const { data, loading, error } = useDashboardData(); 
if (loading) return <p>Loading dashboard data...</p>;
if (error) return <p>Error loading data: {error}</p>;

// Protect against undefined data
if (!data || !data.courses) {
  console.log("Dashboard data is missing or incomplete:", data);
  return <p>Dashboard data unavailable.</p>;
}

const { totalCourses = 0, totalStudents = 0, attendance = {}, courses = [] } = data;

  if (!user || !user.role) {
    return <p>Loading...</p>;  
  }

  switch (user.role) {
    case 'admin':
      return (
        <div>
          <h1>Admin Dashboard</h1>
          <p>Welcome, {user.username}. You can manage the system here.</p>
          {/* Add additional admin-specific content */}
        </div>
      );
    
    case 'teacher':
      return (
        <section>
          <section className="col-1">
            <div className="colItems itemspad">
              <Card title="Total Courses" value={totalCourses} />
            </div>
            <div className="colItems itemspad">
              <Card title="Total Students" value={totalStudents} />
            </div>
            <div className="colItems present">
              <Card title="Present" value={attendance.present || 0} />
            </div>
            <div className="colItems absent">
              <Card title="Absent" value={attendance.absent || 0} />
            </div>
            <div className="colItems excuse">
              <Card title="Excused" value={attendance.excused || 0} />
            </div>
          </section>
          <section className="col-1">
            {courses.map((course) => (
              <div className="colItems" key={course.id}>
                <Card title={course.name} value={course.studentCount || 0} />
              </div>
            ))}
          </section>
          <section className="graphholder"></section> 

      </section>
      );
    
    case 'student':
      return (
        <div>
          <h1>Student Dashboard</h1>
          <p>Welcome, {user.username}. You can view your courses and attendance status.</p>
          {/* Add additional student-specific content */}
        </div>
      );
    
    default:
      return <p>Role not recognized. Please contact support.</p>; // Handle unexpected roles
  }
};

export default RoleBasedContent;
