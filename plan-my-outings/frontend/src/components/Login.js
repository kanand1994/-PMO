import React, { useState } from 'react';
import { authAPI } from '../services/api';

const Login = ({ onLogin }) => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await authAPI.login(credentials);
      onLogin(response.data.user, response.data.token);
    } catch (error) {
      alert('Invalid credentials. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <div className="logo">
            <span className="logo-icon">📅</span>
            <span className="logo-text">Plan My Outings</span>
          </div>
          <h1>Welcome Back!</h1>
          <p>Sign in to continue planning amazing outings with your friends</p>
        </div>
        
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              name="username"
              placeholder="Enter your username"
              value={credentials.username}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              placeholder="Enter your password"
              value={credentials.password}
              onChange={handleChange}
              required
            />
          </div>
          
          <button 
            type="submit" 
            className="btn-primary login-btn"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="loading-spinner">⏳</span>
                Signing in...
              </>
            ) : (
              <>
                <span>🚀</span>
                Sign In
              </>
            )}
          </button>
        </form>
        
        <div className="login-footer">
          <p className="signup-link">
            Don't have an account? 
            <a href="/contact"> Contact Us!</a>
          </p>
          <p className="back-link">
            <a href="/">← Back to Home</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;

const styles = `
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-container {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 100%;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header .logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1rem;
}

.login-header .logo-icon {
  font-size: 1.5rem;
}

.login-header h1 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.login-header p {
  color: #666;
  font-size: 1rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.login-form .form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.login-btn {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

.login-footer {
  text-align: center;
}

.signup-link, .back-link {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.signup-link a, .back-link a {
  color: #ff6b6b;
  text-decoration: none;
  font-weight: 500;
}

.signup-link a:hover, .back-link a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .login-container {
    padding: 2rem;
    margin: 1rem;
  }
  
  .login-header h1 {
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