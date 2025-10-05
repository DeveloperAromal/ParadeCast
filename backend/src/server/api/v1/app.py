from flask import Flask,jsonify,request
from flask_cors import CORS

from src.agent.main_agent import main_agent
from src.utils.generate_basic_data import generate_historic_dates
from datetime import datetime
from src.tools.summarizer import final_output_data_processing_agent

import os


app = Flask(__name__)
CORS(app)


@app.route("/")
def root():
    return jsonify({"message": "Welcome to the ParadeCast API!"})


@app.route("/api/v1/get_infos",method=["POST"])
def info(lon, lat, day_forcast):
    
    dates = generate_historic_dates((datetime.now().strftime("%Y%m%d")), total_years_back=10)
    main_agent(dates, lat, lon, (datetime.now().strftime("%Y%m%d")))
    

    final_output_data_processing_agent(lat,lon, day_forcast)
    
    load_path = os.path.join("src/db/processed", "prediction.json")

    
    with open(load_path, "r") as f:
        result = f.read()

    return result



