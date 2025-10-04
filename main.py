from src.server.api.v1.app import app


app.run(host="0.0.0.0", port=5000, debug=True)