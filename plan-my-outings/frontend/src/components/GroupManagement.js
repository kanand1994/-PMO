import React, { useState, useEffect } from 'react';
import { groupsAPI } from '../services/api';

const GroupManagement = ({ user }) => {
  const [groups, setGroups] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newGroup, setNewGroup] = useState({
    name: '',
    description: ''
  });
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

  const handleCreateGroup = async (e) => {
    e.preventDefault();
    try {
      await groupsAPI.createGroup(newGroup);
      setNewGroup({ name: '', description: '' });
      setShowCreateForm(false);
      fetchGroups(); // Refresh the list
      alert('Group created successfully!');
    } catch (error) {
      alert('Error creating group. Please try again.');
    }
  };

  const handleInputChange = (e) => {
    setNewGroup({
      ...newGroup,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="group-management">
      <div className="header">
        <h2>Group Management</h2>
        <button 
          className="create-btn"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'Cancel' : 'Create New Group'}
        </button>
      </div>

      {showCreateForm && (
        <div className="create-group-form">
          <h3>Create New Group</h3>
          <form onSubmit={handleCreateGroup}>
            <div className="form-group">
              <input
                type="text"
                name="name"
                placeholder="Group Name"
                value={newGroup.name}
                onChange={handleInputChange}
                required
              />
            </div>
            
            <div className="form-group">
              <textarea
                name="description"
                placeholder="Group Description (Optional)"
                value={newGroup.description}
                onChange={handleInputChange}
                rows="3"
              />
            </div>
            
            <div className="form-actions">
              <button type="submit">Create Group</button>
              <button 
                type="button" 
                onClick={() => setShowCreateForm(false)}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="groups-section">
        <h3>Your Groups</h3>
        {loading ? (
          <p>Loading groups...</p>
        ) : groups.length > 0 ? (
          <div className="groups-grid">
            {groups.map(group => (
              <div key={group.id} className="group-card">
                <div className="group-header">
                  <h4>{group.name}</h4>
                  <span className="member-count">{group.member_count} members</span>
                </div>
                
                <p className="group-description">
                  {group.description || 'No description provided'}
                </p>
                
                <div className="group-actions">
                  <button onClick={() => alert('View details coming soon!')}>
                    View Details
                  </button>
                  <button onClick={() => alert('Plan event coming soon!')}>
                    Plan Event
                  </button>
                  <button onClick={() => alert('Manage members coming soon!')}>
                    Manage Members
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-groups">
            <p>You haven't created or joined any groups yet.</p>
            <p>Create your first group to start planning outings with friends!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default GroupManagement;