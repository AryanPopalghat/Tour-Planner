# One-Day Tour Planning Assistant

A web application that helps users plan a one-day tour based on their preferences, such as city, interests, budget, and available time. The application provides recommendations on places to visit, starting points, and additional details like entry fees and transportation.

## Overview

The application consists of a FastAPI backend to handle API requests and a Streamlit frontend for user interaction. Users enter their preferences on the frontend, which are sent to the backend for processing. The backend generates an itinerary using multiple specialized agents and returns the results to the frontend for display.

## Components

### Backend (main.py)

The backend is built with FastAPI and acts as the core processing unit of the application. It includes endpoints to handle user preferences and generate an itinerary based on user input.

#### Key Agents

- **Itinerary Generation Agent**: Generates a recommended itinerary based on the city, interests, start and end times, and budget. It uses the [Geoapify API](https://www.geoapify.com/) to gather location and activity data.
- **Weather Agent**: Fetches real-time weather information to make weather-informed itinerary recommendations.
- **News Agent**: Retrieves relevant news for the selected city to provide additional information about the destination, giving users a sense of current events or unique opportunities during their visit.
- **Memory Agent**: Stores user preferences and past interactions, using Neo4j as a database. This supports personalized insights and historical data retrieval.

### Frontend (frontend.py)

The frontend, built with Streamlit, serves as the user interface where users can enter preferences and view their generated itinerary. It interacts with the backend via HTTP requests to send preferences and retrieve the generated itinerary.

## APIs Used

- **Geoapify API**: Provides location-based recommendations for places and activities in the selected city.
- **Weather API**: Fetches current weather conditions to enhance the itinerary with weather-informed decisions.
- **News API**: Retrieves the latest news articles relevant to the selected city, providing additional context and information.
- **Neo4j Database**: Stores user preferences, supporting a personalized and context-aware experience.

## How It Works

1. **User Input**: Users enter their preferences (city, interests, budget, etc.) in the Streamlit frontend.
2. **Data Processing**: Preferences are sent to the FastAPI backend, where the Itinerary Generation Agent, Weather Agent, News Agent, and Memory Agent work together to gather data and generate recommendations.
3. **Itinerary Display**: The generated itinerary, including details on each stop, entry fees, transportation, news about the destination, and weather considerations, is displayed on the frontend.

## Installation

## Setup Instructions

1. **Install Requirements**
   ```bash
   pip install -r requirements.txt

2. **Run the FastAPI Backend**
```bash
   uvicorn main:app --reload
   ```
3. **Start Streamlit Frontend**
```bash
   streamlit run streamlit_frontend/frontend.py
```

## Usage

1. Open the Streamlit application in your browser at `http://localhost:8501`.
2. Enter your preferences (city, interests, budget, etc.) on the frontend.
3. Click **Save Preferences** to store your preferences.
4. Click **Generate Itinerary** to view the recommended itinerary based on your input.

## Future Enhancements

- Add more agents to support additional data sources or features.
- Implement user authentication for a more personalized experience.
- Integrate more APIs for richer recommendations.

## Video Link

[Click here](https://drive.google.com/file/d/19zQaAGRT580rwJxu_n9NCHvHrB7_9lig/view?usp=sharing)

Please watch it in 1.5-2x speed.
