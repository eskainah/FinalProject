import React, { useContext, useState, useEffect } from "react";
import { AuthContext } from "../../context/AuthContext";
import ApiContext from "../../context/ApiContext";
import { Routes, Route, useNavigate, useLocation } from "react-router-dom";
import NavBar from "./NavBar";
import './dashboard.css';

import TeacherMainDashboard from "./TeacherDashboard/TeacherMainDashboard";
import StudentMainDashboard from "./StudentDashboard/StudentMainDashboard";
import AdminMainDashboard from "./AdminDashboard/AdminMainDashboard";

import TeacherAttendanceOverview from "./TeacherDashboard/TeacherAttendanceOverView";
import StudentAttendanceOverview from "./StudentDashboard/StudentAttendanceOvervoew";
import AdminAttendanceOverview from "./AdminDashboard/AdminAttendanceOverview";

import Attendance from "./Attendance";

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();
  const { data } = useContext(ApiContext);
  const courses = data?.courses || [];

  const [selectedCourse, setSelectedCourse] = useState("");

  useEffect(() => {
    if (courses.length > 0) {
      setSelectedCourse(courses[0].course_name);
    }
  }, [courses]);

  const shouldShowSelect =
  location.pathname.includes("attendance-overview") ||
  location.pathname.includes("course");

  const handleCourseChange = (event) => {
    const courseName = event.target.value;
    setSelectedCourse(courseName);
    if (location.pathname.includes("attendance-overview")) {
      navigate(`/attendance-overview/`);
    } else {
      navigate(`/course/${courseName}`);
    }
  };

  const openAttendance = () => {
    if (courses.length > 0) {
      setSelectedCourse(courses[0].course_name); // Set the selected course to the first one
      navigate(`/course/${courses[0].course_name}`); // Navigate to the attendance page for that course
    }
  };

  const renderDashboard = () => {
    switch (user.role) {
      case "teacher":
        return <TeacherMainDashboard />;
      case "student":
        return <StudentMainDashboard />;
      case "admin":
        return <AdminMainDashboard />;
      default:
        return <div>Unauthorized Access</div>;
    }
  };



  if (!data) {
    return <p>Loading...</p>;
  }
  return (
    <div className="dashboard-container">
      
      <section className="dashboard-header">
        <div className="logoImg"></div>

        <div className="courseList">
          {user.role === "teacher" && shouldShowSelect && courses.length > 0 && (
            <select
              value={selectedCourse}
              onChange={handleCourseChange}
              onFocus={(e) => { e.target.style.border = "1px solid rgb(192, 190, 190);"}}
            >
              {courses.map((course) => (
                <option key={course.course_name} value={course.course_name}>
                  {course.course_name}
                </option>
              ))}
            </select>
        )}
        </div>

        <div className="profile">
          <div className="profile_img"></div>
          <div className="user-info">
            <h4>{user.username}</h4>
            <p><strong>{user.role}</strong></p>
          </div>
        </div>
      </section>

      <div className="main-section">
        <section className="dashboard-nav">
          <NavBar
            handleAttendanceOverviewClick={() => {
              navigate("/attendance-overview");

            }}
            goToDashboard={() => {
              navigate("/");
            }}
            openAttendance={openAttendance}
          />
        </section>

        <section className="dashboard-main">
          <Routes>
            {/* Main dashboard */}
            <Route path="/" element={renderDashboard()} />

            {/* Attendance overview */}
            {user.role === "teacher" && (
              <Route path="/attendance-overview" element={<TeacherAttendanceOverview  selectedCourse={selectedCourse}/>} />
            )}
            {user.role === "student" && (
              <Route path="/attendance-overview" element={<StudentAttendanceOverview />} />
            )}
            {user.role === "admin" && (
              <Route path="/attendance-overview" element={<AdminAttendanceOverview />} />
            )}

            {/* Course-specific page */}
            <Route
              path="/course/:courseName"
              element={<Attendance />}
            />
          </Routes>
        </section>
      </div>

    </div>
  );
};

export default Dashboard;
