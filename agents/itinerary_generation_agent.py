import requests

class ItineraryGenerationAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.places_base_url = "https://api.geoapify.com/v2/places"
        self.geocoding_base_url = "https://api.geoapify.com/v1/geocode/search"

    def get_coordinates(self, city):
        """Fetches the latitude and longitude of a city using Geoapify's geocoding API."""
        params = {
            "text": city,
            "apiKey": self.api_key
        }
        response = requests.get(self.geocoding_base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['features']:
                # Return the coordinates of the first result
                location = data['features'][0]['geometry']['coordinates']
                return location[1], location[0]  # latitude, longitude
            else:
                print(f"No results found for city: {city}")
        else:
            print(f"Error fetching coordinates: {response.status_code} - {response.text}")
        return None, None

    def get_places(self, location, categories, radius=5000, limit=5):
        params = {
            "categories": ",".join(categories),
            "filter": f"circle:{location[1]},{location[0]},{radius}",
            "limit": limit,
            "apiKey": self.api_key
        }
        response = requests.get(self.places_base_url, params=params)
        if response.status_code == 200:
            return response.json().get('features', [])
        else:
            print(f"Error fetching places: {response.status_code} - {response.text}")
            return []

    def generate_itinerary(self, city, interests, start_time, end_time, budget):
        # Get coordinates for the city
        latitude, longitude = self.get_coordinates(city)
        if latitude is None or longitude is None:
            return [{"Error": "Unable to find location for the specified city"}]

        # Map interests to Geoapify categories
        interest_to_category = {
            "food": "catering.restaurant",
            "shopping": "commercial.shopping_mall",
            "adventure": "leisure.outdoor",
            "culture": "entertainment.museum"
        }
        
        # Get relevant categories based on user interests
        categories = [interest_to_category[interest.lower()] for interest in interests if interest.lower() in interest_to_category]

        # Fetch places from Geoapify
        places = self.get_places((latitude, longitude), categories)

        # Format the itinerary with fetched place details
        itinerary = []
        for i, place in enumerate(places, start=1):
            properties = place.get('properties', {})
            itinerary.append({
                "Stop": i,
                "Name": properties.get("name", "Unknown Place"),
                "Time": f"{start_time} - {end_time}",  # Example timing; adjust based on actual need
                "Entry Fee": properties.get("fee", "TBD"),
                "Transportation": "Walk",
                "Status": properties.get("opening_hours", "Open") if properties.get("opening_hours") else "TBD",
                "Address": properties.get("formatted", "No Address Available")
            })
        
        return itinerary
