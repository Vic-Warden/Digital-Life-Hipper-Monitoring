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