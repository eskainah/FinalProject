import React, { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import RoleBasedContent from "./RoleBaseContent";

const Dashboard = () => {
  
  const { user, logout } = useContext(AuthContext);

  if (!user) return <p>No user data available</p>;
  
  return (
    <div className="dashboard-container">
      {/* Dashboard UI */}
      <section className="dashboard-header">
        <div className="logoImg"></div>

        <div className="profile">
          <div className="profile_img">
          </div>
          <div className="user-info">
            <h4>{user.username}</h4> {/* Display username */}
            <p><strong>{user.role}</strong></p> {/* Display role */}
          </div>
        </div>
      </section>
      <div className="main-section">
      
      <section className="dashboard-nav">
        <button>Hello</button>
      </section>

      <section className="dashboard-main">
        <RoleBasedContent />
      </section>
      
      </div>
    </div>
  );
};


export default Dashboard;
