document.addEventListener("DOMContentLoaded", () => {
  const navbar = `
<nav class="admin-navbar">
  <div class="nav-left"></div>
 
   <div class="logo-container">
    <div class="logo-line"></div>
    <a href="/admin/patients" class="hippertext">Hipper Therapeutics</a>
    <div class="logo-line"></div>
  </div>

<!--  <div class="nav-center">&#45;&#45;&#45;&#45;&#45;&#45; Hipper Therapeutics &#45;&#45;&#45;&#45;&#45;&#45;</div>-->

  <div class="dropdown nav-right">
    <button class="dropbtn" aria-label="Menu Toggle" id="menu-button">
      <div class="menu-icon">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
      </div>
    </button>
    <div class="dropdown-content">
      <a href="/admin/patients" class="nav-link">Patients</a>
      <a href="/admin/manage-devices" class="nav-link">Manage Devices</a>
      <a href="/admin/settings" class="nav-link">Settings</a>
      <a href="/admin/logout" class="nav-link">Logout</a>
    </div>
  </div>
</nav>

  `;

  // Insert the navbar HTML into the page
  document.getElementById("admin-navbar").innerHTML = navbar;

  // Highlight current page in dropdown
  // Have to check if this works when we work on local server: extension vscode can't find the paths!
  const currentPath = window.location.pathname;
  document.querySelectorAll(".nav-link").forEach(link => {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active-link");
    }
  });

  // Optional: Add toggle behavior if you later implement mobile nav
  const menuButton = document.getElementById("menu-button");
  menuButton?.addEventListener("click", () => {
    const dropdown = document.querySelector(".dropdown-content");
    dropdown.classList.toggle("active"); // You can style `.active` in CSS
  });
});
