import React, { useContext, useState, useEffect } from 'react';
import './navbar.css';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

const NavBar = ({ handleAttendanceOverviewClick, goToDashboard, openAttendance }) => {
  const [activeTab, setActiveTab] = useState(() => {
   
    return localStorage.getItem('activeTab') || 'dashboard';
  });

  const bell = "/bell.png";
  const dashboard = "/dashboard.png";
  const group = "/group.png";
  const structure = "/structure.png";
  const setting = "/setting.png";
  const exit = "/exit.png";
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();

  // Save active tab to localStorage whenever it changes
  useEffect(() => {
    if (activeTab) {
      localStorage.setItem('activeTab', activeTab); // Store active tab in localStorage
    }
  }, [activeTab]);

  const handleLogout = () => {
    logout(); // Call logout function from AuthContext
    navigate('/');
    window.location.reload(); // Reload the page to reset app state
  };

  // Set active tab and navigate to corresponding path
  const handleTabClick = (tabName, navigateTo) => {
    setActiveTab(tabName); // Update the active tab
    if (navigateTo) navigate(navigateTo); // Optionally navigate
  };

  return (
    <div className='nav_container'>
      <nav className="nav-bar">
        <section className='featureBtn'>
          <button
            className={`nav-button ${activeTab === 'notification' ? 'active' : ''}`}
            onClick={() => handleTabClick('notification')}
          >
            <img src={bell} alt="bell" />
          </button>
          <button
            className={`nav-button ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => { handleTabClick('dashboard', '*'); goToDashboard(); }}
          >
            <img src={dashboard} alt="dashboard" />
          </button>
          <button
            className={`nav-button ${activeTab === 'attendance' ? 'active' : ''}`}
            onClick={() => { handleTabClick('attendance'); openAttendance(); }}
          >
            <img src={group} alt="group" />
          </button>
          <button
            className={`nav-button ${activeTab === 'attendance-Overview' ? 'active' : ''}`}
            onClick={() => { handleTabClick('attendance-Overview'); handleAttendanceOverviewClick(); }}
          >
            <img src={structure} alt="structure" />
          </button>
        </section>
        <section className='actionBtn'>
          <button
            className={`nav-button ${activeTab === 'settings' ? 'active' : ''}`}
            onClick={() => handleTabClick('settings')}
          >
            <img src={setting} alt="setting" />
          </button>
          <button className="nav-button" onClick={handleLogout}>
            <img src={exit} alt="exit" />
          </button>
        </section>
      </nav>
    </div>
  );
};

export default NavBar;
