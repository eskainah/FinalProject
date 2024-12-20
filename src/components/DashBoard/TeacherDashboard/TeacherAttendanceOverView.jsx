import React, { useState, useContext, useEffect, useMemo, useCallback } from "react";
import ApiContext from "../../../context/ApiContext";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import ChartDataLabels from 'chartjs-plugin-datalabels';
import './TeacherDashboard.css';
import Card from "../Card";

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

const TeacherAttendanceOverview = ({ selectedCourse }) => {
  const {
    data,
    fetchOverview,
    weeklyOverview,
    StudentAttendanceAverages,
    attendanceSummary,
    fetchAttendanceSummary,
  } = useContext(ApiContext);
 
  const group = "/group.png";
  const print = "/printer.png";
  const search = "/search.png";
  const filterImg = "/filter.png";

  const [isDropdownVisible, setDropdownVisible] = useState(false);
  const [selectedOption, setSelectedOption] = useState("Weekly");
  const [fetchError, setFetchError] = useState(null); // Track fetch error
  
  const toggleDropdown = () => {
    setDropdownVisible(!isDropdownVisible);
  };

  const handleOptionSelect = useCallback((option) => {
    setSelectedOption(option);
    setDropdownVisible(false);
  }, []);

  // Memoize the selected course and check for data
  const course = useMemo(() => {
    return data?.courses?.find((course) => course.course_name === selectedCourse);
  }, [data, selectedCourse]);

  // Memoize attendance summary for selected course
  const selectedCourseAttendanceData = useMemo(() => {
    return attendanceSummary?.find((course) => course.course_name === selectedCourse);
  }, [attendanceSummary, selectedCourse]);

  // Create an AbortController
  const controller = new AbortController();
  const signal = controller.signal;

  // Fetch attendance summary data
  useEffect(() => {
    fetchAttendanceSummary();
  }, [fetchAttendanceSummary]);

  // Fetch attendance data based on selected course and option
  useEffect(() => {
    if (course) {
      setFetchError(null);
      fetchOverview(course.course_code, selectedOption.toLowerCase(), "", { signal }).catch((err) => {
        if (err.name !== "AbortError") {
          setFetchError("Failed to fetch attendance overview: " + err.message);
        }
      });
    }

    // Cleanup function to abort fetch if the component is unmounted or if the effect is re-triggered
    return () => {
      controller.abort();
    };
  }, [course, fetchOverview, selectedOption]);

  // Memoize chart data for performance optimization
  const prepareChartData = useMemo(() => {
    return {
      labels: selectedCourseAttendanceData ? ["Present", "Absent", "Excused"] : [],
      datasets: [
        {
          data: selectedCourseAttendanceData
            ? [
                selectedCourseAttendanceData.students_present_percentage,
                selectedCourseAttendanceData.students_absent_percentage,
                selectedCourseAttendanceData.students_excused_percentage,
              ]
            : [0, 0, 0],
          backgroundColor: ["green", "red", "blue"], 
        },
      ],
    };
  }, [selectedCourseAttendanceData]);

  const chartOptions = {
    plugins: {
      legend: { display: false },
      datalabels: {
        color: "#fff",
        formatter: (value) => `${value.toFixed(0)}%`,
        font: {
          size: 12,
          weight: "bold",
        },
      },
    },
  };

  const getStatusBox = (status) => {
    if (status === "Present") {
      return <div className="status-box present-box">✔</div>;
    } else if (status === "Absent") {
      return <div className="status-box absent-box">✘</div>;
    } else if (status === "Excused") {
      return <div className="status-box excused-box">?</div>;
    }
    return <div className="status-box empty-box"></div>;
  };

  const renderAttendanceBox = useCallback((present, absent, excused) => {
    const total = present + absent + excused;
    const presentWidth = (present / total) * 100;
    const absentWidth = (absent / total) * 100;
    const excusedWidth = (excused / total) * 100;

    return (
      <div className="avg-chart">
        <div
          style={{
            backgroundColor: "green",
            width: `${presentWidth}%`,
            height: "100%",
          }}
        >
          <p>{presentWidth}%</p>
        </div>
        <div
          style={{
            backgroundColor: "red",
            width: `${absentWidth}%`,
            height: "100%",
          }}
        >
           <p>{absentWidth}%</p>
        </div>
        <div
          style={{
            backgroundColor: "blue",
            width: `${excusedWidth}%`,
            height: "100%",
          }}
        >
           <p>{excusedWidth}%</p>
        </div>
      </div>
    );
  }, []);

  const renderWeeklyOverview = useMemo(() => {
    if (!weeklyOverview || weeklyOverview.length === 0) {
      return <p>No weekly attendance records available.</p>;
    }

    const weekKeys = Object.keys(weeklyOverview[0]).filter((key) => key.startsWith("Week"));

    return (
      <table>
        <thead>
          <tr>
            <th>Student ID</th>
            <th>Student Name</th>
            {weekKeys.map((week) => (
              <th className="weeksth" key={week}>{week}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {weeklyOverview.map((record) => (
            <tr key={record["Student ID"]}>
              <td>{record["Student ID"]}</td>
              <td>{record["Student Name"]}</td>
              {weekKeys.map((week) => (
                <td className="records" key={`${record["Student ID"]}-${week}`}>
                  {record[week] !== "null" && record[week] !== null
                    ? getStatusBox(record[week])
                    : <div className="status-box empty-box"></div>}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  }, [weeklyOverview]);

  const renderAveragesOverview = useMemo(() => {
    if (!StudentAttendanceAverages || StudentAttendanceAverages.length === 0) {
      return <p>No student attendance averages available.</p>;
    }

    return (
      <table>
        <thead>
          <tr>
            <th>Student ID</th>
            <th>Student Name</th>
            <th>Average Attendance</th>
          </tr>
        </thead>
        <tbody>
          {StudentAttendanceAverages.map((record) => (
            <tr key={record["Student ID"]}>
              <td>{record["Student ID"]}</td>
              <td>{record["Student Name"]}</td>
              <td>
                <div>
                  {renderAttendanceBox(
                    record["Present Percentage"],
                    record["Absent Percentage"],
                    record["Excused Percentage"]
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }, [StudentAttendanceAverages]);

  return (
    <div className="overview_container">
      {/* Course info section */}
      <section className="col-1">
        <div className="course_info">
          {course ? (
            <div className="colItems">
              <Card cornerElement={group} title={course.course_name} value={`${course.student_count}`} />
            </div>
          ) : (
            <p>No courses assigned</p>
          )}
        </div>
        <div className="indicator">
            <div className="indicator-item">
              <div className="box">
                <div><span className="present-box"> </span> Present</div>
                <div><span className="absent-box"></span>Absent</div>
                <div><span className="excused-box"></span>Excused</div>
              </div>
            </div>
            <div className="indicator-chart" >
            <Pie className="chart" data={prepareChartData} options={chartOptions} />
            </div>
            
        </div>
      </section>

      {/* Attendance overview and filters section */}
      <section className="col-1 table_holder">
        <section className="CrtlBtn">
          <div className="fields">
            <h5>{selectedOption} Attendance Overview</h5>

            <div>
              <input
                className="search"
                type="text"
                placeholder="Search"
                onFocus={(e) => {
                  e.target.style.border = "1px solid rgb(192, 190, 190);";
                }}
              />
              <button>
                <img src={search} alt="search" />
              </button>
            </div>
          </div>

          {/* Filter dropdown */}
          <div className="btns">
            <div>
              <button className="filterBtn" onClick={toggleDropdown}>
                <img src={filterImg} alt="FilterIcon" /> Filter
              </button>
              {isDropdownVisible && (
                <div className="filter-list">
                  <ul>
                    <li onClick={() => handleOptionSelect("Weekly")}> Weekly</li>
                    <li onClick={() => handleOptionSelect("Averages")}> Averages</li>
                  </ul>
                </div>
              )}
            </div>

            <button className="PrintBtn">
              <img src={print} alt="print" /> Print Report
            </button>
          </div>
        </section>

        <section className="DataTable">
          {fetchError && <p className="error">{fetchError}</p>} {/* Display error message */}
          {selectedOption === "Weekly"
            ? renderWeeklyOverview
            : selectedOption === "Averages"
            ? renderAveragesOverview
            : (
              <p>No {selectedOption.toLowerCase()} attendance records available.</p>
            )}
        </section>
      </section>
    </div>
  );
};

export default TeacherAttendanceOverview;
