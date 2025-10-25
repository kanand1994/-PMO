import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import Login from './components/Login';
import ContactForm from './components/ContactForm';
import Dashboard from './components/Dashboard';
import GroupManagement from './components/GroupManagement';
import EventPlanner from './components/EventPlanner';
import AdminDashboard from './components/AdminDashboard';
import SocketService from './services/socket';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      setUser(JSON.parse(userData));
      SocketService.connect();
    }
    
    setLoading(false);
  }, []);

  const handleLogin = (userData, token) => {
    setUser(userData);
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    SocketService.connect();
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    SocketService.disconnect();
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner">📅</div>
        <p>Loading Plan My Outings...</p>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        {/* Authenticated App Layout */}
        {user && (
          <header className="app-header">
            <div className="header-logo">
              <span className="logo-icon">📅</span>
              <span className="logo-text">Plan My Outings</span>
            </div>
            <div className="user-info">
              <span>
                {user.username === 'superadmin' ? 
                  '🔧 Super Admin Panel' : 
                  `Welcome, ${user.first_name}!`
                }
              </span>
              <button className="logout-btn" onClick={handleLogout}>Logout</button>
            </div>
          </header>
        )}

        <Routes>
          <Route 
            path="/" 
            element={user ? (
              user.username === 'superadmin' ? 
                <Navigate to="/admin" /> : 
                <Navigate to="/dashboard" />
            ) : <LandingPage />} 
          />
          <Route 
            path="/login" 
            element={user ? <Navigate to="/dashboard" /> : <Login onLogin={handleLogin} />} 
          />
          <Route 
            path="/contact" 
            element={user ? <Navigate to="/dashboard" /> : <ContactForm />} 
          />
          <Route 
            path="/dashboard" 
            element={user ? (
              user.username === 'superadmin' ? 
                <AdminDashboard user={user} /> : 
                <Dashboard user={user} />
            ) : <Navigate to="/login" />} 
          />
          <Route 
            path="/groups" 
            element={user ? <GroupManagement user={user} /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/events" 
            element={user ? <EventPlanner user={user} /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/admin" 
            element={user ? <AdminDashboard user={user} /> : <Navigate to="/login" />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
