from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse
from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient
from authlib.common.security import generate_token
from models.user_model import PreferencesPayload, ItineraryRequest
from agents.memory_agent import MemoryAgent
from agents.itinerary_generation_agent import ItineraryGenerationAgent
from agents.optimization_agent import OptimizationAgent
from agents.weather_agent import WeatherAgent
from agents.news_agent import NewsAgent
from agents.user_interaction_agent import UserInteractionAgent
import os
from datetime import datetime

app = FastAPI()

# Kinde configuration
configuration = Configuration(host="https://tourplanner.kinde.com")
kinde_api_client_params = {
    "configuration": configuration,
    "domain": "https://tourplanner.kinde.com",
    "client_id": "ffb281183f5146ddb3817475b6ef6ce9",
    "client_secret": "tyLkPmcG9Lr4nNlg0Q6ZOisreiUHSn9TiEa5z6gaxIps7oDiKNxm",  # Replace with your actual client secret
    "grant_type": GrantType.AUTHORIZATION_CODE,
    "callback_url": "http://localhost:8000/callback"
}
kinde_client = KindeApiClient(**kinde_api_client_params)

CODE_VERIFIER = generate_token(48)
kinde_api_client_params["code_verifier"] = CODE_VERIFIER

# Initialize agents
user_interaction_agent = UserInteractionAgent()
itinerary_agent = ItineraryGenerationAgent()
optimization_agent = OptimizationAgent()
weather_agent = WeatherAgent(api_key="e033de0610ea429d98703246241011")  # Replace with OpenWeather API key
news_agent = NewsAgent(api_key="e098c3680b2c4520bca39cde6f6c54c2")  # Replace with NewsAPI key
memory_agent = MemoryAgent(uri="neo4j+s://ac1d74d4.databases.neo4j.io", user="neo4j", password="zM-HuEf-w9wMmTOICO_-iPGXauVfFGX9j_DBqiDnyp8")

# Routes for login and registration
@app.get("/login")
def login():
    login_url = kinde_client.get_authorization_url()
    return RedirectResponse(login_url)

@app.get("/register")
def register():
    register_url = kinde_client.get_authorization_url(signup=True)
    return RedirectResponse(register_url)

@app.get("/callback")
def callback(request: Request):
    code = request.query_params.get("code")
    token_response = kinde_client.get_token(code=code, code_verifier=CODE_VERIFIER)
    if "access_token" in token_response:
        request.session["access_token"] = token_response["access_token"]
        return RedirectResponse(url="/dashboard")
    return {"error": "Failed to retrieve access token"}

# Route to collect user preferences
@app.post("/preferences/")
async def set_preferences(payload: PreferencesPayload):
    user_id = payload.user_id
    preferences_data = payload.preferences.dict()

    for pref, value in preferences_data.items():
        if value is not None:  # Ensure no null values are sent
            memory_agent.store_preference(user_id, pref, value)
    return {"status": "Preferences stored"}


# Route to generate itinerary
@app.post("/itinerary/")
async def get_itinerary(request: ItineraryRequest):
    user_id = request.user_id
    city = request.city
    interests = request.interests
    start_time = request.start_time
    end_time = request.end_time
    budget = request.budget
    
    # Get suggested places based on interests
    suggested_places = user_interaction_agent.suggest_places(city, interests)
    
    # Generate and optimize itinerary using suggested places
    itinerary = itinerary_agent.generate_itinerary(city, interests, start_time, end_time, budget, suggested_places)
    optimized_itinerary = optimization_agent.optimize_route(itinerary, budget)

    # Get weather forecast and news events
    weather_forecast = weather_agent.get_weather(city, datetime.now())
    news_events = news_agent.get_news_info(city, datetime.now())

    # Format the response with detailed itinerary
    formatted_itinerary = {
        "start_point": f"{city} City Center",
        "itinerary": [
            {
                "Stop": i + 1,
                "Name": stop.get("name", "Unknown Place"),
                "Time": stop.get("time", "TBD"),
                "Entry Fee": stop.get("entry_fee", "TBD"),
                "Transportation": stop.get("transportation", "TBD"),
                "Status": stop.get("status", "TBD")
            }
            for i, stop in enumerate(optimized_itinerary)
        ],
        "weather": weather_forecast,
        "news": news_events
    }

    return {"itinerary": formatted_itinerary}


    # except Exception as e:
    # return {"error": f"An unexpected error occurred: {str(e)}"}


# Route to view dashboard
@app.get("/dashboard")
async def dashboard():
    return {"message": "Welcome to your dashboard!"}
