import React, { useState, useEffect } from 'react';
import { groupsAPI } from '../services/api';
import EmojiVotingSystem from './EmojiVotingSystem';
import './EmojiVotingSystem.css';

const Dashboard = ({ user }) => {
    const [groups, setGroups] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchGroups();
    }, []);

    const fetchGroups = async () => {
        try {
            const response = await groupsAPI.getGroups();
            setGroups(response.data);
        } catch (error) {
            console.error('Error fetching groups:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dashboard">
            <div className="dashboard-container">
                <div className="dashboard-header">
                    <h1>Welcome back, {user.first_name}! 👋</h1>
                    <p>Ready to plan some amazing outings?</p>
                </div>

                <div className="dashboard-stats">
                    <div className="stat-card">
                        <div className="stat-icon">👥</div>
                        <div className="stat-content">
                            <h3>Your Groups</h3>
                            <p className="stat-number">{groups.length}</p>
                        </div>
                    </div>

                    <div className="stat-card">
                        <div className="stat-icon">📅</div>
                        <div className="stat-content">
                            <h3>Active Events</h3>
                            <p className="stat-number">0</p>
                        </div>
                    </div>

                    <div className="stat-card">
                        <div className="stat-icon">🎉</div>
                        <div className="stat-content">
                            <h3>Upcoming Plans</h3>
                            <p className="stat-number">0</p>
                        </div>
                    </div>
                </div>

                <div className="dashboard-content">
                    <div className="recent-groups">
                        <div className="section-header">
                            <h3>Your Groups</h3>
                            <button
                                className="btn-secondary"
                                onClick={() => window.location.href = '/groups'}
                            >
                                Manage All
                            </button>
                        </div>

                        {loading ? (
                            <div className="loading-state">
                                <span className="loading-spinner">📅</span>
                                <p>Loading groups...</p>
                            </div>
                        ) : groups.length > 0 ? (
                            <div className="groups-grid">
                                {groups.slice(0, 3).map(group => (
                                    <div key={group.id} className="group-card">
                                        <div className="group-header">
                                            <h4>{group.name}</h4>
                                            <span className="member-badge">{group.member_count} members</span>
                                        </div>
                                        <p className="group-description">
                                            {group.description || 'No description provided'}
                                        </p>
                                        <div className="group-actions">
                                            <button className="btn-primary btn-sm">View Details</button>
                                            <button className="btn-secondary btn-sm">Plan Event</button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="empty-state">
                                <div className="empty-icon">👥</div>
                                <h4>No groups yet</h4>
                                <p>Create your first group to start planning amazing outings!</p>
                                <button
                                    className="btn-primary"
                                    onClick={() => window.location.href = '/groups'}
                                >
                                    Create First Group
                                </button>
                            </div>
                        )}
                    </div>

                    <div className="quick-actions">
                        <h3>Quick Actions</h3>
                        <div className="action-grid">
                            <div className="action-card" onClick={() => window.location.href = '/groups'}>
                                <div className="action-icon">👥</div>
                                <h4>Manage Groups</h4>
                                <p>Create and organize your friend groups</p>
                            </div>

                            <div className="action-card" onClick={() => window.location.href = '/events'}>
                                <div className="action-icon">📅</div>
                                <h4>Plan Event</h4>
                                <p>Start planning your next outing</p>
                            </div>

                            <div className="action-card" onClick={() => alert('Voting system demo below!')}>
                                <div className="action-icon">🗳️</div>
                                <h4>View Polls</h4>
                                <p>Check ongoing group decisions</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Demo Emoji Voting System */}
                <div className="demo-voting-section">
                    <h3>🎉 Demo: Emoji Voting System</h3>
                    <EmojiVotingSystem 
                        poll={{
                            id: 'demo-poll',
                            question: "Where should we go for our weekend outing?",
                            poll_type: 'multiple',
                            options: [
                                {
                                    id: 1,
                                    title: "🎬 Movie Theater",
                                    description: "Watch the latest blockbuster movie",
                                    vote_count: 5
                                },
                                {
                                    id: 2,
                                    title: "🍕 Pizza Place",
                                    description: "Grab some delicious pizza and hang out",
                                    vote_count: 8
                                },
                                {
                                    id: 3,
                                    title: "🏞️ Nature Park",
                                    description: "Enjoy the outdoors and fresh air",
                                    vote_count: 3
                                },
                                {
                                    id: 4,
                                    title: "🎮 Gaming Cafe",
                                    description: "Play games and have some fun",
                                    vote_count: 6
                                }
                            ]
                        }}
                        currentUser={user}
                        onVoteUpdate={(data) => console.log('Vote update:', data)}
                    />
                </div>
            </div>
        </div>
    );
};

const
    styles = `
.dashboard {
  min-height: calc(100vh - 80px);
  background: #f8f9fa;
  padding: 2rem;
}

.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.dashboard-header p {
  color: #666;
  font-size: 1.1rem;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 2.5rem;
  background: #ff6b6b;
  color: white;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content h3 {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h3 {
  font-size: 1.3rem;
  color: #333;
}

.recent-groups {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.loading-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.loading-spinner {
  font-size: 2rem;
  animation: spin 2s linear infinite;
  display: block;
  margin-bottom: 1rem;
}

.groups-grid {
  display: grid;
  gap: 1rem;
}

.group-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
}

.group-card:hover {
  border-color: #ff6b6b;
  box-shadow: 0 2px 8px rgba(255, 107, 107, 0.1);
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.group-header h4 {
  color: #333;
  margin: 0;
}

.member-badge {
  background: #f0f0f0;
  color: #666;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.group-description {
  color: #666;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.group-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.8rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h4 {
  color: #333;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #666;
  margin-bottom: 1.5rem;
}

.quick-actions {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.quick-actions h3 {
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.action-grid {
  display: grid;
  gap: 1rem;
}

.action-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.action-card:hover {
  border-color: #ff6b6b;
  box-shadow: 0 2px 8px rgba(255, 107, 107, 0.1);
  transform: translateY(-1px);
}

.action-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.action-card h4 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.action-card p {
  color: #666;
  font-size: 0.8rem;
  margin: 0;
}

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }
  
  .dashboard-header h1 {
    font-size: 2rem;
  }
  
  .dashboard-stats {
    grid-template-columns: 1fr;
  }
  
  .dashboard-content {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
}

/* Demo Voting Section Styles */
.demo-voting-section {
  margin-top: 2rem;
  grid-column: 1 / -1;
}

.demo-voting-section h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
  text-align: center;
}

@media (max-width: 768px) {
  .demo-voting-section {
    margin-top: 1rem;
  }
}
`;

// Inject styles
if (typeof document !== 'undefined') {
    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);
}

export default Dashboard;