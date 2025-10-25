import React, { useState } from 'react';
import { groupsAPI } from '../services/api';
import SocketService from '../services/socket';

const GroupCreation = ({ onGroupCreated }) => {
  const [groupName, setGroupName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await groupsAPI.createGroup({
        name: groupName,
        description: description
      });
      
      onGroupCreated(response.data.group_id);
      setGroupName('');
      setDescription('');
    } catch (error) {
      alert('Error creating group');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="group-creation">
      <h3>Create New Group</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Group Name"
          value={groupName}
          onChange={(e) => setGroupName(e.target.value)}
          required
        />
        <textarea
          placeholder="Group Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows="3"
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Creating...' : 'Create Group'}
        </button>
      </form>
    </div>
  );
};

export default GroupCreation;
