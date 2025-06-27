# Web page file template
each page of the frontend exists of a html, css and js file.<br>
all html files are made according to the following template:<br>
````html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Blank Page</title>
  <link rel="stylesheet" href="../static/css/home.css" />
</head>
<body>

  <!-- Content goes here -->

  <script src="../static/js/home.js"></script>
</body>
</html>

````

# File structures
the file structure is as follows:<br>

the templates folder had all the html files,<br>
the static folder has the css and js files in their folders as well as all the assets like fonts and images.
![structure.png](structure.png)

## Navigation bar (Patient and Therapist)
The navigation bar is made in JavaScript in this way the navbar can be injected into every HTML file where it is needed. 

The call upon the navbar in an HTML file you need to include this code:

**Patient navigation bar**

```HTML
   <link rel="stylesheet" href="../static/css/navbar.css" />

   <div id="navbar"></div>

   <script src="../static/js/navbar.js"></script>

```
**Therapist navigation bar**

```HTML
   <link rel="stylesheet" href="../static/css/navbar.css" />

   <div id="admin-navbar"></div>

   <script src="../static/js/navbar.js"></script>

```
These lines of code will dynamically inject the navbar on page load. 

### Navbar design
Before making the code for the navbar there was a design made for the navbar in figma. After talking about it with the team there was decided that we would take most of the design from figma, but there will be some changes to the actual navbar made for the app. The most important page for the patients is the homepage, because of this the navbar won't be used as much, so there was decided that the "Hamburger icon" would be used on the actual design and make a hover effect to show the elements of the navbar. The design for the navbar of the therapist is the same, but the only difference is there are some extra elements on the navbar for the therapist.

**Figma design navbar**
![FigmaNavbar](/docs/assets/NavbarFigma.png)

**Actual design for app (Patient)**
![patientNavbar](/docs/assets/patientNavbar.png)

**Actual design for app (Therapist)**
![therapistNavbar](/docs/assets/adminNavbar.png)

### navbar/admin_navbar.js
In this file you will find all the html code for the injection of the navbar and function that are used for the functionality of the navbar.<br>
the navbar has the logo with a line, then HIPPER THERAPUTICS and then another line. these were made using css flex in a container class that was defined in navbar.js<br>
<br>the container class in navbar looks like the following<br>
````js
   <div class="logo-container">
    <div class="logo-line"></div>
    <span class="hippertext">Hipper Therapeutics</span>
    <div class="logo-line"></div>
  </div>
````
<br>
and the flex that is used for these divs works as follows:<br>
<br>

````css
.logo-container{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  font-family: 'Julius Sans One', sans-serif;
  font-weight: bold;
  color: black;
  letter-spacing: 2px;
  position: relative;
  margin-left: 50px;
}

.logo-line{
  margin-left: 10px;
  margin-right: 10px;
  width: 200px;
  height: 1px;
  background-color: black;
}
````
<br>
the logo exists of the name of the company ("Hipper Theraputics") and some lines before and after it<br>

### navbar/admin_navbar.css
In this file you will find all the code for the styling of the navbar.<br>
the navbar of the admin pages works exactly the same.<br>

### Responsive 
The links in the navbar will always be hidden under what is called "a hamburger icon" this will stay the same on phone and on desktop. The only thing that will be different is that the text in the center of the navbar will resize when visiting the page on a different device.

### References
- W3Schools is used to figure out how to make the dropdown menu for the navbar.
- Chatgpt is used to help figuring out some errors in the code.

## Profile page
The profile page is used for patient to view there personal information and they are able to change some setting to their own preferences. Before starting to make the code for this page a design on figma was made and with this design the profile page was made. There is some difference in the visual experience between phone and desktop. On the phone the boxes are vertical instead of horizontally placed for a better user experience.

**Figma design Profile page**
![FigmaProfile](/docs/assets/Figma/ProfilePageDesign.png)

### profile.css
In the css file used to style the profile page you will find all the code that is used to style the page

### profile.js
In this file you will find the function used for the profile page.

**Function getProfile is used to fetch the /profile endpoint that sends the patients personal information.**

