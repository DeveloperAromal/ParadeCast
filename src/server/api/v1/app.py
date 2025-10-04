from flask import Flask,jsonify,request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def root():
    return jsonify({"message": "Welcome to the ParadeCast API!"})