from fastapi import FastAPI, HTTPException, Request
from models.user_model import PreferencesPayload, ItineraryRequest
from agents.itinerary_generation_agent import ItineraryGenerationAgent
from agents.weather_agent import WeatherAgent
from agents.news_agent import NewsAgent
from agents.memory_agent import MemoryAgent
import os

app = FastAPI()

# Initialize API keys and agents
GEOAPIFY_API_KEY = "ed42799fa0cb455dabdb1e96cf966419"  
itinerary_agent = ItineraryGenerationAgent(api_key=GEOAPIFY_API_KEY)
weather_agent = WeatherAgent(api_key="e033de0610ea429d98703246241011")
news_agent = NewsAgent(api_key="e098c3680b2c4520bca39cde6f6c54c2")
memory_agent = MemoryAgent(uri="neo4j+s://ac1d74d4.databases.neo4j.io", user="neo4j", password="zM-HuEf-w9wMmTOICO_-iPGXauVfFGX9j_DBqiDnyp8")

# Endpoint to generate itinerary
@app.post("/itinerary/")
async def generate_itinerary(request: ItineraryRequest):
    city = request.city
    interests = request.interests
    start_time = request.start_time
    end_time = request.end_time
    budget = request.budget

    # Set a default value for start_point
    response_data = {"start_point": f"{city} City Center"}

    # Generate itinerary using the ItineraryGenerationAgent
    itinerary = itinerary_agent.generate_itinerary(city, interests, start_time, end_time, budget)
    if itinerary:
        response_data["itinerary"] = itinerary
    else:
        response_data["itinerary"] = [{"Error": "No places found or itinerary could not be generated."}]

    return response_data
