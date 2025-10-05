
from src.agent.main_agent import main_agent
import json

from src.tools.summarizer import final_output_data_processing_agent


if __name__ == "__main__":
    historic_dates = ["20241005", "20241004", "20241003"]
    location_name = "Sample City"
    latitude = 40.7128
    longitude = -74.0060
    target_date = "20251005"

    final_output_data_processing_agent(latitude,longitude, days=2)
    
    # result = main_agent(
    #     historic_dates=historic_dates,
    #     location_name=location_name,
    #     latitude=latitude,
    #     longitude=longitude,
    #     target_date=target_date,
    # )

    # try:
    #     print(json.dumps(result, indent=2, default=str))
    # except Exception:
    #     print(result)

