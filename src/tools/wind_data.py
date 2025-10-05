import requests
import time


def wind_speed(lat, lon, start_date, end_date):
    
    
    base_url =  f"https://power.larc.nasa.gov/api/temporal/daily/point"
   
    params = {
                "parameters": "WD10M,WS10M",
                "community": "RE",
                "latitude": lat,
                "longitude": lon,
                "start": start_date,
                "end": end_date,
                "format": "JSON"
             }

    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"NASA API error: {response.status_code}")


    data = response.json()
    
    if "properties" not in data or "parameter" not in data["properties"]:
        raise Exception("Invalid response structure")


    parameters = data["properties"]["parameter"]
    ws10m = parameters.get("WS10M", {})
    wd10m = parameters.get("WD10M", {})


    return  {
                "speed": ws10m, 
                "direction": wd10m
            }