# 📄 Script: `generate_dataset.py`

## Purpose
Generates a synthetic dataset simulating human activity (steps and PAM scores) over a span of days. The dataset includes timestamps, randomly generated step counts, and PAM scores, with built-in gaps to represent inactivity.

## How It Works

1. **Time Range Definition**
   - Sets a start time (`1970-02-01 18:00`) and end time (`1970-02-10 00:00`).
   - Generates timestamps at 1-minute intervals.

2. **Simulating Gaps (Inactivity)**
   - Randomly removes 20% of the timestamps to simulate periods of no data (e.g., sleep or device turned off).

3. **Data Generation**
   - **Steps**: Mostly `0`, with occasional values between `1` and `20` (simulating bursts of activity).
   - **PAM Score**: Random float between `0.0` and `2.0`, with a 30% chance of being `0.0` to represent inactivity.

4. **Export**
   - Saves the final dataset as a CSV file: `artificial_movement_data.csv`.
