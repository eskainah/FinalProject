import React, { useState,useContext, useEffect } from "react";
import { AuthContext } from "../../context/AuthContext";
import  ApiContext  from "../../context/ApiContext";
import Card from "./Card";
import { Link, useNavigate, useParams} from "react-router-dom";
import Attendance from "./Attendance";

//import RoleBasedContent from "./RoleBaseContent";

const Dashboard = () => {
  
  const group = "/group.png";
  const book = "/book.png";
  const absent = "/absent.png";
  const classroom = "/nature.png";
  const hand = "/hand.png";

  const { user, logout } = useContext(AuthContext);
  const { data, loading, error } = useContext(ApiContext);

  const navigate = useNavigate(); // Used for navigation on link click
  const { courseName } = useParams();

  const [selectedCourse, setSelectedCourse] = useState(null);

  useEffect(() => {
    if (courseName) {
      setSelectedCourse(courseName);
    } else {
      setSelectedCourse(null); // Reset if no courseName
    }
  }, [courseName]);

  const handleCourseChange = (e) => {
    setSelectedCourse(e.target.value);
    navigate(`/course/${e.target.value}`);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  const { total_courses = 0, total_students = 0, attendance = {}, courses = [] } = data;
  
  const handleCourseClick = (courseName) => {
    navigate(`/course/${courseName}`); // Navigate to the attendance route
  };

  return (
    <div className="dashboard-container">
    
      <section className="dashboard-header">
        <div className="logoImg"></div>
          {/* display a dropdown list in the header when the attendance component is active  */}
        {courseName && (
          <div className="course-selector">
            <select
              id="course-select"
              onChange={handleCourseChange}
              value={selectedCourse || ""}
            >
              {courses.map((course) => (
                <option key={course.course_name} value={course.course_name}>
                  {course.course_name}
                </option>
              ))}
            </select>
          </div>
        )}
        <div className="profile">
          <div className="profile_img">
          </div>
          <div className="user-info">
            <h4>{user.username}</h4> {/* Display username */}
            <p><strong>{user.role}</strong></p> {/* Display role */}
          </div>
        </div>
      </section>
      <div className="main-section">
      
      <section className="dashboard-nav">
        <button>Hello</button>
      </section>

      <section className="dashboard-main">
      {courseName ? (
            <Attendance selectedCourse={selectedCourse} />
          ) : (
         <div className="teacher-main-dashboard">
         <section className="col-1">
            <div className="colItems itemspad">
                 <Card cornerElement={book} title="Total Courses" value={total_courses} /> 
            </div>
            <div className="colItems itemspad">
              <Card cornerElement={group} title="Total Students" value={total_students} /> 
            </div>
            <div className="colItems present">
              <Card cornerElement={classroom} title="Present" value={attendance.present || 0} />
            </div>
            <div className="colItems absent">
               <Card cornerElement={absent} title="Absent" value={attendance.absent || 0} /> 
            </div>
            <div className="colItems excuse">
              <Card cornerElement={hand} title="Excused" value={attendance.excused || 0} /> 
            </div>
            <div className="colItems excuse">
               
            </div>
          </section>
          <section className="col-1 "> 
            {courses.length > 0 ? (
                  courses.map((course) => (
                <div className="colItems" key={course.course_name}>
                  <Link to={`/course/${course.course_name}`} 
                  onClick={() => handleCourseClick(course.course_name)} 
                  className="course-link">
                   
                      <Card 
                        cornerElement={group} 
                        title={course.course_name} 
                        value={`${course.student_count}`} 
                      />
                  </Link>
                </div>
              ))
            ) : (
              <p>No courses assigned</p>
            )}
          </section>
           
          <section className="graphholder">
          </section>
       
         </div>
          )}
      </section>
      
      </div>
    </div>
  );
};


export default Dashboard;
