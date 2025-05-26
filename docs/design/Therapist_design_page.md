# Hipper Therapeutics Client Dashboard Design Overview

This document describes the interface and functionalities of the **Hipper Therapeutics** client dashboard used by therapists to monitor and manage their clients' physical activity data and goals.

---

##  Dashboard Components

### 1. **Client Data Panel (Left Section)**
- **Weekly PAM Score**: Visualized with a footstep icon and progress bar. Example: `11/20`.
- **Inactive Minutes**: Displays total minutes of inactivity (e.g., `180` minutes).
- **Monthly Score Dial**:
  - Circular progress indicator showing the overall monthly score.
  - Center value displays current vs. target (e.g., `370 / 600`).
  - Color coding (e.g., yellow highlight) shows progress percentage.

### 2. **Client Goals Panel (Right Section)**
- **Weekly Goal**: Horizontal progress bar showing current progress (e.g., `40 / 85`).
- **Monthly Goal**: Another bar showing monthly goal progress (e.g., `153 / 600`).
- **Edit / Delete Options**: Icons next to each goal allow therapists to:
  - ✏️ Edit goal values.
  - 🗑️ Delete goals.
- **Add Client Goals**:
  -  Button allows therapists to add new custom goals for the client.

---


##  Historic Activity Graph

### Description
- A combined graph displays multiple types of client activity data:
  - **Blue Bars**: Daily step counts.
  - **Green Line**: PAM (Physical Activity Metric) score.
  - **Red Highlights**: Indicates inactive days.

### Graph Features
- **Daily / Weekly Toggle**: Top-right selector allows switching views.
- **Hover Labels**: Hovering shows exact step count and PAM score for each day.
- **X-Axis**: Dates.
- **Y-Axis**:
  - Left: Step count scale.
  - Right: PAM score scale.

---

##  Therapist Additional Functionalities

Therapists using this dashboard can:
- View a comprehensive summary of the client's physical activity.
- Monitor both **activity (steps, PAM)** and **inactivity (minutes, red days)**.
- Track performance against **customizable weekly and monthly goals**.
- Use visual insights (graph & dial) to guide discussions and adjust plans.
- Add, edit, or remove goals based on progress.