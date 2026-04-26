# Hipper Monitoring

A full-stack IoT health monitoring system for tracking patient activity data from **Hipper PAM (Physical Activity Monitor)** devices. Data is collected via a Raspberry Pi base station over BLE, stored in a MariaDB database, and visualized through a Flask web application for both patients and therapists.

---

## Architecture

```
PAM Device (BLE)
      │
Raspberry Pi Base Station (BLE → HTTP)
      │
Flask Web App ←→ MariaDB
      │
Browser (Patient / Therapist / Admin)
```

- **Base station**: Raspberry Pi 4 running `src/back-end/pam/main.py` — scans for PAM devices via BLE and pushes data to the backend.
- **Backend**: Flask (`src/app/`) with a MariaDB database (`src/back-end/database/`).
- **AI/ML**: Decision tree model (`src/back-end/AI/`) for activity zone classification and anomaly detection on step data.

---

## Stack

| Layer | Technology |
|---|---|
| Web framework | Flask (Python 3.11) |
| Database | MariaDB |
| BLE communication | Raspberry Pi 4 (Legacy OS) |
| ML | scikit-learn (Decision Tree) |
| Containerization | Docker / Docker Compose |
| Documentation | MkDocs |

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- A `.env` file at `src/back-end/database/.env` with the following variables:

```env
MYSQL_HOST=
MYSQL_PORT=3306
MYSQL_ROOT_USER=
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=
```

### Run with Docker

```bash
docker compose up --build
```

The web app will be available at `http://localhost:5000`.

### Base Station Setup (Raspberry Pi)

Flash Raspberry Pi OS (Legacy, 32-bit). Set hostname and username to `hippy`, then:

```bash
sudo apt update && sudo apt install git -y
git clone <repo-url>
cd <repo-folder>
chmod +x pi_setup.sh
./pi_setup.sh
```

Set `BACKEND_URL` in the base station config to point to your running Flask instance.

---

## Project Structure

```
src/
├── app/                  # Flask application
│   ├── __init__.py       # Routes and app entry point
│   ├── anomaly_detection.py
│   ├── zone_classifier.py
│   ├── database.py
│   ├── templates/
│   └── static/
└── back-end/
    ├── database/         # MariaDB init scripts & config
    ├── pam/              # Raspberry Pi BLE base station
    ├── AI/               # ML model training & inference
    └── datasets/
```

---

## Documentation

Full technical, therapist, and patient documentation is available via MkDocs:

```bash
pip install -r requirements.txt
mkdocs serve
```

Pre-built PDFs are available in `docs/`.
