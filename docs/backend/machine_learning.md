# Usual Activity Slot Detection

## Description

This module provides a script that automatically detects a patient’s usual activity time slots over the last 7 days. The goal is to assist therapists in identifying routine patterns and spotting any disruptions over time.

## Technologies Used
Python 3.10+

MySQL database

Pandas for data processing

dotenv for environment configuration

## How to Use It

```bash
pip install pandas mysql-connector-python python-dotenv
```

```bash
python src/back-end/pam/get_usual_slots.py
```

## Features

Automatically analyzes the past 7 days of hourly activity

Identifies time slots with consistently high activity

Configurable detection threshold 

Output is structured and exportable in JSON format

Easily extendable for future usage like anomaly comparison