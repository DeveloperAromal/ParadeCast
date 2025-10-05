import requests
from src.utils.haversine import haversine  
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("NASA_API_KEY") 

def get_eonet_events_nearby(lat, lon, radius_km=500):
    """
    Fetch recent natural events from EONET within radius_km of given coordinates
    """
    url = "https://eonet.gsfc.nasa.gov/api/v3/events"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch events: {response.status_code}")
        return []

    data = response.json()
    events = data.get("events", [])
    nearby_events = []

    for event in events:
        for geom in event.get("geometry", []):
            coords = geom.get("coordinates", [])

            if len(coords) >= 2:
                event_lon, event_lat = coords[0], coords[1]
                distance = haversine(lon, lat, event_lon, event_lat)

                if distance <= radius_km:
                    event_copy = event.copy()
                    event_copy["distance_km"] = round(distance, 2)
                    nearby_events.append(event_copy)
                    break 

    return nearby_events
