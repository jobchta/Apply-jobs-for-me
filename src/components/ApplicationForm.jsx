import React, { useState } from 'react';

const ApplicationForm = ({ job, user, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    resume: '',
    coverLetter: '',
    phone: '',
    linkedIn: '',
    portfolio: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData(prev => ({
        ...prev,
        resume: file.name
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    onSubmit(formData);
    setIsSubmitting(false);
  };

  return (
    <div className="application-form-container">
      <div className="application-header">
        <h2>Apply for {job.title}</h2>
        <p className="company-name">{job.company} • {job.location}</p>
      </div>

      <div className="applicant-info">
        <h3>Applicant Information</h3>
        <p><strong>Name:</strong> {user.firstName} {user.lastName}</p>
        <p><strong>Email:</strong> {user.email}</p>
      </div>

      <form onSubmit={handleSubmit} className="application-form">
        <div className="form-group">
          <label htmlFor="resume">Resume *</label>
          <div className="file-upload">
            <input
              type="file"
              id="resume"
              accept=".pdf,.doc,.docx"
              onChange={handleFileChange}
              required
            />
            <span className="file-name">
              {formData.resume || 'Upload your resume (PDF, DOC)'}
            </span>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="phone">Phone Number *</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={formData.phone}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="linkedIn">LinkedIn Profile</label>
          <input
            type="url"
            id="linkedIn"
            name="linkedIn"
            value={formData.linkedIn}
            onChange={handleInputChange}
            placeholder="https://linkedin.com/in/yourprofile"
          />
        </div>

        <div className="form-group">
          <label htmlFor="portfolio">Portfolio Website</label>
          <input
            type="url"
            id="portfolio"
            name="portfolio"
            value={formData.portfolio}
            onChange={handleInputChange}
            placeholder="https://yourportfolio.com"
          />
        </div>

        <div className="form-group">
          <label htmlFor="coverLetter">Cover Letter *</label>
          <textarea
            id="coverLetter"
            name="coverLetter"
            rows="6"
            value={formData.coverLetter}
            onChange={handleInputChange}
            placeholder="Tell us why you're interested in this position and what makes you a good fit..."
            required
          />
        </div>

        <div className="form-actions">
          <button
            type="button"
            onClick={onCancel}
            className="cancel-button"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="submit-application-button"
          >
            {isSubmitting ? 'Submitting...' : 'Submit Application'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ApplicationForm;
