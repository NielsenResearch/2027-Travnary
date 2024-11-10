import requests
import streamlit as st

# Function to fetch weather data
def get_weather(destination):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={destination}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["weather"][0]["description"], data["main"]["temp"]
    else:
        return "Weather data not available", None

# Function to fetch events from Eventbrite (or any similar API)
def get_events(destination):
    api_key = "YOUR_EVENTBRITE_API_KEY"
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"https://www.eventbriteapi.com/v3/events/search/?location.address={destination}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        events = response.json()["events"]
        return [event["name"]["text"] for event in events[:5]]
    else:
        return ["No events available"]

# Destination-specific activities (Sample data for illustration)
DESTINATION_ACTIVITIES = {
    "Paris": ["Eiffel Tower visit", "Louvre Museum tour", "Seine River cruise"],
    "New York": ["Statue of Liberty", "Central Park picnic", "Broadway show"],
    "Tokyo": ["Shibuya Crossing", "Sensoji Temple", "Tsukiji Fish Market tour"]
}

# Function to generate an itinerary based on user preferences
def generate_itinerary(destination, duration, interests):
    itinerary = []
    activities = DESTINATION_ACTIVITIES.get(destination, ["Explore the city"])
    
    # Fetch real-time data
    weather_desc, temperature = get_weather(destination)
    events = get_events(destination)
    
    # Build itinerary with daily activities
    for day in range(1, duration + 1):
        day_plan = f"Day {day}: "
        if day <= len(activities):
            day_plan += f"{activities[day-1]}"
        else:
            day_plan += "Free exploration"
        
        if interests:
            day_plan += f" and some {interests} activities."
        
        itinerary.append(day_plan)
    
    # Display weather and events
    itinerary.append(f"\nWeather forecast: {weather_desc}, Temp: {temperature}K")
    itinerary.append("\nTop Events:")
    itinerary.extend(events)
    
    return itinerary

# Streamlit app layout
def itinerary_app():
    st.title("Travel Itinerary Generator")
    
    # User inputs
    destination = st.text_input("Enter your destination:")
    duration = st.slider("Select the number of days:", 1, 10, 3)
    interests = st.text_input("Enter your interests (optional):")
    
    if st.button("Generate Itinerary"):
        if destination:
            itinerary = generate_itinerary(destination, duration, interests)
            st.write("\n".join(itinerary))
        else:
            st.write("Please enter a destination.")

# Run the app
if __name__ == "__main__":
    itinerary_app()
