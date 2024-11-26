import { useState } from 'react'
import logo from '../public/logo.png'

import './App.css'

function App() {


  return (
    <>
    <div class="container">
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
      <div>
        <p><strong>Attendance Simplified, Results amplified <br />
          Be here now, thrive everywhere  </strong>
        </p>
        <button class="signinBtn">Sign In</button>
      </div>
  </div>
  </>
)}
  
export default App
