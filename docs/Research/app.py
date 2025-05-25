from flask import Flask
app = Flask(__name__)

@app.route("/ping")
def ping():
    return "pong"

ideas = [
    {"title": "Fall detection", "description": "Spot sudden falls using the accelerometer"},
]


if __name__ == "__main__":
    app.run(debug=True)
