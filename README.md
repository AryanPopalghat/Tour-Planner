# One-Day Tour Planning Assistant

A one-day tour planning assistant that creates a personalized itinerary based on user preferences, using memory to adapt to evolving requirements. 

## Features

- **User Preferences Collection**: Collect city, interests, timing, budget, and starting point.
- **Dynamic Itinerary Generation**: Adjusts based on user input, with budget-based optimization.
- **Memory Storage**: Neo4j database stores user preferences for continuity.
- **Multiple Agents**: Weather, Map, and Optimization agents to provide tailored suggestions.
- **Frontend Interface**: Streamlit interface for easy user interaction and itinerary viewing.

## Setup Instructions

1. **Install Requirements**
   ```bash
   pip install -r requirements.txt

2. **Run the FastAPI Backend**
   uvicorn main:app --reload
3. **Start Streamlit Frontend**
   streamlit run streamlit_frontend/frontend.py

