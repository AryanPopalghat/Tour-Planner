import streamlit as st
import requests

st.title("One-Day Tour Planning Assistant")

user_id = st.text_input("Enter User ID", "")
city = st.text_input("City to Visit", "")
interests = st.multiselect("Select your Interests", ["Culture", "Adventure", "Food", "Shopping"])
start_time = st.time_input("Start Time")
end_time = st.time_input("End Time")
budget = st.number_input("Budget", min_value=0, step=1)

if st.button("Submit Preferences"):
    preferences = {
        "city": city,
        "interests": interests,
        "start_time": start_time.strftime('%H:%M'),
        "end_time": end_time.strftime('%H:%M'),
        "budget": budget
    }
    payload = {
        "user_id": user_id,
        "preferences": preferences
    }

    response = requests.post("http://localhost:8000/preferences/", json=payload)
    if response.ok:
        st.success("Preferences saved!")
    else:
        st.error("Failed to save preferences.")
        try:
            st.write(response.json())
        except ValueError:
            st.write("Unable to parse error details.")

if st.button("Generate Itinerary"):
    itinerary_payload = {
        "user_id": user_id,
        "city": city,
        "interests": interests,
        "start_time": start_time.strftime('%H:%M'),
        "end_time": end_time.strftime('%H:%M'),
        "budget": budget
    }
    itinerary_response = requests.post("http://localhost:8000/itinerary/", json=itinerary_payload)
    
    if itinerary_response.ok:
        response_data = itinerary_response.json()
        
        if "itinerary" in response_data:
            itinerary = response_data["itinerary"]
            st.write(f"Start Point: {itinerary['start_point']}")
            for stop in itinerary["itinerary"]:
                st.write(f"Stop {stop['Stop']}: {stop['Name']}")
                st.write(f"  - Time: {stop['Time']}")
                st.write(f"  - Entry Fee: {stop['Entry Fee']}")
                st.write(f"  - Transportation: {stop['Transportation']}")
                st.write(f"  - Status: {stop['Status']}")
        else:
            st.error("Failed to generate itinerary.")
            st.write(response_data.get("error", "Unknown error occurred."))
    else:
        st.error("Failed to generate itinerary.")
        try:
            st.write(itinerary_response.json())
        except ValueError:
            st.write("Unable to parse error details.")
