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
The admin login is used by therapist to login to their account and see their personal information, but also see the data from their patients. The styling of this page is the same as the login page for the patients. The only difference is that it wil send you to a home page only accessible to therapists.

**Figma design:**
![FigmaLogin](/docs/assets/Figma/LoginPage.png)

**Actual design:**
![FigmaLogin](/docs/assets/ActualLoginPage.png)

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

````html
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

````html
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