```js
function getProfile() {
  fetch("/profile", {
    method: "GET",
    headers: {
      "Accept": "application/json"
    },
    credentials: "include"
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Failed to fetch profile");
    }
    return response.json();
  })
  .then(data => {
    document.getElementById("display-name").textContent = data.name;
    document.getElementById("display-email").textContent = data.email;
    document.getElementById("display-therapist").textContent = data.therapist;
  })
  .catch(error => {
    console.error("Error fetching profile:", error);
  });
}
```
**function setupToggleBar(toggleId) sets up a toggle bar UI component that allows a user to choose between two options.**

```js
function setupToggleBar(toggleId) {
  const toggleBar = document.getElementById(toggleId);
  const halves = toggleBar.querySelectorAll('.half');

  halves.forEach(half => {
    half.addEventListener('click', () => {
      halves.forEach(h => h.classList.remove('selected'));
      half.classList.add('selected');
      
      const selectedValue = half.dataset.value;
      console.log(`${toggleId} selected:`, selectedValue);

    });
  });
}
```

### Responsive
For the responsive design there is decided that placing the boxes vertical would be better for the user experience. This is done with media queries in css.

![ResponsiveProfilePage](/docs/assets/Figma/responsiveProfilePage.png)

### References 
- Figma is used to help with making the design for the website
- W3Schools is used for helping with some problems in the css.

**Chatgpt was used to clean up the written code**

## Login Page
The login page allows patients to securely access their accounts and view their personal progress. Before coding began, a design was created in Figma to ensure the layout, colors, and user flow were clear and user-friendly. This helped guide development and maintain consistency with the overall app design.

**Figma design:**
![FigmaLogin](/docs/assets/Figma/LoginPage.png)

**Actual design:**
![FigmaLogin](/docs/assets/ActualLoginPage.png)

### login html
In the html file for the login page you will find the code for the login form and the image box. In the login form the /login endpoint which has a POST method is also called. In the image box you will find the image of the Hipper logo.

```html
<body>
  <header>
    <div class="header-content">
      <div class="header-line">
        <span>Hipper Therapeutics</span>
      </div>
    </div>
  </header>
  
  <main class="container">
    <section class="login-box">
      <h2>Welcome Back</h2>
      <form action="/login" method="POST">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" required />
      
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required />
      
        <div class="remember">
          <input type="checkbox" id="remember" name="remember" />
          <label for="remember">Remember me</label>
        </div>
      
        <button type="submit">Sign in</button>
        <a href="#" class="forgot">Forgot Password?</a>
      </form>
      
    </section>

    <section class="image-box">
      <div class="logo">
        <img src="../static/assets/HIREZHipperLogoTransparent.png" alt="Hipper Therapeutics Logo" />
      </div>
    </section>
  </main>
```

### login css
In this file you will find all the css code that is used to style is page.

### References 
- Figma is used to help with making the design for the website.

**Chatgpt was used to clean up the written code**

## admin_login
The admin login is used by therapist to login to their account and see their personal information, but also see the data from their patients. The styling of this page is the same as the login page for the patients. The only difference is that it wil send you to a home page only accessible to therapists. On both login pages there is a button that will redirect you to /admin/login on patient page or /login on admin page. In this way it is easy for users to go to the login page that is made for them.

**Figma design:**
![FigmaLogin](/docs/assets/Figma/LoginPage.png)

**Actual design:**
![FigmaLogin](/docs/assets/newLoginPage.png)

### admin_login html
In the html file for the login page you will find the code for the login form and the image box. In the login form the /admin/login endpoint which has a POST method is also called. In the image box you will find the image of the Hipper logo. 

```html
  <header>
    <div class="header-content">
      <div class="header-line">
        <span>Hipper Therapeutics</span>
      </div>
    </div>
  </header>
  
  <main class="container">
    <section class="login-box">
      <h2>Welcome Back</h2>
      <form action="/admin/login" method="POST">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" required />
      
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required />
      
        <div class="remember">
          <input type="checkbox" id="remember" name="remember" />
          <label for="remember">Remember me</label>
        </div>
      
        <button type="submit">Sign in</button>
        <a href="#" class="forgot">Forgot Password?</a>
      </form>
      
    </section>

    <section class="image-box">
      <div class="logo">
        <img src="../static/assets/HIREZHipperLogoTransparent.png" alt="Hipper Therapeutics Logo" />
      </div>
    </section>
  </main>
```

### login css
In this file you will find all the css code that is used to style is page.

### References 
- Figma is used to help with making the design for the website.

