import React, { useContext, useState } from 'react';
import './navbar.css';
import Attendance from '../Attendance';
import { AuthContext } from '../../../../AuthContext';
import { useNavigate } from 'react-router-dom';
import App from '../../../App';
const NavBar = () => {
    const { logout } = useContext(AuthContext); // Consume logout function from context
    const navigate = useNavigate(); 

    const bell = "/bell.png";
    const dashboard = "/dashboard.png";
    const group = "/group.png";
    const structure = "/structure.png";
    const setting = "/setting.png";
    const exit = "/exit.png";

    const [activeTab, setActiveTab] = useState('tab1'); // Start with tab1 active
    const [isLoggedOut, setIsLoggedOut] = useState(false); // Track logout state

    const renderComponent = () => {
        switch (activeTab) {
            case 'tab3': return <Attendance />;
            default: return null;
        }
    };

    const handleLogout = () => {
        logout(); // Call logout to update the authentication state
        setIsLoggedOut(true); // Set the logged-out state
    };

    if (isLoggedOut) {
        return <App />; // Render the App component (redirects to login)
    }

    return (
        <div className='nav_container'>
            <nav className="nav-bar">
                <section className='featureBtn'>
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
                </section>

                <section className='actionBtn'>
                    <button
                        className={`nav-button ${activeTab === 'tab5' ? 'active' : ''}`}
                        onClick={() => setActiveTab('tab5')}
                    > 
                    <img src={setting} alt="setting" />
                    </button>

                    <button className="nav-button" onClick={handleLogout}> 
                    <img src={exit} alt="exit" />
                    </button>
                </section>
            </nav>

            <div className="component-container">
                {renderComponent()}
            </div>
        </div>
    );
};

export default NavBar;
