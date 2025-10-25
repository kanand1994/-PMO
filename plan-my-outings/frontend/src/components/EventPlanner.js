import React, { useState, useEffect } from 'react';
import { eventsAPI, placesAPI, moviesAPI, weatherAPI } from '../services/api';
import SocketService from '../services/socket';

const EventPlanner = ({ groupId }) => {
  const [eventData, setEventData] = useState({
    title: '',
    description: '',
    event_type: 'dinner'
  });
  const [suggestions, setSuggestions] = useState({
    places: [],
    movies: [],
    weather: []
  });
  const [loading, setLoading] = useState(false);

  const searchPlaces = async (query) => {
    try {
      const response = await placesAPI.searchPlaces(query, '40.7128,-74.0060');
      setSuggestions(prev => ({ ...prev, places: response.data }));
    } catch (error) {
      console.error('Error searching places:', error);
    }
  };

  const searchMovies = async (query) => {
    try {
      const response = await moviesAPI.searchMovies(query);
      setSuggestions(prev => ({ ...prev, movies: response.data }));
    } catch (error) {
      console.error('Error searching movies:', error);
    }
  };

  const getWeather = async (lat, lon) => {
    try {
      const response = await weatherAPI.getForecast(lat, lon);
      setSuggestions(prev => ({ ...prev, weather: response.data }));
    } catch (error) {
      console.error('Error fetching weather:', error);
    }
  };

  const createEvent = async () => {
    setLoading(true);
    try {
      const response = await eventsAPI.createEvent({
        ...eventData,
        group_id: groupId
      });
      
      SocketService.createEvent(groupId, {
        ...eventData,
        id: response.data.event_id
      });
      
      setEventData({ title: '', description: '', event_type: 'dinner' });
      alert('Event created successfully!');
    } catch (error) {
      alert('Error creating event');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="event-planner">
      <h3>Plan New Event</h3>
      
      <div className="event-form">
        <input
          type="text"
          placeholder="Event Title"
          value={eventData.title}
          onChange={(e) => setEventData({...eventData, title: e.target.value})}
        />
        
        <select 
          value={eventData.event_type}
          onChange={(e) => setEventData({...eventData, event_type: e.target.value})}
        >
          <option value="dinner">Dinner</option>
          <option value="movie">Movie</option>
          <option value="trip">Weekend Trip</option>
          <option value="activity">Activity</option>
        </select>
        
        <textarea
          placeholder="Event Description"
          value={eventData.description}
          onChange={(e) => setEventData({...eventData, description: e.target.value})}
          rows="3"
        />
        
        <button onClick={createEvent} disabled={loading}>
          {loading ? 'Creating...' : 'Create Event'}
        </button>
      </div>

      <div className="suggestions-section">
        <h4>Smart Suggestions</h4>
        
        <div className="search-box">
          <input
            type="text"
            placeholder="Search for restaurants, cafes..."
            onChange={(e) => searchPlaces(e.target.value)}
          />
        </div>
        
        <div className="suggestions-list">
          {suggestions.places.slice(0, 5).map(place => (
            <div key={place.id} className="suggestion-item">
              <h5>{place.name}</h5>
              <p>{place.address}</p>
              <span>Rating: {place.rating}/5</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EventPlanner;
