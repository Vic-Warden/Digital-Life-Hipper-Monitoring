# 📄 PAM Label Assignment Tool Documentation

## 🧾 Overview

The **PAM Label Assignment Tool** is a graphical user interface (GUI) application built using `tkinter` and `matplotlib`. It enables users to visually label segments of time-series data, specifically physical activity metrics like "Steps" and "PAM Score". Users can select time intervals directly on a plot and assign predefined activity labels to those intervals. The labeled dataset can be exported as a CSV file for further analysis or model training.

---

## 📁 Dataset Requirements

The application expects a CSV file containing at least the following columns:

- `Timestamp`: Timestamps in a standard format (ISO 8601 recommended).
- `Steps`: Numeric values representing step counts.
- `PAM Score`: Numeric values representing PAM scores.

---

## 📦 Dependencies

Make sure the following Python packages are installed:

```bash
pip install pandas matplotlib numpy