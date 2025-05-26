# AI Ideas Web Application Documentation

## Overview

This document is a simple, full-featured web application that demonstrates how to serve AI-related ideas from a sensor-based dataset using a Flask backend and a simple HTML frontend

- The interface displays a list of potential use cases for sensor data 
- Le backend fournit une API pour récupérer ces cas d'utilisation à partir d'un fichier JSON

---

## How It Works

### 1. Backend (Flask)

#### Description

The Flask application serves an API to `/api/ideas` which returns a list of AI use cases. The data is stored in a local JSON file 

#### Key Features:
- CORS enabled to allow the frontend on another port ( 8000 ) to access the API on port 5000
- Reads data from `ideas.json`.
- Simple `/ping` route for test purposes

#### Code 

```python
from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

def load_ideas():
    with open('ideas.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route("/ping")
def ping():
    return "pong"

@app.route("/api/ideas", methods=["GET"])
def get_ideas():
    return jsonify(load_ideas())

if __name__ == "__main__":
    app.run(debug=True)
```

### 2. Data File (ideas.json)

This file contains a list of ideas for how sensor data could be used in AI applications

Example content:

```json
[
  {
    "title": "Fall detection",
    "description": "Spot sudden falls using the accelerometer"
  },
  {
    "title": "Activity tracking",
    "description": "Measure daily physical activity with motion sensors"
  }
]
```

---

### 3. Frontend (HTML + JavaScript)

#### Description

A HTML page is used to display the list of ideas. It fetches the data from the `/api/ideas` endpoint

#### Key Features:

- Vanilla JS `fetch()` call to get JSON data
- Basic styling with inline CSS

#### Code Snippet

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>AI Ideas</title>
  <style>
    body { font-family: sans-serif; margin: 2rem; }
    .idea { border: 1px solid #ccc; padding: 1rem; margin-bottom: 1rem; border-radius: 5px; }
    .idea h2 { margin: 0 0 0.5rem 0; }
  </style>
</head>
<body>

  <h1>Ideas for using data</h1>
  <div id="ideas-container">List in progress</div>

  <script>
    fetch('http://localhost:5000/api/ideas')
      .then(response => response.json())
      .then(data => {
        const container = document.getElementById('ideas-container');
        container.innerHTML = '';
        data.forEach(idea => {
          const div = document.createElement('div');
          div.className = 'idea';
          div.innerHTML = `<h2>${idea.title}</h2><p>${idea.description}</p>`;
          container.appendChild(div);
        });
      })
      .catch(err => {
        document.getElementById('ideas-container').innerText = "Error";
        console.error('Fetch error:', err);
      });
  </script>

</body>
</html>
```

---

## Running the App

1. **Start the Flask API :**

   ```bash
   python app.py
   ```

2. **Start a simple HTTP server to serve `index.html` :**

   ```bash
   python -m http.server 8000
   ```

3. **Access the frontend:**
   Go to [http://localhost:8000](http://localhost:8000) and navigate to your `index.html`

---
