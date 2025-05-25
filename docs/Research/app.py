# Import Flask (for API) and jsonify (to return JSON)
from flask import Flask, jsonify

# Import CORS
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Test route
@app.route("/ping")
def ping():
    return "pong"

# List of ideas
ideas = [
            {
                "title": "Fall detection",
                "description": "Spot sudden falls using the accelerometer"
            },
            {
                "title": "Activity tracking",
                "description": "Measure daily physical activity with motion sensors"
            },
            {
                "title": "Sleep monitoring",
                "description": "Analyze movement during the night to estimate sleep quality and phases"
            },
            {
                "title": "Rehabilitation progress tracking",
                "description": "Monitor patient movement patterns during physiotherapy sessions"
            },
            {
                "title": "Posture detection",
                "description": "Detect bad sitting or standing posture using orientation sensors"
            },
            {
                "title": "Running vs walking detection",
                "description": "Classify physical activity into walking, running, or idle states"
            },
            {
                "title": "Cycling detection",
                "description": "Identify when the user is cycling using periodic motion data"
            }
]

def load_ideas():
    with open('ideas.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route("/api/ideas", methods=["GET"])
def get_ideas():
    return jsonify(ideas)


if __name__ == "__main__":
    app.run(debug=True)
