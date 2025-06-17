# HIPPER Therapeutics - Dashboard HTML Structure

This document explains the structure and functionality of the HTML file used for the **HIPPER Therapeutics** dashboard/home page. The layout is composed of a header and a three-panel main content section that provides a quick overview of a user’s wellness data and goals.

---

##  File Overview

**HTML file location:**  
`home.html`

**Linked assets:**  
- CSS: `../static/css/home.css`
- JS: `../static/js/home.js`
- Images: `../static/images/` (are here at the moment just for placeholders)

---

##  HTML Structure Breakdown

### `<head>`
- Sets the character encoding (`UTF-8`)
- Ensures responsive layout on mobile devices (`viewport`)
- Loads external CSS for styling
- Sets page title

---

##  Header Section (`<header class="header">`)

Contains:
- **Logo**: Title "HIPPER THERAPEUTICS"
- **User Controls**:
  - User profile area displaying:
    - User name (e.g. Marianne Elsenbeek)
    - Profile avatar image

---


## Main Dashboard (`<main class="dashboard">`)

### 1. **Left Panel – Daily Stats** (`<section class="stats-panel">`)
Displays three daily metrics:
- **Mood indicator**: Emoji icon representing the user’s mood
- **Steps counter**: Shows steps taken (e.g. XXXX amount of steps)
- **Activity duration**: Time spent being active (e.g. XX minutes)

Each stat is visually separated by a divider.

---

### 2. **Middle Panel – Weekly Score** (`<section class="score-panel">`)
- Title: *Weekly Movement Score*
- Circular progress chart (SVG-based)
- Displays current weekly score (e.g. `XXX / XXX`)

---

### 3. **Right Panel – Personal Goals** (`<section class="goals-panel">`)
Displays progress on 3 goal categories:
- **Daily Goal**
  - Example: 3-day streak
  - Progress: `40 / 85` (47% complete)
- **Weekly Goal**
  - Progress: `153 / 600` (25% complete)
- **Monthly Goal**
  - Progress: `153 / 2400` (6% complete)

Each goal includes:
- Title and streak (if applicable)
- Visual progress bar
- Numeric progress display

---

### 4. **Bottom panel – Historical graph** (`<class="card chart-section">`)
The section allows users to visualize their historical activity data (steps and PAM score) across different time scales:
- Hourly (past 12 hours)
- Daily (past 7 days)
- Weekly (past 7 weeks)
- Monthly (past 6 months)

Each view displays bar charts for two metrics:
- steps: Number of steps taken
- PAM_score: A physical activity measure

---

## Script Reference

The following JS script is included at the bottom of the HTML:
```html
<script src="../static/js/home.js"></script>