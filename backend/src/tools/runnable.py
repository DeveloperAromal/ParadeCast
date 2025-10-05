from langchain.tools import tool
from typing import List, Dict, Any
import json
from src.tools.wind_data import wind_speed
from src.tools.environment_events import get_eonet_events_nearby
from src.tools.weather_data import nasa_weather
from src.tools.temp_and_humidity import temperature_humidity
from src.tools.send_mail import send_email


@tool("collect_wind_info", return_direct=False)
def do_collect_wind_info(lat: float, lon: float, start_date: str, end_date: str) -> str:
    """Collect wind speed/direction for coordinates between start_date and end_date."""
    data = wind_speed(lat, lon, start_date, end_date)
    return json.dumps(data)


@tool("collect_weather_info", return_direct=False)
def do_collect_weather_info(lat: float, lon: float, start_date: str, end_date: str) -> str:
    """Fetch NASA weather summary for coordinates between start_date and end_date."""
    summary = nasa_weather(lat, lon, start_date, end_date)
    return summary


@tool("collect_temperature_info", return_direct=False)
def do_collect_temperature_info(lat: float, lon: float, start_date: str, end_date: str) -> str:
    """Collect temperature and humidity for coordinates between start_date and end_date."""
    data = temperature_humidity(lat, lon, start_date, end_date)
    return json.dumps(data)


@tool("collect_environment_info", return_direct=False)
def do_collect_environment_info(lat: float, lon: float) -> str:
    """Retrieve environmental events near the given coordinates."""
    events = get_eonet_events_nearby(lat, lon)
    return json.dumps(events)
