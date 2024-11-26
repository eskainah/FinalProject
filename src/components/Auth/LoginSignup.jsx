import { useEffect, useRef, useState} from 'react';
import './LoginSignup.css';

function LoginSignup({ onClose }) {
  const modalRef = useRef(null);
  // Close the modal when clicking outside of the modal (outside the overlay and content)
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (modalRef.current && !modalRef.current.contains(e.target)) {
        onClose();
      }
    };
    document.addEventListener('mousedown', handleClickOutside); // Add event listener to document
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);  // Cleanup event listener on unmount
    };


  }, [onClose]);


  const [activeSection, setActiveSection] = useState('login'); // 'login' or 'createAcc'

  const handleButtonClick = (section) => {
    setActiveSection(section);
  };

  return (
    <div className="modalOverlay" ref={modalRef}>
      <section className='toggleBtn'>
        <button 
          className={`signInBtn ${activeSection === 'login' ? 'active' : ''}`} 
          onClick={() => handleButtonClick('login')}
        >
          Sign In
        </button>
        <button 
          className={`createAcc ${activeSection === 'createAcc' ? 'active' : ''}`} 
          onClick={() => handleButtonClick('createAcc')}
        >
          Create Account
        </button>
      </section>
      
      <section className='frmContainer'>
        <form className={` ${activeSection ? 'activeBackground' : ''}`}>
          <section className={`login ${activeSection === 'login' ? 'show' : ''}`}>
            <h3>Login Form</h3>
          </section>
          
          <section className={`createNewAcc ${activeSection === 'createAcc' ? 'show' : ''}`}>
            <h3>Create Account Form</h3>
          </section>
        </form>
      </section>
    </div>
      
    
  );
}

export default LoginSignup;
