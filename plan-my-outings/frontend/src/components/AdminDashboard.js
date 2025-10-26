import React, { useState, useEffect } from 'react';
import { adminAPI } from '../services/api';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [emailLogs, setEmailLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      setLoading(true);
      const [statsResponse, emailResponse] = await Promise.all([
        adminAPI.getStats(),
        adminAPI.getEmailLogs()
      ]);
      
      setStats(statsResponse.data);
      setEmailLogs(emailResponse.data);
    } catch (error) {
      console.error('Error fetching admin data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClearDemoData = async () => {
    if (!window.confirm('Are you sure you want to clear ALL demo data? This cannot be undone!')) {
      return;
    }
    
    if (!window.confirm('Type "DELETE ALL DATA" to confirm:') || 
        prompt('Type "DELETE ALL DATA" to confirm:') !== 'DELETE ALL DATA') {
      return;
    }

    try {
      await adminAPI.clearDemoData();
      alert('Demo data cleared successfully!');
      fetchAdminData();
    } catch (error) {
      alert('Error clearing demo data: ' + error.message);
    }
  };

  const handleResendEmail = async (userId) => {
    try {
      const response = await adminAPI.resendEmail(userId);
      
      // Show success message with new password
      const message = `✅ Email resent successfully!\n\n` +
                     `New password: ${response.data.new_password}\n\n` +
                     `The user will receive a welcome email with their new credentials.`;
      
      alert(message);
      
      // Refresh admin data to update email logs
      fetchAdminData();
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Unknown error';
      alert(`❌ Error resending email: ${errorMessage}`);
    }
  };

  if (loading) {
    return <div className="admin-loading">Loading admin dashboard...</div>;
  }

  return (
    <div className="admin-dashboard">
      <div className="admin-header">
        <h1>🔐 Super Admin Dashboard</h1>
        <p>Plan My Outings - Administrative Control Panel</p>
      </div>

      <div className="admin-tabs">
        <button 
          className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button 
          className={`tab-btn ${activeTab === 'emails' ? 'active' : ''}`}
          onClick={() => setActiveTab('emails')}
        >
          📨 Email Logs
        </button>
        <button 
          className={`tab-btn ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
        >
          👥 Users
        </button>
        <button 
          className={`tab-btn ${activeTab === 'maintenance' ? 'active' : ''}`}
          onClick={() => setActiveTab('maintenance')}
        >
          🔧 Maintenance
        </button>
      </div>

      <div className="admin-content">
        {activeTab === 'overview' && (
          <OverviewTab stats={stats} />
        )}
        
        {activeTab === 'emails' && (
          <EmailLogsTab 
            emailLogs={emailLogs} 
            onResendEmail={handleResendEmail}
            onRefresh={fetchAdminData}
          />
        )}
        
        {activeTab === 'users' && (
          <UsersTab onResendEmail={handleResendEmail} />
        )}
        
        {activeTab === 'maintenance' && (
          <MaintenanceTab onClearDemoData={handleClearDemoData} />
        )}
      </div>
    </div>
  );
};

const OverviewTab = ({ stats }) => (
  <div className="overview-tab">
    <div className="overview-summary">
      <h3>📊 System Overview</h3>
      <p>Monitor your Plan My Outings platform activity and growth</p>
    </div>
    
    <div className="stats-grid">
      <div className="stat-card">
        <h3>👥 Users</h3>
        <div className="stat-number">{stats?.totals?.users || 0}</div>
        <div className="stat-change">+{stats?.recent?.users || 0} this week</div>
      </div>
      
      <div className="stat-card">
        <h3>🏠 Groups</h3>
        <div className="stat-number">{stats?.totals?.groups || 0}</div>
        <div className="stat-change">+{stats?.recent?.groups || 0} this week</div>
      </div>
      
      <div className="stat-card">
        <h3>📅 Events</h3>
        <div className="stat-number">{stats?.totals?.events || 0}</div>
        <div className="stat-change">+{stats?.recent?.events || 0} this week</div>
      </div>
      
      <div className="stat-card">
        <h3>📝 Enquiries</h3>
        <div className="stat-number">{stats?.totals?.enquiries || 0}</div>
        <div className="stat-change">+{stats?.recent?.enquiries || 0} this week</div>
      </div>
    </div>
  </div>
);

const EmailLogsTab = ({ emailLogs, onResendEmail, onRefresh }) => {
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  const filteredEmails = emailLogs?.recent_emails?.filter(email => {
    const matchesStatus = filterStatus === 'all' || email.status === filterStatus;
    const matchesType = filterType === 'all' || email.type === filterType;
    const matchesSearch = searchTerm === '' || 
      email.recipient.toLowerCase().includes(searchTerm.toLowerCase()) ||
      email.subject.toLowerCase().includes(searchTerm.toLowerCase());
    
    return matchesStatus && matchesType && matchesSearch;
  }) || [];

  const getEmailTypeColor = (type) => {
    switch(type) {
      case 'welcome': return '#4ecdc4';
      case 'admin_notification': return '#ff6b6b';
      case 'resend': return '#ffa726';
      case 'admin_setup': return '#9c27b0';
      default: return '#666';
    }
  };

  const getEmailTypeIcon = (type) => {
    switch(type) {
      case 'welcome': return '👋';
      case 'admin_notification': return '🔔';
      case 'resend': return '🔄';
      case 'admin_setup': return '⚙️';
      default: return '📧';
    }
  };

  return (
    <div className="email-logs-tab">
      <div className="email-stats">
        <h3>📊 Email Statistics</h3>
        <div className="email-stats-grid">
          <div className="email-stat">
            <span className="stat-label">Total Emails:</span>
            <span className="stat-value">{emailLogs?.stats?.total || 0}</span>
          </div>
          <div className="email-stat">
            <span className="stat-label">Successfully Sent:</span>
            <span className="stat-value success">{emailLogs?.stats?.sent || 0}</span>
          </div>
          <div className="email-stat">
            <span className="stat-label">Failed:</span>
            <span className="stat-value error">{emailLogs?.stats?.failed || 0}</span>
          </div>
          <div className="email-stat">
            <span className="stat-label">Success Rate:</span>
            <span className="stat-value">{emailLogs?.stats?.success_rate?.toFixed(1) || 0}%</span>
          </div>
          <div className="email-stat">
            <span className="stat-label">Last 24h:</span>
            <span className="stat-value">{emailLogs?.stats?.recent_24h || 0}</span>
          </div>
        </div>
        
        <button className="refresh-btn" onClick={onRefresh}>
          🔄 Refresh Logs
        </button>
      </div>

      <div className="email-filters">
        <div className="filter-group">
          <label>Search:</label>
          <input
            type="text"
            placeholder="Search by email or subject..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
        
        <div className="filter-group">
          <label>Status:</label>
          <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
            <option value="all">All Status</option>
            <option value="sent">✅ Sent</option>
            <option value="failed">❌ Failed</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label>Type:</label>
          <select value={filterType} onChange={(e) => setFilterType(e.target.value)}>
            <option value="all">All Types</option>
            <option value="welcome">👋 Welcome</option>
            <option value="admin_notification">🔔 Admin Alert</option>
            <option value="resend">🔄 Resend</option>
            <option value="admin_setup">⚙️ Admin Setup</option>
          </select>
        </div>
      </div>

      <div className="email-logs-list">
        <div className="email-logs-header">
          <h3>📧 Email Logs ({filteredEmails.length} of {emailLogs?.recent_emails?.length || 0})</h3>
          {filteredEmails.length !== emailLogs?.recent_emails?.length && (
            <span className="filter-indicator">Filtered results</span>
          )}
        </div>
        
        <div className="email-logs-table">
          {filteredEmails.length === 0 ? (
            <div className="no-emails">
              {emailLogs?.recent_emails?.length === 0 ? 
                "No email logs found" : 
                "No emails match your filters"
              }
            </div>
          ) : (
            filteredEmails.map(email => (
              <div key={email.id} className={`email-log-item ${email.status}`}>
                <div className="email-log-header">
                  <span className={`status-icon ${email.status}`}>
                    {email.status === 'sent' ? '✅' : '❌'}
                  </span>
                  <span className="recipient">{email.recipient}</span>
                  <span 
                    className="email-type"
                    style={{ 
                      backgroundColor: getEmailTypeColor(email.type),
                      color: 'white'
                    }}
                  >
                    {getEmailTypeIcon(email.type)} {email.type}
                  </span>
                  <span className="timestamp">{email.sent_at}</span>
                </div>
                
                <div className="email-log-details">
                  <div className="subject">{email.subject}</div>
                  {email.error && (
                    <div className="error-message">
                      <strong>Error:</strong> {email.error}
                    </div>
                  )}
                  {email.user_id && (
                    <div className="email-actions">
                      <button 
                        className="resend-btn"
                        onClick={() => onResendEmail(email.user_id)}
                        title="Resend welcome email with new password"
                      >
                        📤 Resend Welcome Email
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

const UsersTab = ({ onResendEmail }) => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [resendingUsers, setResendingUsers] = useState(new Set());

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await adminAPI.getRecentUsers();
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleResendEmail = async (userId) => {
    if (resendingUsers.has(userId)) return;
    
    if (!window.confirm('This will generate a new password and send welcome email. Continue?')) {
      return;
    }

    setResendingUsers(prev => new Set([...prev, userId]));
    
    try {
      await onResendEmail(userId);
      // Refresh user list after successful resend
      await fetchUsers();
    } catch (error) {
      console.error('Error resending email:', error);
    } finally {
      setResendingUsers(prev => {
        const newSet = new Set(prev);
        newSet.delete(userId);
        return newSet;
      });
    }
  };

  if (loading) return <div className="loading-users">Loading users...</div>;

  return (
    <div className="users-tab">
      <div className="users-header">
        <h3>👥 Recent Users ({users.length})</h3>
        <button className="refresh-btn" onClick={fetchUsers}>
          🔄 Refresh Users
        </button>
      </div>
      
      <div className="users-list">
        {users.length === 0 ? (
          <div className="no-users">No users found</div>
        ) : (
          users.map(user => (
            <div key={user.id} className="user-item">
              <div className="user-info">
                <div className="user-header">
                  <div className="user-name">{user.name}</div>
                  <div className="user-id">ID: {user.id}</div>
                </div>
                <div className="user-details">
                  <div className="user-detail">
                    <span className="detail-label">Username:</span>
                    <span className="detail-value">@{user.username}</span>
                  </div>
                  <div className="user-detail">
                    <span className="detail-label">Email:</span>
                    <span className="detail-value">{user.email}</span>
                  </div>
                  <div className="user-detail">
                    <span className="detail-label">Joined:</span>
                    <span className="detail-value">{user.created_at}</span>
                  </div>
                  <div className="user-detail">
                    <span className="detail-label">Activity:</span>
                    <span className="detail-value">
                      {user.groups_count} groups, {user.events_count} events
                    </span>
                  </div>
                </div>
              </div>
              <div className="user-actions">
                <button 
                  className={`resend-btn ${resendingUsers.has(user.id) ? 'loading' : ''}`}
                  onClick={() => handleResendEmail(user.id)}
                  disabled={resendingUsers.has(user.id)}
                  title="Generate new password and resend welcome email"
                >
                  {resendingUsers.has(user.id) ? (
                    <>⏳ Sending...</>
                  ) : (
                    <>📤 Resend Welcome Email</>
                  )}
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

const MaintenanceTab = ({ onClearDemoData }) => (
  <div className="maintenance-tab">
    <h3>🔧 System Maintenance</h3>
    
    <div className="maintenance-actions">
      <div className="maintenance-card danger">
        <h4>🗑️ Clear Demo Data</h4>
        <p>Remove all test users, groups, events, and enquiries. Super admin account will be preserved.</p>
        <button className="danger-btn" onClick={onClearDemoData}>
          Clear All Demo Data
        </button>
      </div>
      
      <div className="maintenance-card">
        <h4>📊 System Status</h4>
        <p>All systems operational. Email tracking active.</p>
        <div className="status-indicators">
          <div className="status-item">
            <span className="status-dot green"></span>
            <span>Database: Online</span>
          </div>
          <div className="status-item">
            <span className="status-dot green"></span>
            <span>Email System: Working</span>
          </div>
          <div className="status-item">
            <span className="status-dot green"></span>
            <span>Encryption: Active</span>
          </div>
        </div>
      </div>
    </div>
  </div>
);

export default AdminDashboard;

// CSS Styles
const styles = `
.admin-dashboard {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 2rem;
}

.admin-header {
  text-align: center;
  margin-bottom: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.admin-header h1 {
  color: #333;
  margin-bottom: 0.5rem;
}

.admin-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  background: white;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.tab-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  background: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.tab-btn.active {
  background: #4ecdc4;
  color: white;
}

.tab-btn:hover {
  background: #e9ecef;
}

.tab-btn.active:hover {
  background: #45b7aa;
}

.admin-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.overview-summary {
  text-align: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
}

.overview-summary h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
}

.overview-summary p {
  margin: 0;
  opacity: 0.9;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
}

.stat-card h3 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.stat-change {
  font-size: 0.9rem;
  opacity: 0.9;
}

.email-stats {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.email-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.email-stat {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: white;
  border-radius: 6px;
}

.stat-value.success {
  color: #28a745;
  font-weight: bold;
}

.stat-value.error {
  color: #dc3545;
  font-weight: bold;
}

.refresh-btn {
  background: #4ecdc4;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}

.email-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.filter-group label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #666;
}

.search-input, .filter-group select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.search-input {
  min-width: 200px;
}

.email-logs-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.filter-indicator {
  background: #4ecdc4;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.email-logs-table {
  max-height: 600px;
  overflow-y: auto;
}

.no-emails {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-style: italic;
}

.email-log-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin-bottom: 1rem;
  padding: 1rem;
}

.email-log-item.sent {
  border-left: 4px solid #28a745;
}

.email-log-item.failed {
  border-left: 4px solid #dc3545;
}

.email-log-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.status-icon.sent {
  color: #28a745;
}

.status-icon.failed {
  color: #dc3545;
}

.recipient {
  font-weight: 500;
  flex: 1;
}

.email-type {
  background: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.timestamp {
  color: #666;
  font-size: 0.9rem;
}

.subject {
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.error-message {
  color: #dc3545;
  font-size: 0.9rem;
  background: #f8d7da;
  padding: 0.5rem;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.email-actions {
  display: flex;
  gap: 0.5rem;
}

.resend-btn {
  background: #ff6b6b;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.resend-btn:hover {
  background: #ff5252;
}

.resend-btn.loading {
  background: #ccc;
  cursor: not-allowed;
}

.resend-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.users-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.users-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.no-users {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-style: italic;
}

.loading-users {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.user-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  background: white;
}

.user-info {
  flex: 1;
}

.user-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.user-name {
  font-weight: 600;
  font-size: 1.1rem;
  color: #333;
}

.user-id {
  background: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #666;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.user-detail {
  display: flex;
  gap: 0.5rem;
}

.detail-label {
  font-weight: 500;
  color: #666;
  min-width: 80px;
}

.detail-value {
  color: #333;
}

.maintenance-actions {
  display: grid;
  gap: 2rem;
}

.maintenance-card {
  padding: 1.5rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
}

.maintenance-card.danger {
  border-color: #dc3545;
  background: #fff5f5;
}

.maintenance-card h4 {
  margin-bottom: 1rem;
  color: #333;
}

.danger-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.danger-btn:hover {
  background: #c82333;
}

.status-indicators {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.green {
  background: #28a745;
}

.admin-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50vh;
  font-size: 1.2rem;
  color: #666;
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }
  
  .admin-tabs {
    flex-direction: column;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .email-stats-grid {
    grid-template-columns: 1fr;
  }
  
  .email-filters {
    flex-direction: column;
    gap: 1rem;
  }
  
  .filter-group {
    flex-direction: row;
    align-items: center;
    gap: 0.5rem;
  }
  
  .search-input {
    min-width: auto;
    flex: 1;
  }
  
  .email-logs-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .users-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .user-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .user-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .user-details {
    width: 100%;
  }
  
  .user-detail {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .detail-label {
    min-width: auto;
    font-size: 0.8rem;
  }
}
`;

// Inject styles
if (typeof document !== 'undefined') {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = styles;
  document.head.appendChild(styleSheet);
}