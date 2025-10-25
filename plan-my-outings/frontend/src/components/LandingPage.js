import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      {/* Header */}
      <header className="landing-header">
        <div className="logo">
          <span className="logo-icon">📅</span>
          <span className="logo-text">Plan My Outings</span>
        </div>
        <div className="header-actions">
          <button className="login-btn" onClick={() => navigate('/login')}>
            Login
          </button>
          <button className="contact-btn" onClick={() => navigate('/contact')}>
            Contact Us
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-text">
            <p className="hero-tagline">🎯 Plan Together, Have Fun Together</p>
            <h1 className="hero-title">
              Plan Your <span className="highlight-orange">Perfect</span>
              <br />
              <span className="highlight-green">Outing</span>
            </h1>
            <p className="hero-description">
              Create groups, suggest movies or cafes, and let everyone vote with
              emojis. Planning outings with friends has never been this fun!
            </p>
            <div className="hero-actions">
              <button className="cta-primary" onClick={() => navigate('/contact')}>
                Get Started Free
              </button>
              <button className="cta-secondary" onClick={() => navigate('/login')}>
                Sign In
              </button>
            </div>
          </div>
          <div className="hero-image">
            <div className="image-placeholder">
              <div className="friends-illustration">
                <div className="friend friend-1">👥</div>
                <div className="friend friend-2">🎬</div>
                <div className="friend friend-3">🍕</div>
                <div className="friend friend-4">🎉</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="features-container">
          <h2 className="features-title">Everything You Need</h2>
          <p className="features-subtitle">
            Simple, fun, and effective tools to plan group outings
          </p>

          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">👥</div>
              <h3 className="feature-title">Create Groups</h3>
              <p className="feature-description">
                Bring your friends together and plan amazing outings
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">📅</div>
              <h3 className="feature-title">Suggest Plans</h3>
              <p className="feature-description">
                Share movie ideas or cafe spots with your group
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">👍</div>
              <h3 className="feature-title">Vote with Emojis</h3>
              <p className="feature-description">
                Express your opinion with fun emoji reactions
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Chat Assistant */}
      {/* <div className="chat-assistant">
        <div className="chat-bubble">
          <div className="chat-header">
            <span className="chat-icon">🤖</span>
            <span className="chat-name">PlanPal</span>
            <span className="chat-status">Always here to help</span>
            <button className="chat-close">×</button>
          </div>
          <div className="chat-message">
            Hi! I'm PlanPal, your planning assistant! How can I help you today?
            😊
          </div>
          <div className="chat-input">
            <input type="text" placeholder="Type a message..." />
            <button className="chat-send">➤</button>
          </div>
        </div>
      </div> */}
    </div>
  );
};

export default LandingPage;