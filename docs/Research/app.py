from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/ping")
def ping():
    return "pong"

ideas = [
    {"title": "Fall detection", "description": "Spot sudden falls using the accelerometer"},
]

@app.route("/api/ideas", methods=["GET"])
def get_ideas():
    return jsonify(ideas)


if __name__ == "__main__":
    app.run(debug=True)
