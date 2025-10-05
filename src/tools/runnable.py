from langchain.tools import tool
from typing import List, Dict, Any
from src.tools.wind_data import wind_speed
from src.tools.environment_events import get_eonet_events_nearby
from src.tools.weather_data import nasa_weather
from src.tools.temp_and_humidity import temperature_humidity
from src.tools.send_mail import send_email


@tool("collect_wind_info", return_direct=True)
def do_collect_wind_info(
    lat: float,
    lon: float,
    start_date: str,
    end_date: str
) -> Dict[str, Any]:
    
    """Collects wind information (speed, direction, etc.) for given coordinates and date range."""
    
    return wind_speed(lat, lon, start_date, end_date)


@tool("collect_weather_info", return_direct=True)
def do_collect_weather_info(
    lat: float,
    lon: float,
    start_date: str,
    end_date: str
) -> Dict[str, Any]:
    
    """Fetches NASA weather data for given coordinates and date range."""
    
    return nasa_weather(lat, lon, start_date, end_date)


@tool("collect_temperature_info", return_direct=True)
def do_collect_temperature_info(
    lat: float,
    lon: float,
    start_date: str,
    end_date: str
) -> Dict[str, Any]:
    
    """Collects temperature and humidity data for given coordinates and date range."""
    
    return temperature_humidity(lat, lon, start_date, end_date)


@tool("collect_environment_info", return_direct=True)
def do_collect_environment_info(
    lat: float,
    lon: float
) -> List[Dict[str, Any]]:
    
    """Retrieves environmental events near the given coordinates (e.g., storms, wildfires, etc.)."""
    
    return get_eonet_events_nearby(lat, lon)


@tool("send_email", return_direct=True)
def do_send_email(
    receiver_email: str,
    subject: str,
    html_content: str
) -> Dict[str, Any]:
    
    """Sends an email with the given subject and HTML content to the receiver."""
    
    return send_email(receiver_email, subject, html_content)
