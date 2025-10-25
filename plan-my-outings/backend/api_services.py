import requests
import json
from config import Config

class GooglePlacesService:
    @staticmethod
    def search_places(query, location=None, radius=5000):
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': query,
            'key': Config.GOOGLE_PLACES_API_KEY
        }
        
        if location:
            params['location'] = location
            params['radius'] = radius
            
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if data['status'] == 'OK':
                places = []
                for place in data['results']:
                    places.append({
                        'id': place['place_id'],
                        'name': place['name'],
                        'address': place.get('formatted_address', ''),
                        'rating': place.get('rating'),
                        'price_level': place.get('price_level'),
                        'types': place.get('types', []),
                        'location': place['geometry']['location']
                    })
                return places
            return []
        except Exception as e:
            print(f"Error fetching places: {e}")
            return []

class TMDBService:
    @staticmethod
    def search_movies(query):
        base_url = "https://api.themoviedb.org/3/search/movie"
        params = {
            'api_key': Config.TMDB_API_KEY,
            'query': query
        }
        
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            movies = []
            for movie in data.get('results', [])[:10]:
                movies.append({
                    'id': movie['id'],
                    'title': movie['title'],
                    'overview': movie.get('overview', ''),
                    'release_date': movie.get('release_date', ''),
                    'rating': movie.get('vote_average', 0),
                    'poster_path': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}" if movie.get('poster_path') else None
                })
            return movies
        except Exception as e:
            print(f"Error fetching movies: {e}")
            return []

class OpenWeatherService:
    @staticmethod
    def get_weather_forecast(lat, lon):
        base_url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': Config.OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            forecast = []
            for item in data.get('list', [])[:8]:
                forecast.append({
                    'datetime': item['dt_txt'],
                    'temp': item['main']['temp'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon']
                })
            return forecast
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return []
