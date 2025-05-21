document.addEventListener("DOMContentLoaded", () => {
  const navbar = `
    <nav class="navbar">
      <!-- Left spacer or nav links (can be empty if not used) -->
      <div class="nav-left"></div>

      <!-- Centered text -->
      <div class="nav-center">------ Hipper Therapeutics ------</div>

      <!-- Dropdown menu on the right -->
      <div class="dropdown nav-right">
        <button class="dropbtn" aria-label="Menu Toggle" id="menu-button">
          <div class="menu-icon">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
          </div>
        </button>
        <div class="dropdown-content">
          <a href="#">Home</a>
          <a href="#">Profile</a>
          <a href="#">Settings</a>
          <a href="#" class="logoutButton">Logout</a>
        </div>
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

  // Optional: Add toggle behavior if you later implement mobile nav
  const menuButton = document.getElementById("menu-button");
  menuButton?.addEventListener("click", () => {
    const dropdown = document.querySelector(".dropdown-content");
    dropdown.classList.toggle("active"); // You can style `.active` in CSS
  });
});

// Logout function
function logout() {
  if (typeof sessionStorage !== "undefined") {
    sessionStorage.clear();
  }
  window.location.href = "/index.html";
}

  
  
  
  
  