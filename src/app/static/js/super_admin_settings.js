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


async function removeSuperuser(userId, btn) {
    if (!confirm("Really remove super‑user status?")) return;

    try {
        const res = await fetch('/api/remove-superuser', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({user_id: userId})
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Unknown error');

        // On success, remove the item from the DOM
        const item = btn.closest('.superuser-item');
        item.parentNode.removeChild(item);

    } catch (err) {
        alert("Could not demote user: " + err.message);
        console.error(err);
    }
    location.reload();
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

    async function promoteSuperuser() {
    const emailInput = document.getElementById('promote-email');
    const fb = document.getElementById('promote-feedback');
    fb.textContent = '';      // clear old feedback

    const email = emailInput.value.trim().toLowerCase();
    if (!email) {
    fb.textContent = 'Please enter an email.';
    return;
}

    document.getElementById('btn-promote').disabled = true;
    try {
    const resp = await fetch('/api/add-superuser', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({email})
});
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || 'Unknown error');

    // Success: add the new super‑user to the scroll box
    const box = document.querySelector('.display-box-superusers');
    const div = document.createElement('div');
    div.className = 'superuser-item';
    div.setAttribute('data-id', data.superuser.id);
    div.innerHTML = `
        <div class="superuser-info">
          <strong>${data.superuser.name}</strong><br>
          ${data.superuser.email}
        </div>
        <button class="btn-demote" onclick="removeSuperuser(${data.superuser.id}, this)">
          Demote
        </button>
      `;
    box.appendChild(div);

    emailInput.value = '';  // clear input
} catch (err) {
    fb.textContent = err.message;
} finally {
    document.getElementById('btn-promote').disabled = false;
}
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

// Fetch and render therapists on load
async function loadTherapists() {
  const res = await fetch('/api/therapists', { credentials: 'include' });
  const data = await res.json();
  const list = document.querySelector('.therapist-list');
  list.innerHTML = '';
  if (!data.therapists || !data.therapists.length) {
    list.innerHTML = '<div class="therapist-item">No therapists found.</div>';
    return;
  }
  data.therapists.forEach(t => {
    const div = document.createElement('div');
    div.className = 'therapist-item';
    div.dataset.id = t.id;
    div.innerHTML = `
      <div class="therapist-info">
        <strong>${t.name}</strong><br>${t.email}
      </div>
      <button class="btn-delete" onclick="removeTherapist(${t.id}, this)">Delete</button>
    `;
    list.appendChild(div);
  });
}

function isValidEmail(email) {
  // Basic email format: some@domain.tld
  const emailRegex = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  return emailRegex.test(email);
}

async function addTherapist() {
  const name = document.getElementById("therapist-name").value.trim();
  const email = document.getElementById("therapist-email").value.trim();
  const password = document.getElementById("therapist-password").value.trim();

  const feedback = document.getElementById("add-therapist-feedback");
  feedback.textContent = "";
  feedback.style.color = "green";

  if (!name || !email || !password) {
    feedback.textContent = "All fields are required.";
    feedback.style.color = "red";
    return;
  }

  if (!isValidEmail(email)) {
    feedback.textContent = "Invalid email format.";
    feedback.style.color = "red";
    return;
  }

  const res = await fetch('/api/therapists', {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password })
  });

  if (res.ok) {
    feedback.textContent = 'Added!';
    // clear inputs
    document.getElementById('therapist-name').value = '';
    document.getElementById('therapist-email').value = '';
    document.getElementById('therapist-password').value = '';
    // reload list
    loadTherapists();
  } else {
    const err = await res.json();
    feedback.textContent = err.error || err.msg || 'Error';
    feedback.style.color = "red";
    console.error('Add therapist error:', err);
  }
  location.reload();
}


// Delete therapist
async function removeTherapist(id, btn) {
  if (!confirm('Really delete therapist?')) return;
  const res = await fetch(`/api/therapists/${id}`, {
    method: 'DELETE',
    credentials: 'include'
  });
  if (res.ok) {
    btn.closest('.therapist-item').remove();
  } else {
    alert('Failed to delete');
  }

  location.reload();
}

// Filter live
function filterTherapists() {
  const term = document.getElementById('search-therapist').value.toLowerCase();
  document.querySelectorAll('.therapist-item').forEach(div => {
    const txt = div.querySelector('.therapist-info').innerText.toLowerCase();
    div.style.display = txt.includes(term) ? '' : 'none';
  });
}

// initialize
document.addEventListener('DOMContentLoaded', loadTherapists);
window.onload = loadTherapists;