**Chatgpt was used to clean up the written code**

## admin_patients

The admin patients is used for therapist to view all their patients and also add new patients if needed.

**Figma Design**
![FigmaDesignPatientsPage](/docs/assets/AdminPatientsPageDesign.png)

**Design Used**
![FigmaDesignPatientsPage](/docs/assets/AdminPatientsPage.png)

### admin_patients.html
In the html file for the admin patients page you will find the code for injected admin-navbar, the patient-card and the addPatient-card.

The patient card is used to display the patients assigned to a therapist. Inside the card, there is a search bar to filter patients by name and a list of patients below it.

The patient data is fetched from the backend before the page is rendered, using Jinja2 to loop through the list. Jinja2 calls Flask's url_for() to generate links to patient detail pages, which are connected to specific Flask routes.

```html
    <div class="patient-card">
      <h3>Patients</h3>
      <input type="text" id="search" placeholder="Search patients by name..." />
      <div id="patient-list" class="display-box">
        {% for patient in patients %}
          <div class="patient-card-item" data-name="{{ patient.name | lower }}">
            <div class="patient-card-box">
              <a href="{{ url_for('admin_patient_details', patient_id=patient.id) }}" style="text-decoration: none; color: inherit;">
              <strong>{{ patient.name }}</strong><br>
              Email: {{ patient.email }}
              </a>
            </div>
          </div>
        {% endfor %}
      </div> 
    </div>
```
The Add Patient card allows a therapist to register a new patient via a form. The form includes required fields for the patient's name, email, and password.

When the form is submitted, it sends a POST request to the backend route '/api/add-patient', which is connected to the Flask function admin_add_patient().

```html
    <div class="addPatient-card">
      <h3>Add Patient</h3>
      <form action="{{ url_for('admin_add_patient') }}" method="POST">
        <label for="name">Name</label>
        <input type="text" id="name" name="name" required />

        <label for="email">Email</label>
        <input type="email" id="email" name="email" required />
      
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required />
    
        <button type="submit" class="patient-button">Add Patient</button>
      </form>
    </div>
```
### admin_patients.css
In this file you will find all the css code that is used to style is page.

### admin_patients.js
The JavaScript file for the admin patients page contains the function that enables search functionality in the patient list.

```javascript
    // Filter patients based on search
    document.addEventListener('DOMContentLoaded', function () {
      const searchInput = document.getElementById("search");
      const patientItems = document.querySelectorAll(".patient-card-item");
  
      searchInput.addEventListener("input", function () {
        const query = this.value.toLowerCase();
  
        patientItems.forEach(item => {
          const name = item.dataset.name;
          item.style.display = name.includes(query) ? "block" : "none";
        });
      });
    });
```

