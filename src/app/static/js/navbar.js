document.addEventListener("DOMContentLoaded", () => {
  const navbar = `
<nav class="navbar">
  <div class="nav-left"></div>

  <div class="nav-center">------ Hipper Therapeutics ------</div>

  <div class="dropdown nav-right">
    <button class="dropbtn" aria-label="Menu Toggle" id="menu-button">
      <div class="menu-icon">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
      </div>
    </button>
    <div class="dropdown-content">
      <a href="/home" class="nav-link">Home</a>
      <a href="/settings" class="nav-link">Settings</a>
      <a href="#" class="logoutButton nav-link">Logout</a>
    </div>
  </div>
</nav>

  `;

  // Insert the navbar HTML into the page
  document.getElementById("navbar").innerHTML = navbar;

// Highlight current page in dropdown
// Have to check if this works when we work on local server: extension vscode can't find the paths!
const currentPath = window.location.pathname;
document.querySelectorAll(".nav-link").forEach(link => {
  if (link.getAttribute("href") === currentPath) {
    link.classList.add("active-link");
  }
});

  
  // Add event listener for logout button
  const logoutButton = document.querySelector(".logoutButton");
  if (logoutButton) {
    logoutButton.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent the default link behavior
      logout();
    });
  }

  // Optional: Add toggle behavior if you later implement mobile nav
  const menuButton = document.getElementById("menu-button");
  menuButton?.addEventListener("click", () => {
    const dropdown = document.querySelector(".dropdown-content");
    dropdown.classList.toggle("active"); // You can style `.active` in CSS
  });
});

function logout() {
  fetch("/logout", {
    method: "GET",  // Use GET request to log out
    credentials: "include", // Ensure cookies are sent along with the request
  })
}

  
  
  
  
  