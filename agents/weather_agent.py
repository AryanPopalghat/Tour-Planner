import requests
from datetime import datetime

class WeatherAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1"

    def get_weather(self, location, date):
        # Ensure `date` is a datetime object; if not, try to parse it
        if isinstance(date, str):
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return "Invalid date format. Expected 'YYYY-MM-DD'."

        date_str = date.strftime('%Y-%m-%d')
        url = f"{self.base_url}/forecast.json"
        params = {
            'key': self.api_key,
            'q': location,
            'dt': date_str
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            forecast = data.get('forecast', {}).get('forecastday', [])
            if forecast:
                day_info = forecast[0].get('day', {})
                condition = day_info.get('condition', {}).get('text', 'No data')
                max_temp = day_info.get('maxtemp_c', 'No data')
                min_temp = day_info.get('mintemp_c', 'No data')
                
                return (
                    f"Weather forecast for {location} on {date_str}:\n"
                    f"Condition: {condition}\n"
                    f"Max Temperature: {max_temp}°C\n"
                    f"Min Temperature: {min_temp}°C\n"
                )
            else:
                return f"No weather data available for {location} on {date_str}."
        else:
            return f"Failed to retrieve weather data: HTTP {response.status_code}."
