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

function getProfile() {
  fetch("/settings", {
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

// Run all initializations after the DOM is fully loaded
window.addEventListener("DOMContentLoaded", () => {
  getProfile();
  setupToggleBar('theme-toggle');
  setupToggleBar('font-toggle');
  setupToggleBar('language-toggle');
});
