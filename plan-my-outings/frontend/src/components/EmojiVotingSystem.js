import React, { useState, useEffect } from 'react';
import { pollsAPI } from '../services/api';
import SocketService from '../services/socket';

const EmojiVotingSystem = ({ poll, currentUser, onVoteUpdate }) => {
  const [selectedOptions, setSelectedOptions] = useState(new Set());
  const [voteCounts, setVoteCounts] = useState({});
  const [emojiReactions, setEmojiReactions] = useState({});
  const [loading, setLoading] = useState(false);

  // Emoji options for voting
  const emojiOptions = {
    love: { emoji: '❤️', label: 'Love it!' },
    like: { emoji: '👍', label: 'Like it' },
    neutral: { emoji: '😐', label: 'Neutral' },
    dislike: { emoji: '👎', label: 'Not for me' },
    excited: { emoji: '🎉', label: 'Super excited!' },
    maybe: { emoji: '🤔', label: 'Maybe...' }
  };

  useEffect(() => {
    // Initialize vote counts
    if (poll && poll.options) {
      const initialCounts = {};
      poll.options.forEach(option => {
        initialCounts[option.id] = option.vote_count || 0;
      });
      setVoteCounts(initialCounts);
    }

    // Listen for real-time vote updates
    SocketService.onEvent('vote_update', (data) => {
      setVoteCounts(prev => ({
        ...prev,
        [data.option_id]: data.vote_count
      }));
      
      if (onVoteUpdate) {
        onVoteUpdate(data);
      }
    });

    SocketService.onEvent('emoji_reaction', (data) => {
      setEmojiReactions(prev => ({
        ...prev,
        [data.option_id]: {
          ...prev[data.option_id],
          [data.emoji]: (prev[data.option_id]?.[data.emoji] || 0) + 1
        }
      }));
    });

    return () => {
      SocketService.offEvent('vote_update');
      SocketService.offEvent('emoji_reaction');
    };
  }, [poll, onVoteUpdate]);

  const castVote = async (optionId, voteType = 'standard') => {
    if (loading) return;
    
    setLoading(true);
    try {
      await pollsAPI.castVote(poll.id, { 
        option_id: optionId,
        vote_type: voteType
      });
      
      if (poll.poll_type === 'single') {
        setSelectedOptions(new Set([optionId]));
      } else {
        setSelectedOptions(prev => {
          const newSet = new Set(prev);
          if (newSet.has(optionId)) {
            newSet.delete(optionId);
          } else {
            newSet.add(optionId);
          }
          return newSet;
        });
      }
      
      SocketService.castVote(poll.id, optionId, currentUser.id);
    } catch (error) {
      console.error('Error casting vote:', error);
      alert('Error casting vote. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const addEmojiReaction = async (optionId, emojiKey) => {
    try {
      // Emit emoji reaction via socket
      SocketService.emit('emoji_reaction', {
        poll_id: poll.id,
        option_id: optionId,
        emoji: emojiKey,
        user_id: currentUser.id
      });
      
      // Update local state optimistically
      setEmojiReactions(prev => ({
        ...prev,
        [optionId]: {
          ...prev[optionId],
          [emojiKey]: (prev[optionId]?.[emojiKey] || 0) + 1
        }
      }));
    } catch (error) {
      console.error('Error adding emoji reaction:', error);
    }
  };

  const getVotePercentage = (optionId) => {
    const totalVotes = Object.values(voteCounts).reduce((sum, count) => sum + count, 0);
    if (totalVotes === 0) return 0;
    return Math.round((voteCounts[optionId] || 0) / totalVotes * 100);
  };

  if (!poll || !poll.options) {
    return (
      <div className="voting-system">
        <p>No poll data available</p>
      </div>
    );
  }

  return (
    <div className="emoji-voting-system">
      <div className="poll-header">
        <h3 className="poll-question">{poll.question}</h3>
        <span className="poll-type-badge">
          {poll.poll_type === 'single' ? '🎯 Single Choice' : '✅ Multiple Choice'}
        </span>
      </div>
      
      <div className="vote-options">
        {poll.options.map(option => {
          const isSelected = selectedOptions.has(option.id);
          const voteCount = voteCounts[option.id] || 0;
          const percentage = getVotePercentage(option.id);
          
          return (
            <div key={option.id} className={`vote-option ${isSelected ? 'selected' : ''}`}>
              <div className="option-header">
                <h4 className="option-title">{option.title}</h4>
                <div className="vote-stats">
                  <span className="vote-count">{voteCount} votes</span>
                  <span className="vote-percentage">({percentage}%)</span>
                </div>
              </div>
              
              {option.description && (
                <p className="option-description">{option.description}</p>
              )}
              
              <div className="vote-progress">
                <div 
                  className="progress-bar" 
                  style={{ width: `${percentage}%` }}
                />
              </div>
              
              <div className="voting-actions">
                <button
                  className={`vote-btn ${isSelected ? 'voted' : ''}`}
                  onClick={() => castVote(option.id)}
                  disabled={loading || (poll.poll_type === 'single' && selectedOptions.size > 0 && !isSelected)}
                >
                  {loading ? '⏳' : isSelected ? '✅ Voted' : '🗳️ Vote'}
                </button>
                
                <div className="emoji-reactions">
                  {Object.entries(emojiOptions).map(([key, { emoji, label }]) => (
                    <button
                      key={key}
                      className="emoji-btn"
                      onClick={() => addEmojiReaction(option.id, key)}
                      title={label}
                    >
                      {emoji}
                      {emojiReactions[option.id]?.[key] && (
                        <span className="emoji-count">
                          {emojiReactions[option.id][key]}
                        </span>
                      )}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>
      
      <div className="poll-footer">
        <p className="poll-info">
          Total votes: {Object.values(voteCounts).reduce((sum, count) => sum + count, 0)}
        </p>
        {poll.poll_type === 'multiple' && (
          <p className="poll-hint">💡 You can vote for multiple options</p>
        )}
      </div>
    </div>
  );
};

export default EmojiVotingSystem;