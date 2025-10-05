import requests

def temperature_humidity(lat, lon, start_date, end_date):
 
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    params = {
        "parameters": "T2M,RH2M", 
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
    temperature = parameters.get("T2M", {}) 
    humidity = parameters.get("RH2M", {})  

    return {"temperature": temperature, "humidity": humidity}
