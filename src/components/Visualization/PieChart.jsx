// AttendancePieCharts.js
import React, { useEffect, useContext } from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import ApiContext from '../../context/ApiContext';
import './visual.css';

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

const AttendancePieCharts = () => {
  const { attendanceSummary, fetchAttendanceSummary, loading, error } = useContext(ApiContext);

  useEffect(() => {
    fetchAttendanceSummary();
  }, [fetchAttendanceSummary]);

  // Prepare chart data for each status (present, absent, excused)
  const prepareChartData = (key) => ({
    labels: attendanceSummary.map((data) => data.course_name),
    datasets: [
      {
        label: `${key} Percentage`,
        data: attendanceSummary.map((data) => data[key]),
        backgroundColor: ['#00A9D7', '#6E7C7C', '#80BC00', '#3A8DDE', '#FFA400', '#164D48'],
      },
    ],
  });

  // Chart options with data labels
  const chartOptions = {
    plugins: {
      legend: { display: false }, // Disable default legend
      datalabels: {
        color: '#fff',
        formatter: (value) => `${value}%`, // Show percentage in the chart
        font: {
          size: 14,
          weight: 'bold',
        },
      },
    },
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="pieCharts">
      <section className="chartSection">
        <div className="chartLabels">
          <h5>Percentage of Students Present</h5>
          <ul>
            {attendanceSummary.map((data, index) => (
              <li key={index}>
                <span
                  style={{
                    backgroundColor: ['#00A9D7', '#6E7C7C', '#80BC00', '#3A8DDE', '#FFA400', '#164D48'][index],
                  }}
                ></span>
                {data.course_name}
              </li>
            ))}
          </ul>
        </div>
        <div className="chartContainer">
          <Pie
            className='charts'
            data={prepareChartData('students_present_percentage')}
            options={chartOptions}
          />
        </div>
      </section>

      <section className="chartSection">
        <div className="chartLabels">
          <h5>Percentage of Students Absent</h5>
          <ul>
            {attendanceSummary.map((data, index) => (
              <li key={index}>
                <span
                  style={{
                    backgroundColor: ['#00A9D7', '#6E7C7C', '#80BC00', '#3A8DDE', '#FFA400', '#164D48'][index],
                  }}
                ></span>
                {data.course_name}
              </li>
            ))}
          </ul>
        </div>
        <div className="chartContainer">
          <Pie
            data={prepareChartData('students_absent_percentage')}
            options={chartOptions}
          />
        </div>
      </section>

      <section className="chartSection">
        <div className="chartLabels">
          <h5>Percentage of Students Excused</h5>
          <ul>
            {attendanceSummary.map((data, index) => (
              <li key={index}>
                <span
                  style={{
                    backgroundColor: ['#00A9D7', '#6E7C7C', '#80BC00', '#3A8DDE', '#FFA400', '#164D48'][index],
                  }}
                ></span>
                {data.course_name}
              </li>
            ))}
          </ul>
        </div>
        <div className="chartContainer">
          <Pie
            data={prepareChartData('students_excused_percentage')}
            options={chartOptions}
          />
        </div>
      </section>
    </div>
  );
};

export default AttendancePieCharts;
