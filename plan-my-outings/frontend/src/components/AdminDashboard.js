import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdminDashboard = ({ user }) => {
  const [stats, setStats] = useState({
    totals: { users: 0, groups: 0, events: 0, enquiries: 0 },
    recent: { users: 0, groups: 0, events: 0, enquiries: 0 }
  });
  const [recentUsers, setRecentUsers] = useState([]);
  const [systemActivity, setSystemActivity] = useState({
    recent_groups: [],
    recent_events: [],
    recent_enquiries: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user && user.username === 'superadmin') {
      fetchAdminData();
    }
  }, [user]);

  const fetchAdminData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      
      // Fetch admin statistics
      const statsResponse = await axios.get('http://localhost:5000/api/admin/stats', { headers });
      setStats(statsResponse.data);
      
      // Fetch recent users
      const usersResponse = await axios.get('http://localhost:5000/api/admin/recent-users', { headers });
      setRecentUsers(usersResponse.data);
      
      // Fetch system activity
      const activityResponse = await axios.get('http://localhost:5000/api/admin/system-activity', { headers });
      setSystemActivity(activityResponse.data);
      
    } catch (error) {
      console.error('Error fetching admin data:', error);
      // Fallback to demo data if API fails
      setStats({
        totals: { users: 0, groups: 0, events: 0, enquiries: 0 },
        recent: { users: 0, groups: 0, events: 0, enquiries: 0 }
      });
    } finally {
      setLoading(false);
    }
  };

  if (!user || user.username !== 'superadmin') {
    return (
      <div className="admin-access-denied">
        <h2>🚫 Access Denied</h2>
        <p>Super Admin access required.</p>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      <div className="admin-header">
        <h1>🔧 Super Admin Dashboard</h1>
        <p>Welcome, {user.first_name}! You have full system access.</p>
      </div>

      <div className="admin-stats">
        <div className="stat-card admin">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h3>Total Users</h3>
            <p className="stat-number">{stats.totals.users}</p>
            <span className="stat-recent">+{stats.recent.users} this week</span>
          </div>
        </div>

        <div className="stat-card admin">
          <div className="stat-icon">🏠</div>
          <div className="stat-content">
            <h3>Total Groups</h3>
            <p className="stat-number">{stats.totals.groups}</p>
            <span className="stat-recent">+{stats.recent.groups} this week</span>
          </div>
        </div>

        <div className="stat-card admin">
          <div className="stat-icon">📅</div>
          <div className="stat-content">
            <h3>Total Events</h3>
            <p className="stat-number">{stats.totals.events}</p>
            <span className="stat-recent">+{stats.recent.events} this week</span>
          </div>
        </div>

        <div className="stat-card admin">
          <div className="stat-icon">📝</div>
          <div className="stat-content">
            <h3>Enquiries</h3>
            <p className="stat-number">{stats.totals.enquiries}</p>
            <span className="stat-recent">+{stats.recent.enquiries} this week</span>
          </div>
        </div>
      </div>

      <div className="admin-content">
        <div className="admin-section">
          <h3>🔧 Admin Tools</h3>
          <div className="admin-tools">
            <button className="admin-btn" onClick={() => alert('CLI Tool: Run backend/run_admin_cli.bat')}>
              💻 CLI Database Tool
            </button>
            <button className="admin-btn" onClick={() => alert('Email system configured')}>
              📧 Email System
            </button>
            <button className="admin-btn" onClick={() => alert('System logs available in backend console')}>
              📊 System Logs
            </button>
            <button className="admin-btn" onClick={() => alert('Database backup feature in CLI')}>
              💾 Backup Database
            </button>
          </div>
        </div>

        <div className="admin-section">
          <h3>👥 Recent Users</h3>
          <div className="recent-users-admin">
            {loading ? (
              <p>Loading users...</p>
            ) : recentUsers.length > 0 ? (
              recentUsers.slice(0, 5).map(user => (
                <div key={user.id} className="user-card-admin">
                  <div className="user-info">
                    <h4>{user.name}</h4>
                    <p>{user.email}</p>
                    <span className="user-date">
                      Joined: {user.created_at} | Groups: {user.groups_count} | Events: {user.events_count}
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <p>No recent users</p>
            )}
          </div>
        </div>

        <div className="admin-section">
          <h3>🏠 Recent Groups</h3>
          <div className="recent-activity">
            {loading ? (
              <p>Loading groups...</p>
            ) : systemActivity.recent_groups.length > 0 ? (
              systemActivity.recent_groups.map(group => (
                <div key={group.id} className="activity-item">
                  <h4>{group.name}</h4>
                  <p>Created by: {group.creator} | Members: {group.members}</p>
                  <span className="activity-date">{group.created_at}</span>
                </div>
              ))
            ) : (
              <p>No recent groups</p>
            )}
          </div>
        </div>

        <div className="admin-section">
          <h3>📅 Recent Events</h3>
          <div className="recent-activity">
            {loading ? (
              <p>Loading events...</p>
            ) : systemActivity.recent_events.length > 0 ? (
              systemActivity.recent_events.map(event => (
                <div key={event.id} className="activity-item">
                  <h4>{event.title}</h4>
                  <p>Type: {event.type} | Group: {event.group} | Creator: {event.creator}</p>
                  <span className="activity-date">{event.created_at}</span>
                </div>
              ))
            ) : (
              <p>No recent events</p>
            )}
          </div>
        </div>

        <div className="admin-section">
          <h3>📝 Recent Enquiries</h3>
          <div className="recent-activity">
            {loading ? (
              <p>Loading enquiries...</p>
            ) : systemActivity.recent_enquiries.length > 0 ? (
              systemActivity.recent_enquiries.map(enquiry => (
                <div key={enquiry.id} className="activity-item">
                  <h4>{enquiry.name}</h4>
                  <p>{enquiry.email}</p>
                  <p className="enquiry-message">{enquiry.message}</p>
                  <span className="activity-date">{enquiry.created_at}</span>
                </div>
              ))
            ) : (
              <p>No recent enquiries</p>
            )}
          </div>
        </div>

        <div className="admin-section">
          <h3>⚙️ System Information</h3>
          <div className="system-info">
            <div className="info-item">
              <strong>Super Admin:</strong> {user.username}
            </div>
            <div className="info-item">
              <strong>Email System:</strong> Configured (planmyouting@outlook.com)
            </div>
            <div className="info-item">
              <strong>CLI Access:</strong> Available via run_admin_cli.bat
            </div>
            <div className="info-item">
              <strong>Database:</strong> SQLite (plan_my_outings.db)
            </div>
            <div className="info-item">
              <strong>Notifications:</strong> Sent to planmyouting@outlook.com
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;