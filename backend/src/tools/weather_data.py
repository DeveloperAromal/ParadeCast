import requests
import time

def nasa_weather(lat: float, lon: float, start_date: str, end_date: str) -> str:

    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "PRECTOTCORR",
        "community": "AG",
        "latitude": lat,
        "longitude": lon,
        "start": start_date,
        "end": end_date,
        "format": "JSON"
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"[~] Fetching NASA POWER data... (Attempt {attempt+1})")
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            break
        except requests.exceptions.Timeout:
            print(f"[x] NASA request timed out on attempt {attempt+1}.")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return "NASA POWER request timed out after multiple attempts."
        except requests.exceptions.RequestException as e:
            print(f"[x] NASA request failed on attempt {attempt+1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return f"NASA POWER request failed after multiple attempts: {e}"

    try:
        prec_data = data["properties"]["parameter"]["PRECTOTCORR"]
    except KeyError:
        return "NASA POWER did not return precipitation data."

    summary_lines = []
    for date, value in prec_data.items():
        if value == -999:
            summary_lines.append(f"{date}: No data available")
        elif value > 0:
            summary_lines.append(f"{date}: {value} mm – Rain expected")
        else:
            summary_lines.append(f"{date}: {value} mm – No rain")

    return "\n".join(summary_lines)