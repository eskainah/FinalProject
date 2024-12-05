import React from 'react';
import './popup.css'

const Notification = ({ message, type, onClose }) => {
  return (
    <div className={`notification ${type}`}>
      <div className="notification-content">
        <span>{message}</span>
        <button className="close-btn" onClick={onClose}>X</button>
      </div>
    </div>
  );
};

export default Notification;
