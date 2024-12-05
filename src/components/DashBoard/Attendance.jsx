import React, { useContext, useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import ApiContext from "../../context/ApiContext";
import Card from "./Card";
import ProfileCard from "../ProfileCards/ProfileCard";
import Notification from "../PopUpNotification/Popup";

const Attendance = () => {
  const [notification, setNotification] = useState({ message: "", type: "", show: false });
  const { courseName } = useParams();
  const {
    data,
    loading,
    error,
    fetchEnrolledStudents,
    enrolledStudents,
    fetchingStudents,
    fetchError,
    upsertAttendance,
  } = useContext(ApiContext);

  const [course, setCourse] = useState(null);
  const [courseAttendance, setCourseAttendance] = useState({});
  const [currentCourseCode, setCurrentCourseCode] = useState("");
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState(null);
  const [changesMade, setChangesMade] = useState(false); // Track if changes are made

  const group = "/group.png";
  const absent = "/absent.png";
  const classroom = "/nature.png";
  const hand = "/hand.png";

  useEffect(() => {
    if (data?.courses) {
      const foundCourse = data.courses.find((course) => course.course_name === courseName);
      if (foundCourse && (!course || foundCourse.course_code !== currentCourseCode)) {
        // Save current course attendance before switching
        if (currentCourseCode) {
          setCourseAttendance((prev) => ({
            ...prev,
            [currentCourseCode]: prev[currentCourseCode] || {
              statusCounts: { Present: 0, Absent: 0, Excused: 0 },
              statuses: {},
            },
          }));
        }

        setCourse(foundCourse);
        setCurrentCourseCode(foundCourse.course_code);
        fetchEnrolledStudents(foundCourse.course_code);
      }
    }
  }, [data, courseName, fetchEnrolledStudents, currentCourseCode, course]);

  const currentCourseAttendance =
    courseAttendance[currentCourseCode] || {
      statusCounts: { Present: 0, Absent: 0, Excused: 0 },
      statuses: {},
    };

  const handleStatusChange = (studentId, oldStatus, newStatus) => {
    setCourseAttendance((prev) => {
      const updatedAttendance = { ...prev };
      const courseData = updatedAttendance[currentCourseCode] || {
        statusCounts: { Present: 0, Absent: 0, Excused: 0 },
        statuses: {},
      };

      const updatedCounts = { ...courseData.statusCounts };
      if (oldStatus) updatedCounts[oldStatus]--;
      if (newStatus) updatedCounts[newStatus]++;

      const updatedStatuses = { ...courseData.statuses, [studentId]: newStatus };

      updatedAttendance[currentCourseCode] = {
        statusCounts: updatedCounts,
        statuses: updatedStatuses,
      };

      setChangesMade(true); // Mark changes as made
      return updatedAttendance;
    });
  };

  const handleSaveAttendance = async () => {
    setSaving(true);
    setSaveError(null);
  
    const studentsData = enrolledStudents.map((student) => ({
      student_id: student.std_ID,
      status: currentCourseAttendance.statuses[student.std_ID] || null,
    }));
  
    // Check if any student is missing a status
    const missingStatus = studentsData.some((student) => !student.status);
    if (missingStatus) {
      setNotification({
        message: "Please select a status for all students before saving.",
        type: "error",
        show: true,
      });
      setSaving(false);
      return;
    }
  
    const data = {
      course_code: course.course_code,
      date: new Date().toISOString().split("T")[0],
      students: studentsData,
    };
  
    try {
      const isUpdated = await upsertAttendance(data);
  
      setNotification({
        message: isUpdated ? "Attendance updated successfully!" : "Attendance saved successfully!",
        type: "success",
        show: true,
      });
  
      // Reset changes tracker since data is saved
      setChangesMade(false);
    } catch (error) {
      setNotification({
        message: "An error occurred while saving attendance.",
        type: "error",
        show: true,
      });
    } finally {
      setSaving(false);
  
      // Hide notification after 3 seconds
      setTimeout(() => {
        setNotification((prev) => ({ ...prev, show: false }));
      }, 3000);
    }
  };
  
  

  if (loading) return <div>Loading course data...</div>;
  if (error) return <div>Error: {error}</div>;

  if (!course) {
    return <div>Course not found.</div>;
  }

  return (
    <div>
      {notification.show && (
        <Notification message={notification.message} type={notification.type} onClose={() => setNotification({ ...notification, show: false })} />
      )}
      <section className="col-1">
        <div className="colItems">
          <Card cornerElement={group} title={course.course_name} value={`${course.student_count}`} />
        </div>
        <div className="colItems present">
          <Card cornerElement={classroom} title="Present" value={currentCourseAttendance.statusCounts.Present} />
        </div>
        <div className="colItems absent">
          <Card cornerElement={absent} title="Absent" value={currentCourseAttendance.statusCounts.Absent} />
        </div>
        <div className="colItems excuse">
          <Card cornerElement={hand} title="Excused" value={currentCourseAttendance.statusCounts.Excused} />
        </div>
      </section>

      <section className="profiles"> 
       <section>
        {fetchingStudents ? (
            <div>Loading enrolled students...</div>
          ) : fetchError ? (
            <div>Error: {fetchError}</div>
          ) : enrolledStudents.length === 0 ? (
            <div>No students are enrolled in this course.</div>
          ) : (
              <div className="student-list">
              {enrolledStudents.map((student, index) => (
                <ProfileCard
                  key={index}
                  student={student}
                  currentStatus={currentCourseAttendance.statuses[student.std_ID] || ""}
                  onStatusChange={(oldStatus, newStatus) => handleStatusChange(student.std_ID, oldStatus, newStatus)}
                />
              ))}
            </div>
        )}
       </section>
         <div className="footer">
          <button onClick={handleSaveAttendance} disabled={!changesMade || saving}>
            {saving ? "Saving..." : "Save Attendance"}
          </button>
          {saveError && <div style={{ color: "red" }}>{saveError}</div>}
      </div>
      </section>
     
    </div>
    
  );
};

export default Attendance;
