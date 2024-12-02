import React, { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import  ApiContext  from "../../context/ApiContext";
import Card from "./Card";
//import RoleBasedContent from "./RoleBaseContent";

const Dashboard = () => {
  
  const group = "/group.png";
  const book = "/book.png"

  const { user, logout } = useContext(AuthContext);
  const { data, loading, error } = useContext(ApiContext);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  //if (data) return <div>{JSON.stringify(data)}</div>;

  const { total_courses = 0, total_students = 0, attendance = {}, courses = [] } = data;
  return (
    <div className="dashboard-container">
      {/* Dashboard UI */}
      <section className="dashboard-header">
        <div className="logoImg"></div>

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
          <section className="col-1">
            <div className="colItems itemspad">
                 <Card cornerElement={book} title="Total Courses" value={total_courses} /> 
            </div>
            <div className="colItems itemspad">
              <Card cornerElement={group} title="Total Students" value={total_students} /> 
            </div>
            <div className="colItems present">
              {/* <Card title="Present" value={attendance.present || 0} /> */}
            </div>
            <div className="colItems absent">
              {/* <Card title="Absent" value={attendance.absent || 0} /> */}
            </div>
            <div className="colItems excuse">
              {/* <Card title="Excused" value={attendance.excused || 0} /> */}
            </div>
          </section>
          <section className="col-1 "> 
            {courses.length > 0 ? (
                  courses.map((course) => (
                <div className="colItems" key={course.course_name}>
                  <Card  cornerElement={group} title={course.course_name} value={`${course.student_count}`}/>
                </div>
              ))
            ) : (
              <p>No courses assigned</p>
            )}
          </section>

          <section className="graphholder">

          </section>
      </section>
      
      </div>
    </div>
  );
};


export default Dashboard;
