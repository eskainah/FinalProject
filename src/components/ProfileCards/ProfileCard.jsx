import React, { useState } from 'react';
import './profile.css'

const ProfileCard = ({ student }) => {
  const [status, setStatus] = useState(''); // Track the current status (Present, Absent, Excused)

  // Function to handle status change
  const handleStatusChange = (newStatus) => {
    setStatus(newStatus);
  };

  return (
    <div className="profile-card">
      <div className="profile-header">
        <img
          src={student.photo} // Student photo URL
          alt={`${student.name}'s photo`}
          className="profile-photo"
        />
        <div className="profile-info">
          <h4>{student.name}</h4>
          <p>{student.std_ID}</p>
        </div>
      </div>
      
      <div className="profile-actions">
        <button
          className={`status-btn ${status === 'Present' ? 'active present' : ''}`}
          onClick={() => handleStatusChange('Present')}
        >P</button>
        <button
          className={`status-btn ${status === 'Absent' ? 'active absent' : ''}`}
          onClick={() => handleStatusChange('Absent')}
        >A</button>
        <button
          className={`status-btn ${status === 'Excused' ? 'active excused' : ''}`}
          onClick={() => handleStatusChange('Excused')}
        >E</button>
      </div>
    </div>
  );
};

export default ProfileCard;
