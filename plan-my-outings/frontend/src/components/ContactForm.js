import React, { useState } from 'react';
import { contactAPI } from '../services/api';

const ContactForm = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    year_of_birth: '',
    message: ''
  });
  const [credentials, setCredentials] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedMethod, setSelectedMethod] = useState(null);

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
        phone: '',
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

  const handleNotificationMethod = async (method) => {
    setSelectedMethod(method);
    
    try {
      switch (method) {
        case 'email':
          alert('Email notification attempted. Please check your email or try another method.');
          break;
        case 'sms':
          const phone = prompt('Enter your phone number (with country code):');
          if (phone) {
            // Call SMS API
            alert(`SMS will be sent to ${phone} (SMS service needs to be configured)`);
          }
          break;
        case 'whatsapp':
          const whatsapp = prompt('Enter your WhatsApp number (with country code):');
          if (whatsapp) {
            alert(`WhatsApp message will be sent to ${whatsapp} (WhatsApp service needs to be configured)`);
          }
          break;
        case 'download':
          // Create and download credentials file
          const credentialsText = `Plan My Outings - Account Credentials\n\nUsername: ${credentials.username}\nPassword: ${credentials.password}\n\nLogin at: http://localhost:3000/login\n\nKeep these credentials safe!`;
          const blob = new Blob([credentialsText], { type: 'text/plain' });
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'plan-my-outings-credentials.txt';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
          alert('Credentials downloaded successfully! Please keep the file safe.');
          break;
        default:
          break;
      }
    } catch (error) {
      console.error('Error with notification method:', error);
      alert('Error processing your request. Please try again.');
    }
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
            <div className="notification-options">
              <p>Your Plan My Outings account has been created!</p>
              <div className="notification-methods">
                <h4>How would you like to receive your login credentials?</h4>
                <div className="method-buttons">
                  <button 
                    className="btn-method email-btn"
                    onClick={() => handleNotificationMethod('email')}
                  >
                    📧 Email
                  </button>
                  <button 
                    className="btn-method sms-btn"
                    onClick={() => handleNotificationMethod('sms')}
                  >
                    📱 SMS
                  </button>
                  <button 
                    className="btn-method whatsapp-btn"
                    onClick={() => handleNotificationMethod('whatsapp')}
                  >
                    💬 WhatsApp
                  </button>
                  <button 
                    className="btn-method download-btn"
                    onClick={() => handleNotificationMethod('download')}
                  >
                    💾 Download
                  </button>
                </div>
              </div>
            </div>
            <p className="security-note">
              For security reasons, your credentials are not displayed on this page.
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
              <label>Phone Number (Optional)</label>
              <input
                type="tel"
                name="phone"
                placeholder="Enter your phone number (for SMS/WhatsApp)"
                value={formData.phone}
                onChange={handleChange}
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

.notification-options {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1rem 0;
  text-align: left;
}

.notification-methods h4 {
  color: #333;
  margin: 1rem 0 0.5rem 0;
  font-size: 1rem;
}

.method-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn-method {
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  text-align: center;
}

.btn-method:hover {
  border-color: #4ecdc4;
  background: #f8f9fa;
  transform: translateY(-2px);
}

.email-btn:hover { border-color: #ff6b6b; }
.sms-btn:hover { border-color: #4ecdc4; }
.whatsapp-btn:hover { border-color: #25d366; }
.download-btn:hover { border-color: #ffa726; }

.security-note {
  background: #f0f8ff;
  padding: 0.75rem;
  border-radius: 6px;
  border-left: 4px solid #4ecdc4;
  color: #555;
  font-size: 0.9rem;
  margin: 1rem 0;
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