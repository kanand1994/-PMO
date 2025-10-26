import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (credentials) => api.post('/login', credentials),
};

export const contactAPI = {
  submitEnquiry: (data) => api.post('/contact', data),
};

export const groupsAPI = {
  getGroups: () => api.get('/groups'),
  createGroup: (data) => api.post('/groups', data),
};

export const eventsAPI = {
  createEvent: (data) => api.post('/events', data),
};

export const placesAPI = {
  searchPlaces: (query, location) => 
    api.get('/places/search', { params: { query, location } }),
};

export const moviesAPI = {
  searchMovies: (query) => 
    api.get('/movies/search', { params: { query } }),
};

export const weatherAPI = {
  getForecast: (lat, lon) => 
    api.get('/weather/forecast', { params: { lat, lon } }),
};

export const pollsAPI = {
  castVote: (pollId, data) => 
    api.post(`/polls/${pollId}/vote`, data),
};

export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
  getEmailLogs: () => api.get('/admin/email-logs'),
  getRecentUsers: () => api.get('/admin/recent-users'),
  getSystemActivity: () => api.get('/admin/system-activity'),
  clearDemoData: () => api.post('/admin/clear-demo-data'),
  resendEmail: (userId) => api.post('/admin/resend-email', { user_id: userId }),
};

export default api;
