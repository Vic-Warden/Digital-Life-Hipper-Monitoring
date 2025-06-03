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

## Navigation bar
The navigation bar is made in JavaScript in this way the navbar can be injected into every HTML file where it is needed. 

The call upon the navbar in an HTML file you need to include this code:

```HTML
   <link rel="stylesheet" href="../static/css/navbar.css" />

   <div id="navbar"></div>

   <script src="../static/js/navbar.js"></script>

```
These lines of code will dynamically inject the navbar on page load. 

### Navbar design
Before making the code for the navbar there was a design made for the navbar in figma. After talking about it with the team there was decided that we would take most of the design from figma, but there will be some changes to the actual navbar made for the app. The most important page for the patients is the homepage, because of this the navbar won't be used as much, so there was decided that the "Hamburger icon" would be used on the actual design and make a hover effect to show the elements of the navbar.

**Figma design navbar**
![FigmaNavbar](/docs/assets/NavbarFigma.png)

**Actual design for app**
![FigmaNavbar](/docs/assets/ActualNavbar.png)

### navbar.js
In this file you will find all the html code for the injection of the navbar and function that are used for the functionality of the navbar.

### navbar.css
In this file you will find all the code for the styling of the navbar.

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
In the html file for the login page you will find the code for the login form and the image box. In the login form the /login endpoint which has a POST method is also called. In the image box you will find the image of the Hipper logo. Also the fil

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