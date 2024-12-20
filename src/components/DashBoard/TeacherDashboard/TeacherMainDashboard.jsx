import {React, useContext, useState, useEffect} from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import ApiContext from '../../../context/ApiContext';

import MyCalendar from '../../Calender/Calendar';
import Card from '../Card';
import Attendance from '../Attendance';
import AttendanceLineGraph from '../../Visualization/AttendanceLineGraph';
import AttendancePieCharts from '../../Visualization/AttendancePieChart';

const TeacherMainDashboard = () =>{
  const group = "/group.png";
  const book = "/book.png";
  const absent = "/absent.png";
  const classroom = "/nature.png";
  const hand = "/hand.png";

  const { data, loading, error, totalPresentPercentage, totalAbsentPercentage, totalExcusedPercentage } = useContext(ApiContext);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const { courseName } = useParams();
  const navigate = useNavigate(); 

 
  useEffect(() => {
    if (courseName) {
      setSelectedCourse(courseName);
      } else {
        setSelectedCourse(null); // Reset if no courseName
      }
  }, [courseName]);
        
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
        
  const { total_courses = 0, total_students = 0, attendance = {}, courses = [] } = data;
          
  const handleCourseClick = (courseName) => {
    navigate(`/course/${courseName}`); // Navigate to the attendance route
  };
        
  return courseName ? (
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
          <Card cornerElement={classroom} title="Present" value={`${Math.round(totalPresentPercentage)}%`} />
        </div>
        <div className="colItems absent">
          <Card cornerElement={absent} title="Absent" value={`${Math.round(totalAbsentPercentage)}%`} />
        </div>
        <div className="colItems excuse">
          <Card cornerElement={hand} title="Excused" value={`${Math.round(totalExcusedPercentage)}%`} />
        </div>
      </section>
      <section className="col-1">
        {courses.length > 0 ? (
          courses.map((course) => (
            <div className="colItems" key={course.course_name}>
              <Link
                to={`/course/${course.course_name}`}
                onClick={() => handleCourseClick(course.course_name)}
                className="course-link"
              >
                <Card cornerElement={group} title={course.course_name} value={`${course.student_count}`} />
              </Link>
            </div>
          ))
        ) : (
          <p>No courses assigned</p>
        )}
      </section>
      <section className="graphholder">
        <section className="dateLine">
          <section className="line">
            <AttendanceLineGraph />
          </section>
          <section className="date">
            <MyCalendar />
          </section>
        </section>
        <section className="Pie">
          <AttendancePieCharts />
        </section>
        
      </section>

        </div>
  );
};

export default TeacherMainDashboard;
