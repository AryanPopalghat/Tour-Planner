import streamlit as st
import requests

st.title("One-Day Tour Planning Assistant")

# URL configuration
API_BASE_URL = "http://localhost:8000"
ITINERARY_URL = f"{API_BASE_URL}/itinerary/"

# Input fields for the tour planner
user_id = st.text_input("Enter User ID", "")
city = st.text_input("City to Visit", "")
interests = st.multiselect("Select your Interests", ["Culture", "Adventure", "Food", "Shopping"])
start_time = st.time_input("Start Time")
end_time = st.time_input("End Time")
budget = st.number_input("Budget", min_value=0, step=1)

# Generate Itinerary button
if st.button("Generate Itinerary"):
    itinerary_payload = {
        "user_id": user_id,
        "city": city,
        "interests": interests,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "budget": budget
    }

    try:
        itinerary_response = requests.post(ITINERARY_URL, json=itinerary_payload)
        if itinerary_response.ok:
            itinerary_data = itinerary_response.json()
            start_point = itinerary_data.get("start_point", "Start Point: Not specified")
            st.write(f"Start Point: {start_point}")
            
            itinerary = itinerary_data.get("itinerary", [])
            if itinerary:
                for stop in itinerary:
                    st.write(f"Stop {stop.get('Stop', 'Unknown')}: {stop.get('Name', 'Unknown Place')}")
                    st.write(f"  - Time: {stop.get('Time', 'No specified time')}")
                    st.write(f"  - Entry Fee: {stop.get('Entry Fee', '$0')}")
                    st.write(f"  - Transportation: {stop.get('Transportation', 'Unspecified')}")
                    st.write(f"  - Status: {stop.get('Status', 'Unspecified')}")
                    st.write(f"  - Address: {stop.get('Address', 'No Address Available')}")
            else:
                st.write("No itinerary available.")
        else:
            st.error("Failed to generate itinerary.")
            st.write(itinerary_response.json())
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