### References
- A youtube video that helped with understand jinja2 was used [Link to video on jinja2](https://www.youtube.com/watch?v=4yaG-jFfePc&t=113s)

**Chatgpt was used to clean up the written code**

# Therapist Dashboard - Guide

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

### Design and readability
- [Typography for Health Information](https://www.nngroup.com/articles/medical-usability/)

###  Web Development
- [MDN Web Docs - HTML Canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)

###  UX & Accessibility
- [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/WCAG21/quickref/)



# Implementing Night-Time Inactivity Filter on the User Homepage

##  What is Built
I developed a dashboard feature that allows users to set a custom night-time inactive period on their homepage. This range is used to exclude those hours from inactivity metrics. If the user doesn’t set a time range, default tracking is used. I also integrated Chart.js to visualize activity and inactivity data.

---

###  Step-by-Step: How it is done

### 1. Set Up Project Structure
```
project/
├── index.html
├── static/
│   ├── css/
│   │   ├── therapist.css
│   │   └── admin_navbar.css
│   └── js/
│       ├── therapist.js
│       └── admin_navbar.js
```

### 2. Include Chart.js in HTML
In `index.html`, I added the Chart.js CDN to the `<head>` so the dashboard can render charts:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
```

### 3. Build the Time Picker Feature in HTML
- Created a modal with two `<input type="time">` fields.
- Added a button for setting the inactive time period.

### 4. Write JavaScript Logic (`therapist.js`)
- Built a function to validate that the start and end time are not equal.
- Supported overnight time ranges (e.g., 10 PM to 6 AM).
- Saved the inactive range to `localStorage` (simulating back-end saving).
- Filtered the inactivity data to exclude the selected period.
- Fallback to default metrics if no range is set.

### 5. Integrate Chart.js for Visual Display
- Created a mixed chart:
  - Bar chart for step counts.
  - Line chart for PAM scores.
- Highlighted inactive periods with a red background.
- Configured dual y-axes for step data and PAM scores.

### 6. Add UI Feedback
- Displayed success and validation messages for user interactions.
- Used CSS animations for modals and notifications.
- Built progress bars and circular indicators to show goal completion.

## Summary

By completing this feature, I learned how to:
- Use `<input type="time">` with JavaScript to capture and validate time ranges.
- Handle 24-hour time logic in JavaScript (including cross-midnight ranges).
- Store user settings locally with `localStorage`.
- Exclude specific time ranges from metrics calculation.
- Integrate and configure Chart.js in a multi-metric dashboard.
- Improve user experience through feedback, validation, and visual indicators.

This setup now provides a smooth and intuitive user experience for controlling night-time exclusion in activity data.

---

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


# CSS Code Documentation

This documentation explains the purpose and design of each section in the CSS code for our Homepage, with references to color theory principles from Figma's guide.

---

##  Global Styles

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
```

**Purpose:** Ensures consistent box sizing and removes default spacing for all elements.

```
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #a8d8ff 0%, #b3e5fc 100%);
  min-height: 100vh;
  color: #333;
}
```

**Notes:**
- Uses a **cool gradient** (light blues) to evoke calm and clarity, inspired by analogous hues in the color wheel.
- Text color `#333` provides good contrast without being harsh black.

---

##  Header Layout

```
.header { ... }
.logo { ... }
.user-info { ... }
.settings-icon { ... }
```

**Purpose:** Creates a **frosted-glass header** using `backdrop-filter` and semi-transparent backgrounds. This gives a modern, airy aesthetic.

- `.settings-icon` includes a **hover animation** (rotation).
- `.user-profile` highlights interaction with hover movement.

---

##  Main Container and Card Layout

```
.container { ... }
.card { ... }
```

**Purpose:** Uses a **CSS Grid** layout to organize content into 3 columns (1 column on smaller screens).

- Cards have soft shadows, rounded corners, and blur effects to give a clean, elevated feel.
- Colors like `rgba(255, 255, 255, 0.95)` are used for semi-transparency while maintaining readability.

---

##  Mood + Activity Section

```
.mood-section { ... }
.mood-emoji { ... }
.activity-item { ... }
.activity-icon { ... }
```

**Color Theory Notes:**
- `.mood-emoji` uses **#ffd93d**, a **warm yellow** to express positivity and energy.
- Icons like `.steps-icon` (`#4caf50`, green) and `.time-icon` (`#2196f3`, blue) follow **analogous harmony** (green-blue palette) for cohesion.

- Includes subtle animations (`@keyframes bounce`) and transitions for interactivity.

---

##  Score Circle Section

```
.score-section { ... }
.score-fill { ... }
@keyframes fillProgress { ... }
```

**Functionality:**
- Displays a circular progress chart using a **conic gradient**.
- Green (`#4caf50`) indicates success, with soft background gray for contrast.
- Animation creates a **filling effect** to visually emphasize progress.

---

##  Goals Section

```
.goals-section { ... }
.goal-item { ... }
.progress-bar { ... }
.progress-fill { ... }
```

- Progress bars use a **green gradient** (`#4caf50` → `#8bc34a`) to represent growth and achievement.
- Streaks are marked with **red** (`#ff6b6b`) for attention and urgency.

---

##  Chart Section

```
.chart-section { ... }
.chart-container { ... }
.bar { ... }
.steps-bar, .pam-bar { ... }
```

- Uses bar charts to display metrics like steps and PAM.
- Color-coded bars:
  - **Blue** (`#2196f3`) for steps = trust, calm
  - **Green** (`#4caf50`) for PAM = balance, wellness
- Smooth transitions and value tooltips enhance usability.

---

##  Responsive Design

```
@media (max-width: 768px) { ... }
```

- Adjusts grid layout, header padding, and chart sizing for mobile screens.
- Ensures usability across devices with consistent visual quality.

---


## Reference link

[Colour Theory](https://www.figma.com/resource-library/what-is-color-theory/)