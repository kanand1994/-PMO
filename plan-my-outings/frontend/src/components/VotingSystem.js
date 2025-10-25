import React, { useState, useEffect } from 'react';
import { pollsAPI } from '../services/api';
import SocketService from '../services/socket';

const VotingSystem = ({ poll, currentUser }) => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [voteCounts, setVoteCounts] = useState({});

  useEffect(() => {
    SocketService.onEvent('vote_update', (data) => {
      setVoteCounts(prev => ({
        ...prev,
        [data.option_id]: data.vote_count
      }));
    });

    return () => {
      SocketService.offEvent('vote_update');
    };
  }, []);

  const castVote = async (optionId) => {
    try {
      await pollsAPI.castVote(poll.id, { option_id: optionId });
      setSelectedOption(optionId);
      
      SocketService.castVote(poll.id, optionId, currentUser.id);
    } catch (error) {
      alert('Error casting vote');
    }
  };

  return (
    <div className="voting-system">
      <h4>{poll.question}</h4>
      
      <div className="vote-options">
        {poll.options.map(option => (
          <div key={option.id} className="vote-option">
            <button
              onClick={() => castVote(option.id)}
              disabled={selectedOption !== null}
              className={selectedOption === option.id ? 'selected' : ''}
            >
              {option.title}
            </button>
            <span className="vote-count">
              {voteCounts[option.id] || 0} votes
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default VotingSystem;
