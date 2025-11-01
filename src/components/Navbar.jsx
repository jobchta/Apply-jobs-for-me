import React from 'react';

const Navbar = ({ user, onLogout }) => {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="nav-brand">
          <h2>CareerConnect</h2>
        </div>
        
        <div className="nav-items">
          {user ? (
            <div className="user-section">
              <span className="welcome-text">
                Welcome, {user.firstName}!
              </span>
              <button 
                onClick={onLogout}
                className="logout-button"
              >
                Logout
              </button>
            </div>
          ) : (
            <div className="auth-section">
              <span>Ready to apply? Login to get started</span>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
