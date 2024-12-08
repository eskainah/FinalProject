import React, { useState, useEffect, useContext, useMemo } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import ApiContext from '../../context/ApiContext';

// Register necessary chart components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const AttendanceLineGraph = () => {
  const { 
    dailyPresentPercentage,
    dailyAbsentPercentage,
    dailyExcusedPercentage,
    weeklyPresentPercentage,
    weeklyAbsentPercentage,
    weeklyExcusedPercentage,
    monthlyPresentPercentage,
    monthlyAbsentPercentage,
    monthlyExcusedPercentage,
  } = useContext(ApiContext);

  

  const [selectedGraph, setSelectedGraph] = useState('daily');

  // Use `useMemo` to avoid unnecessary recomputations of chartData
  const chartData = useMemo(() => {
    if (selectedGraph === 'daily') {
      return {
        labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
        datasets: [
          {
            label: 'Present (%)',
            data: dailyPresentPercentage.map(value => Math.round(value)),
            borderColor: 'green',
            backgroundColor: 'green',
            fill: false,
          },
          {
            label: 'Absent (%)',
            data: dailyAbsentPercentage.map(value => Math.round(value)),
            borderColor: 'red',
            backgroundColor: 'red',
            fill: false,
          },
          {
            label: 'Excused (%)',
            data: dailyExcusedPercentage.map(value => Math.round(value)),
            borderColor: 'blue',
            backgroundColor: 'blue',
            fill: false,
          },
        ],
      };
    } else if (selectedGraph === 'weekly') {
      return {
        labels: ['Week I', 'Week II', 'Week III', 'Week IV'],
        datasets: [
          {
            label: 'Present (%)',
            data: weeklyPresentPercentage.map(percentage => Math.round(percentage)),
            borderColor: 'green',
            backgroundColor: 'green',
            fill: false,
          },
          {
            label: 'Absent (%)',
            data: weeklyAbsentPercentage.map(percentage => Math.round(percentage)),
            borderColor: 'red',
            backgroundColor: 'red',
            fill: false,
          },
          {
            label: 'Excused (%)',
            data: weeklyExcusedPercentage.map(percentage => Math.round(percentage)),
            borderColor: 'blue',
            backgroundColor: 'blue',
            fill: false,
          },
        ],
      };
    } else if (selectedGraph === 'monthly') {
      return {
        labels: ['Month I', 'Month II', 'Month III', 'Month IV'],
        datasets: [
          {
            label: 'Present (%)',
            data: monthlyPresentPercentage.map(percentage => Math.round(percentage)),
            borderColor: 'green',
            backgroundColor: 'green',
            fill: false,
          },
          {
            label: 'Absent (%)',
            data: monthlyAbsentPercentage.map(percentage => Math.round(percentage)),
            borderColor: 'red',
            backgroundColor: 'red',
            fill: false,
          },
          {
            label: 'Excused (%)',
            data: monthlyExcusedPercentage.map(percentage => Math.round(percentage)),
            borderColor: 'blue',
            backgroundColor: 'blue',
            fill: false,
          },
        ],
      };
    }
  }, [
    selectedGraph,
    dailyPresentPercentage,
    dailyAbsentPercentage,
    dailyExcusedPercentage,
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
    height: '100%',  // Or '100%' for dynamic resizing
    width: '100%',
  };

  return (
    <div className='lineGraph'>
      {/* Buttons to switch between daily, weekly, and monthly graphs */}
      <section className='graphHeader'>
        <div>
          <h5>Attendance Comparison</h5>
        </div>
        {customLegend}
        <div className='graphBtn'>
          <button onClick={() => setSelectedGraph('daily')}>Daily</button>
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
