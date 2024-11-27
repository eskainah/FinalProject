import { useState } from 'react'
import logo from '../public/logo.png'
import LoginSignup from './components/Auth/LoginSignup'

import './App.css'

function App() {
  const [showLoginSignup, setShowLoginSignup] = useState(false);

  const toggleLoginSignup = () => {
    setShowLoginSignup((prev) => !prev);
  };

  return (
    <>
    <div className="container">
      <header>
        <section>
          <img src={logo} alt=""/>
        </section>
        <nav>
        
          <a href="">Home</a>
          <a href="">About</a>
          <a href="">Contact Us</a>
        
        </nav>
      </header> 
      <div className='hero'>
        <p><strong>Attendance Simplified, Results amplified <br />
          Be here now, thrive everywhere  </strong>
        </p>
        <button className="signinBtn" onClick={toggleLoginSignup}>Sign In</button>
        {showLoginSignup && <LoginSignup onClose={toggleLoginSignup} />}
      </div>
     
  </div>
  </>
)}
  
export default App
