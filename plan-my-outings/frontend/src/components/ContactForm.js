import React, { useState } from 'react';
import { contactAPI } from '../services/api';

const ContactForm = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    year_of_birth: '',
    message: ''
  });
  const [credentials, setCredentials] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      console.log('Submitting form data:', formData);
      const response = await contactAPI.submitEnquiry(formData);
      console.log('Response received:', response);
      setCredentials(response.data.credentials);
      setFormData({
        first_name: '',
        last_name: '',
        email: '',
        year_of_birth: '',
        message: ''
      });
    } catch (error) {
      console.error('Error submitting enquiry:', error);
      console.error('Error response:', error.response);
      
      if (error.response && error.response.data && error.response.data.error === 'duplicate_email') {
        alert('An account with this email already exists. Please use the login page.');
      } else {
        alert('Error submitting enquiry. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="contact-page">
      <div className="contact-container">
        <div className="contact-header">
          <h1>Get Started with Plan My Outings</h1>
          <p>Fill out this form and we'll create your account automatically!</p>
        </div>
        
        {credentials && (
          <div className="credentials-success">
            <div className="success-icon">🎉</div>
            <h3>Account Created Successfully!</h3>
            <div className="credentials-info">
              <p><strong>Username:</strong> <code>{credentials.username}</code></p>
              <p><strong>Password:</strong> <code>{credentials.password}</code></p>
            </div>
            <p className="credentials-note">
              Please save these credentials and use them to login.
            </p>
            <button 
              className="btn-primary"
              onClick={() => window.location.href = '/login'}
            >
              Go to Login
            </button>
          </div>
        )}

        {!credentials && (
          <form className="contact-form" onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>First Name</label>
                <input
                  type="text"
                  name="first_name"
                  placeholder="Enter your first name"
                  value={formData.first_name}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Last Name</label>
                <input
                  type="text"
                  name="last_name"
                  placeholder="Enter your last name"
                  value={formData.last_name}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>
            
            <div className="form-group">
              <label>Email Address</label>
              <input
                type="email"
                name="email"
                placeholder="Enter your email address"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="form-group">
              <label>Year of Birth</label>
              <input
                type="number"
                name="year_of_birth"
                placeholder="e.g., 1990"
                min="1900"
                max="2123"
                value={formData.year_of_birth}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="form-group">
              <label>Message (Optional)</label>
              <textarea
                name="message"
                placeholder="Tell us about your group planning needs..."
                value={formData.message}
                onChange={handleChange}
                rows="4"
              />
            </div>
            
            <button 
              type="submit" 
              className="btn-primary submit-btn"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="loading-spinner">⏳</span>
                  Submitting...
                </>
              ) : (
                <>
                  <span>🚀</span>
                  Submit
                </>
              )}
            </button>
            
            <p className="login-link">
              Already have an account? <a href="/login">Sign in here</a>
            </p>
          </form>
        )}
      </div>
    </div>
  );
};

export default ContactForm;

const styles = `
.contact-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.contact-container {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  width: 100%;
}

.contact-header {
  text-align: center;
  margin-bottom: 2rem;
}

.contact-header h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.contact-header p {
  color: #666;
  font-size: 1.1rem;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.submit-btn {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

.credentials-success {
  text-align: center;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 12px;
  border: 2px solid #4ecdc4;
}

.success-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.credentials-success h3 {
  color: #333;
  margin-bottom: 1rem;
}

.credentials-info {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  text-align: left;
}

.credentials-info code {
  background: #f0f0f0;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: monospace;
}

.credentials-note {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.login-link {
  text-align: center;
  color: #666;
  margin-top: 1rem;
}

.login-link a {
  color: #ff6b6b;
  text-decoration: none;
  font-weight: 500;
}

.login-link a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .contact-container {
    padding: 2rem;
    margin: 1rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .contact-header h1 {
    font-size: 1.5rem;
  }
}
`;

// Inject styles
if (typeof document !== 'undefined') {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = styles;
  document.head.appendChild(styleSheet);
}