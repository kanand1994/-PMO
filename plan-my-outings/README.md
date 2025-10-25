# Plan My Outings - Group Event Planning App

A smart event planning web application that helps groups decide plans together with suggestions for movies, restaurants, and hangout spots based on preferences.

## Features

- **Auto Account Creation**: No traditional signup - users submit enquiries and get auto-generated credentials
- **Group Management**: Create and manage outing groups with friends
- **Event Planning**: Plan events with smart suggestions
- **Real-time Collaboration**: Live updates using Socket.io
- **API Integrations**: 
  - Google Places for venue suggestions
  - TMDB for movie recommendations
  - OpenWeather for weather forecasts
- **Voting System**: Polls and RSVP features
- **Smart Suggestions**: Location-based recommendations

## Tech Stack

### Backend
- Python Flask
- SQLite3 database
- Socket.io for real-time features
- JWT for authentication

### Frontend
- React.js
- Socket.io client
- Axios for API calls

## Setup Instructions

### Backend Setup
1. Navigate to backend directory:
   bash
   cd plan-my-outings/backend
2. Install Python dependencies:
	bash
	pip install -r requirements.txt

3. Set up environment variables in .env file

4. Run the backend server:
	bash
	python app.py

### Frontend Setup
1. Navigate to frontend directory:
	bash
	cd plan-my-outings/frontend
2. Install dependencies:
	bash
	npm install
3. Start the development server:
	bash
	npm start
### API Keys Required
Get the following API keys and add them to backend/.env:

Google Places API Key

TMDB API Key

OpenWeather API Key

Email credentials (optional)

### Usage
Go to the Contact page and fill out the form

System will automatically create your account and provide credentials

Use the provided credentials to login

Create groups and start planning events!

### Project Structure
text
plan-my-outings/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── auth.py             # Authentication utilities
│   ├── database.py         # Database models and setup
│   ├── socket_events.py    # Socket.io event handlers
│   ├── api_services.py     # External API integrations
│   ├── requirements.txt    # Python dependencies
│   ├── config.py          # Configuration settings
│   └── .env               # Environment variables
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API and socket services
│   │   ├── utils/         # Utility functions
│   │   └── App.js         # Main App component
│   ├── package.json       # Node.js dependencies
│   └── .env              # Frontend environment variables
└── README.md
