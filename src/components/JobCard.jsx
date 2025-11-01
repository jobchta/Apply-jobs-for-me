import React from 'react';

const JobCard = ({ job, onApplyClick, user }) => {
  return (
    <div className="job-card">
      <div className="job-header">
        <h3 className="job-title">{job.title}</h3>
        <span className="company-name">{job.company}</span>
      </div>
      
      <div className="job-details">
        <div className="detail-item">
          <span className="label">Location:</span>
          <span className="value">{job.location}</span>
        </div>
        <div className="detail-item">
          <span className="label">Salary:</span>
          <span className="value">{job.salary}</span>
        </div>
      </div>

      <div className="job-description">
        <p>{job.description}</p>
      </div>

      <div className="requirements">
        <h4>Requirements:</h4>
        <ul>
          {job.requirements.map((req, index) => (
            <li key={index}>{req}</li>
          ))}
        </ul>
      </div>

      <button 
        className="apply-button"
        onClick={() => onApplyClick(job)}
      >
        {user ? 'Apply Now' : 'Login to Apply'}
      </button>
    </div>
  );
};

export default JobCard;
