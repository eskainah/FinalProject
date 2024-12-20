import React, { useState, useEffect, useContext, useMemo } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import ApiContext from '../../context/ApiContext';

// Register necessary chart components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const AttendanceLineGraph = () => {
  const { 
    weeklyPresentPercentage,
    weeklyAbsentPercentage,
    weeklyExcusedPercentage,
    monthlyPresentPercentage,
    monthlyAbsentPercentage,
    monthlyExcusedPercentage,
  } = useContext(ApiContext);

  const [selectedGraph, setSelectedGraph] = useState('weekly');

  // Helper function to ensure the data is an array before using map
  const safeMap = (data) => Array.isArray(data) ? data.map(percentage => Math.round(percentage)) : [];
 
  const chartData = useMemo(() => {
    if (selectedGraph === 'weekly') {
      return {
        labels: Array.from({ length: 16 }, (_, i) => `Week ${i + 1}`),
        datasets: [
          {
            label: 'Present (%)',
            data: safeMap(weeklyPresentPercentage),
            borderColor: 'green',
            backgroundColor: 'green',
            fill: false,
            pointRadius: 0, 
            borderWidth: 1, 
          },
          {
            label: 'Absent (%)',
            data: safeMap(weeklyAbsentPercentage),
            borderColor: 'red',
            backgroundColor: 'red',
            fill: false,
            pointRadius: 0, 
            borderWidth: 1, 
          },
          {
            label: 'Excused (%)',
            data: safeMap(weeklyExcusedPercentage),
            borderColor: 'blue',
            backgroundColor: 'blue',
            fill: false,
            pointRadius: 0, 
            borderWidth: 1, 
          },
        ],
      };
    } else if (selectedGraph === 'monthly') {
      return {
        labels: ['Month I', 'Month II', 'Month III', 'Month IV'],
        datasets: [
          {
            label: 'Present (%)',
            data: safeMap(monthlyPresentPercentage),
            borderColor: 'green',
            backgroundColor: 'green',
            fill: false,
            pointRadius: 0,
            borderWidth: 1,
          },
          {
            label: 'Absent (%)',
            data: safeMap(monthlyAbsentPercentage),
            borderColor: 'red',
            backgroundColor: 'red',
            fill: false,
            pointRadius: 0, 
            borderWidth: 1, 
          },
          {
            label: 'Excused (%)',
            data: safeMap(monthlyExcusedPercentage),
            borderColor: 'blue',
            backgroundColor: 'blue',
            fill: false,
            pointRadius: 0, 
            borderWidth: 1, 
          },
        ],
      };
    }
  }, [
    selectedGraph,
    weeklyPresentPercentage,
    weeklyAbsentPercentage,
    weeklyExcusedPercentage,
    monthlyPresentPercentage,
    monthlyAbsentPercentage,
    monthlyExcusedPercentage,
  ]);

  // Chart options
  const chartOptions = useMemo(() => ({
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        min: 0,
        max: 100,
        ticks: {
          font: {
            size: 12,
          },
          stepSize: 20,
          padding: 10,
        },
      },
    },
    plugins: {
      legend: {
        display: false, // Hide the default legend
      },
    },
  }), []);

  // Custom Legend
  const customLegend = useMemo(() => (
    <div className='legend'>
      <div>
        <span className='boxes' style={{ backgroundColor: 'green' }}></span>
        <span>Present</span>
      </div>
      <div>
        <span className='boxes' style={{ backgroundColor: 'red' }}></span>
        <span>Absent</span>
      </div>
      <div>
        <span className='boxes' style={{ backgroundColor: 'blue' }}></span>
        <span>Excused</span>
      </div>
    </div>
  ), []);

  // Chart container style
  const chartContainerStyle = {
    height: '100%', 
    width: '100%',
  };

  return (
    <div className='lineGraph'>
      <section className='graphHeader'>
        <div>
          <h5>Attendance Comparison</h5>
        </div>
        {customLegend}
        <div className='graphBtn'>
          <button onClick={() => setSelectedGraph('weekly')}>Weekly</button>
          <button onClick={() => setSelectedGraph('monthly')}>Monthly</button>
        </div>
      </section>

      {/* Line chart */}
      <section className='graphContainer'>
        <Line data={chartData} options={chartOptions} style={chartContainerStyle} />
      </section>
    </div>
  );
};

export default AttendanceLineGraph;
