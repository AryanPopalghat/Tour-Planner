class WeatherService:
    def get_weather(self, city, date):
        # Mock weather data, replace with actual API integration
        weather_data = {
            "Rome": {"forecast": "Sunny", "temperature": "24°C"},
            "Paris": {"forecast": "Rainy", "temperature": "18°C"},
        }
        if city in weather_data:
            return weather_data[city]
        else:
            return {"forecast": "Unknown", "temperature": "Unknown"}
