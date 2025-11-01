import React, { useState, useEffect } from 'react';
import LoginModal from './components/LoginModal';
import JobCard from './components/JobCard';
import ApplicationForm from './components/ApplicationForm';
import Navbar from './components/Navbar';
import { checkAuth, logout } from './utils/auth';
import './styles/App.css';

const App = () => {
  const [user, setUser] = useState(null);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const [showApplicationForm, setShowApplicationForm] = useState(false);

  // Mock job data
  const [jobs] = useState([
    {
      id: 1,
      title: "Frontend Developer",
      company: "Tech Corp",
      location: "Remote",
      salary: "$80,000 - $100,000",
      description: "We are looking for a skilled Frontend Developer to join our team...",
      requirements: ["React", "JavaScript", "CSS", "3+ years experience"]
    },
    {
      id: 2,
      title: "Backend Developer",
      company: "Data Systems Inc",
      location: "New York, NY",
      salary: "$90,000 - $120,000",
      description: "Join our backend team to build scalable systems...",
      requirements: ["Node.js", "Python", "SQL", "AWS", "5+ years experience"]
    },
    {
      id: 3,
      title: "UX Designer",
      company: "Creative Solutions",
      location: "San Francisco, CA",
      salary: "$75,000 - $95,000",
      description: "Design amazing user experiences for our products...",
      requirements: ["Figma", "UI/UX Design", "User Research", "2+ years experience"]
    }
  ]);

  useEffect(() => {
    // Check if user is already logged in
    const currentUser = checkAuth();
    if (currentUser) {
      setUser(currentUser);
    }
  }, []);

  const handleLoginSuccess = (userData) => {
    setUser(userData);
    setShowLoginModal(false);
    
    // If there was a selected job, show application form
    if (selectedJob) {
      setShowApplicationForm(true);
    }
  };

  const handleApplyClick = (job) => {
    if (!user) {
      setSelectedJob(job);
      setShowLoginModal(true);
      return;
    }
    
    setSelectedJob(job);
    setShowApplicationForm(true);
  };

  const handleLogout = () => {
    logout();
    setUser(null);
    setShowApplicationForm(false);
    setSelectedJob(null);
  };

  const handleApplicationSubmit = (applicationData) => {
    console.log('Application submitted:', {
      job: selectedJob,
      user: user,
      application: applicationData
    });
    
    alert(`Application submitted successfully for ${selectedJob.title} at ${selectedJob.company}!`);
    setShowApplicationForm(false);
    setSelectedJob(null);
  };

  return (
    <div className="app">
      <Navbar user={user} onLogout={handleLogout} />
      
      <div className="container">
        {!showApplicationForm ? (
          <>
            <div className="header">
              <h1>Find Your Dream Job</h1>
              <p>Browse through our latest job openings</p>
            </div>

            <div className="jobs-grid">
              {jobs.map(job => (
                <JobCard
                  key={job.id}
                  job={job}
                  onApplyClick={handleApplyClick}
                  user={user}
                />
              ))}
            </div>
          </>
        ) : (
          <ApplicationForm
            job={selectedJob}
            user={user}
            onSubmit={handleApplicationSubmit}
            onCancel={() => setShowApplicationForm(false)}
          />
        )}
      </div>

      <LoginModal
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
        onLoginSuccess={handleLoginSuccess}
      />
    </div>
  );
};

export default App;
