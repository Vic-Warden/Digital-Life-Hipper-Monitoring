function setupToggleBar(toggleId) {
  const toggleBar = document.getElementById(toggleId);
  const halves = toggleBar.querySelectorAll('.half');

  halves.forEach(half => {
    half.addEventListener('click', () => {
      halves.forEach(h => h.classList.remove('selected'));
      half.classList.add('selected');

      const selectedValue = half.dataset.value;
      console.log(`${toggleId} selected:`, selectedValue);

      if (toggleId === 'font-toggle') {
        document.body.classList.toggle('font-large', selectedValue === '1');
        document.body.classList.toggle('font-normal', selectedValue === '0');
      }
    });
  });

    // ✅ Apply font-size class on page load
  if (toggleId === 'font-toggle') {
    const selected = toggleBar.querySelector('.selected')?.dataset.value;
    if (selected) {
      document.body.classList.toggle('font-large', selected === '1');
      document.body.classList.toggle('font-normal', selected === '0');
    }
  }
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

function saveSettings() {
  // Get the selected values from the toggle bars
  const dark_mode = document.querySelector('#theme-toggle .selected').dataset.value;
  const large_font = document.querySelector('#font-toggle .selected').dataset.value;
  const language = document.querySelector('#language-toggle .selected').dataset.value;

  // Create the settings object to send to the server
  const settings = {
    dark_mode: parseInt(dark_mode),
    large_font: parseInt(large_font),
    language: language
  };

  // Send the settings to the server
  fetch("/settings", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    credentials: "include", // Include credentials for session management
    body: JSON.stringify(settings)
  })
    // Show  a message based on the server response
    .then(response => response.json())
    .then(data => {
      const oldMsg = document.querySelector('.return-message');
      if (oldMsg) oldMsg.remove();

      const msgContainer = document.createElement('div');
      msgContainer.className = 'return-message';

      const msgSpan = document.createElement('span');
      msgSpan.className = 'message-content';

      if (data.msg) {
        msgSpan.textContent = data.msg;
      } else if (data.error) {
        msgSpan.textContent = data.error;
        msgContainer.style.backgroundColor = 'rgb(255, 150, 150)';
      }

      msgContainer.appendChild(msgSpan);

      const parentContainer = document.querySelector('.parent-container');
      parentContainer.insertBefore(msgContainer, parentContainer.children[0]);

      // Fade out after 7 seconds, remove after 9 seconds
      setTimeout(() => {
        msgContainer.classList.add('fade-out');
      }, 5000);

      setTimeout(() => {
        msgContainer.remove();
      }, 6000);
    })
};