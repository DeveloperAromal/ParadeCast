import requests
from math import radians, cos, sin, asin, sqrt
from src.utils.haversine import haversine
import os
from dotenv import load_dotenv

api_key = os.getenv("NASA_API_KEY")


def get_eonet_events_nearby(api_key, latitude, longitude, radius_km=100):
	
	url = "https://eonet.gsfc.nasa.gov/api/v3/events"
	headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
	params = {}
	response = requests.get(url, headers=headers, params=params)


	if response.status_code != 200:
		print(f"Failed to fetch events: {response.status_code}")
		return []


	data = response.json()
	events = data.get("events", [])
	nearby_events = []

	for event in events:
		for geom in event.get("geometry", []):
			coords = geom.get("coordinates", [])

			if len(coords) == 2:
				event_lon, event_lat = coords
				distance = haversine(longitude, latitude, event_lon, event_lat)


				if distance <= radius_km:
					event_copy = event.copy()
					event_copy["distance_km"] = distance
					nearby_events.append(event_copy)
					break 


	return nearby_events


