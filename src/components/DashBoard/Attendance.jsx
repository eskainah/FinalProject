import React, { useContext, useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import ApiContext from "../../context/ApiContext";
import Card from "./Card";
import ProfileCard from "../ProfileCards/ProfileCard";

const Attendance = () => {
  const { courseName } = useParams();
  const { data, loading, error } = useContext(ApiContext);
  const [course, setCourse] = useState(null);
  const group = "/group.png";
  const book = "/book.png";
  const absent = "/absent.png";
  const classroom = "/nature.png";
  const hand = "/hand.png";

  // UseEffect to set the course once data is loaded
  useEffect(() => {
    if (data && data.courses) {
      const foundCourse = data.courses.find(course => course.course_name === courseName);
      setCourse(foundCourse); // Update state with the found course
    }
  }, [data, courseName]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  if (!course) {
    return <div>Course not found.</div>;
  }


  const students = [
    {
      name: 'John Doe',
      std_ID: 'S1234567',
      photo: 'https://via.placeholder.com/60',
    },
    {
      name: 'Konah Doe',
      std_ID: 'S7654321',
      photo: 'https://via.placeholder.com/60',
    },
    {
      name: 'Blama Doe',
      std_ID: 'S7654321',
      photo: 'https://via.placeholder.com/60',
    },
    {
      name: 'John Doe',
      std_ID: 'S1234567',
      photo: 'https://via.placeholder.com/60',
    },
    {
      name: 'Konah Doe',
      std_ID: 'S7654321',
      photo: 'https://via.placeholder.com/60',
    },
    {
      name: 'Blama Doe',
      std_ID: 'S7654321',
      photo: 'https://via.placeholder.com/60',
    },
    {
      name: 'John Doe',
      std_ID: 'S1234567',
      photo: 'https://via.placeholder.com/60',
    },
    {
      name: 'Konah Doe',
      std_ID: 'S7654321',
      photo: 'https://via.placeholder.com/60',
    },
    {
      name: 'Blama Doe',
      std_ID: 'S7654321',
      photo: 'https://via.placeholder.com/60',
    },
    {
      name: 'Konah Doe',
      std_ID: 'S7654321',
      photo: 'https://via.placeholder.com/60',
    },

    {
      name: 'Edwin Saah Kainah',
      std_ID: 'S7654321',
      photo: 'https://via.placeholder.com/60',
    },
    // Add more students as needed
  ];

 
  return (
    <div>
      <section className="col-1">
        <div className="colItems">
          <Card 
          cornerElement={group} 
          title={course.course_name} 
          value={`${course.student_count}`}
        />
        </div>

        <div className="colItems present">
              <Card cornerElement={classroom} title="Present" value={ 0} />
            </div>
            <div className="colItems absent">
               <Card cornerElement={absent} title="Absent" value={ 0} /> 
            </div>
            <div className="colItems excuse">
              <Card cornerElement={hand} title="Excused" value={ 0} /> 
            </div>
      </section>
     <section className="profiles">
        <div className="student-list">
          {students.map((student, index) => (
            <ProfileCard key={index} student={student} />
          ))}
        </div>
     </section>
    </div>
  );
};

export default Attendance;
