from flask import Flask,jsonify,request
from flask_cors import CORS


from src.tools.environment_events import get_eonet_events_nearby
from src.tools.temp_and_humidity import temperature_humidity
from src.tools.weather_data import nasa_weather
from scr.tools.wind_data import wind_speed
from src.tools.send_mail import send_mail
import os


app = Flask(__name__)
CORS(app)


@app.route("/")
def root():
    return jsonify({"message": "Welcome to the ParadeCast API!"})


@app.route("/api/v1/info",method=["GET"])
def info(lon,lat,start_time,end_time):
    





