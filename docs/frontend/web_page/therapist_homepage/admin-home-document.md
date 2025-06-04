# Therapist Dashboard - Setup Guide

##  Project Overview
This is a modern therapist dashboard that displays client data, activity charts, and goal management. The dashboard includes:
- Client metrics (Weekly PAM, Inactive Minutes)
- Interactive activity chart with steps and PAM scores
- Goal management system (add, edit, delete goals)
- Responsive design with glassmorphism effects

---

##  File Structure Setup

### Step 1: Create Your Project Folder
Create a new folder on your computer for the project:
```
therapist-dashboard/
├── index.html
└── static/
    ├── css/
    │   └── therapist.css
    └── js/
        └── therapist.js
```

### Step 2: Create the Folders
1. Create a main folder called `therapist-dashboard`
2. Inside it, create a folder called `static`
3. Inside `static`, create two folders: `css` and `js`

---

##  HTML File (admin_home.html)

### Purpose
The HTML file creates the structure and layout of the dashboard with three main sections:
- **Left Panel**: Client data and metrics
- **Center Panel**: Activity chart
- **Right Panel**: Goal management

### Key Components
- **Header**: Logo and user profile
- **Client Data Panel**: Shows weekly PAM (11/20), inactive minutes (180), and circular progress (370/600)
- **Activity Chart**: Interactive chart showing steps, PAM scores, and inactive days
- **Goals Panel**: Displays goals with progress bars and edit/delete buttons


---

##  CSS File (therapist.css)

### Purpose
The CSS file styles the dashboard with a modern, professional look using:
- **Glassmorphism effects**: Blurred backgrounds with transparency
- **Responsive design**: Works on desktop, tablet, and mobile
- **Color scheme**: Blue gradient background with green accents

### Key Design Features
- **Blue gradient background** (#a8d8f0 to #e6f3ff): Calm and professional
- **Green accents** (#4CAF50): Indicate progress and positivity
- **Red highlights** (rgba(255, 182, 193, 0.3)): Signal inactive periods
- **White/gray tones**: Ensure clarity and medical aesthetic
- **Layout**: CSS Grid
- **Fonts**: Modern sans-serif for readability

---

##  JavaScript File (therapist.js)

### Purpose
Handles all interactive functionality and visualizations.

### Main Functions
- `initializeChart()`: Draws step bars, PAM line, and highlights inactive days
- `addNewGoal()`: Adds new goals based on user input
- `editGoal(button)`: Edits selected goal
- `deleteGoal(button)`: Removes selected goal with confirmation
- `updateCircularProgress()`: Animates progress ring
- Event listeners for time toggles and button actions

### Data Structure Example (hardcoded numbers for the prototype)
```javascript
const chartData = {
  dates: ['2025-05-19', '2025-05-20', ...],
  steps: [1000, 3000, 5000, ...],
  pamScores: [0.25, 1.0, 1.5, ...],
  inactiveDays: [0, 1, 4, 6]
};
```

---

##  How I Run the Dashboard to see what i'm working on

### VS Code Live Server
1. Install VS Code + Live Server extension
2. Open project folder
3. Right-click `admin_home.html` → "Open with Live Server"

---

##  Features & Functionality

###  Features
- Interactive chart with dynamic data
- Add/edit/delete goals
- Responsive and accessible layout
- Modern glassmorphism style

###  Customization
- Edit `chartData` in JS
- Update styles in CSS
- Change goal structure in HTML

---

##  Troubleshooting

1. **Chart Missing?** Check `<canvas id="activityChart">` and JS import path.
2. **CSS Not Applying?** Ensure correct folder structure and relative paths.
3. **Buttons Not Responding?** Look for JavaScript errors in console.
4. **Goal Data Lost?** Page refresh resets in-memory data.

---

##  Technical Notes

- No external data or persistent storage
- Goals reset on page reload (it is currently only stored locally not in the database yet)

---

##  Future Enhancements

- LocalStorage/database support
- Chart export (PDF/PNG)
- More time ranges (monthly/yearly)
- Client switching and real-time data
- Enhanced accessibility features

---


##  References

###  Color Theory
- [What is Color Theory? - Figma](https://www.figma.com/resource-library/what-is-color-theory/)

###  Web Development
- [MDN Web Docs - HTML Canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)

###  UX & Accessibility
- [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/WCAG21/quickref/)


