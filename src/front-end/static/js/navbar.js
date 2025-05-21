document.addEventListener("DOMContentLoaded", () => {
    const navbar = `
      <nav class="navbar">
        <ul class="nav-links" id="nav-links">
          <li><a href="home.html">Home</a></li>
          
          <!-- Dropdown menu -->
          <li class="dropdown">
            <a href="#" class="dropbtn">Appointments</a>
            <div class="dropdown-content">
              <a href="#">View Appointments</a>
              <a href="#">Create Appointment</a>
              <a href="#">Manage Appointments</a>
            </div>
          </li>
          
          <li><a href="#" class="logoutButton">Logout</a></li>
        </ul>
  
        <!-- Hamburger Menu Icon on the right -->
        <div class="menu-icon" id="menu-icon">
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
        </div>
      </nav>
    `;
  
    // Insert the navbar HTML into the page
    document.getElementById("navbar").innerHTML = navbar;
  
    // Add event listener for logout button
    const logoutButton = document.querySelector(".logoutButton");
    if (logoutButton) {
      logoutButton.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent the default link behavior
        logout();
      });
    }
  
    // Toggle the mobile menu when the hamburger icon is clicked
    const menuIcon = document.getElementById("menu-icon");
    const navLinks = document.getElementById("nav-links");
  
    menuIcon.addEventListener("click", () => {
      navLinks.classList.toggle("active");
    });
  });
  
  function logout() {
    // Clear sessionStorage and redirect to login page
    if (typeof sessionStorage !== 'undefined') {
      sessionStorage.clear();
    }
    window.location.href = "/index.html";
  }
  
  
  
  
  