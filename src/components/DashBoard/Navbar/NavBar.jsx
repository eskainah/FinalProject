import React, { useState } from 'react';
import './navbar.css';
import Dashboard from '../Dashboard';
import Attendance from '../Attendance';

// import Component6 from '../Component6';

const NavBar = () => {
    const bell = "/bell.png";
    const dashboard = "/dashboard.png";
    const group = "/group.png";
    const structure = "/structure.png";
    const setting = "/setting.png";
    const exit = "/exit.png";

    const [activeTab, setActiveTab] = useState('tab1');

    const renderComponent = () => {
        switch (activeTab) {
            case 'tab1': return < Dashboard/>;
            case 'tab2': return <Dashboard />;
            case 'tab3': return <Attendance />;
            case 'tab4': return <Dashboard />;
            case 'tab5': return <Dashboard />;
            // case 'tab6': return <Component6 />;
            default: return null;
        }
    };

    return (
        <div>
            <nav className="nav-bar">
                <button
                    className={`nav-button ${activeTab === 'tab1' ? 'active' : ''}`}
                    onClick={() => setActiveTab('tab1')}
                >
                    <img src={bell} alt="bell" />
                </button>
                <button
                    className={`nav-button ${activeTab === 'tab2' ? 'active' : ''}`}
                    onClick={() => setActiveTab('tab2')}
                > 
                <img src={dashboard} alt="dashboard" />
                </button>
                <button
                    className={`nav-button ${activeTab === 'tab3' ? 'active' : ''}`}
                    onClick={() => setActiveTab('tab3')}
                >
                    <img src={group} alt="group" />
                </button>
                <button
                    className={`nav-button ${activeTab === 'tab4' ? 'active' : ''}`}
                    onClick={() => setActiveTab('tab4')}
                >
                     <img src={structure} alt="structure" />
                </button>
                <button
                    className={`nav-button ${activeTab === 'tab5' ? 'active' : ''}`}
                    onClick={() => setActiveTab('tab5')}
                >
                     <img src={setting} alt="setting" />
                </button>
                <button
                    className={`nav-button ${activeTab === 'tab6' ? 'active' : ''}`}
                    onClick={() => setActiveTab('tab6')}
                >
                    <img src={exit} alt="exit" />
                </button>
            </nav>
            <div className="component-container">
                {renderComponent()}
            </div>
        </div>
    );
};

export default NavBar;
