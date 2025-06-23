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

// Filter patients based on search
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById("search-device");
    const patientItems = document.querySelectorAll(".device-card-item");

    searchInput.addEventListener("input", function () {
        const query = this.value.toLowerCase();

        patientItems.forEach(item => {
            const name = item.dataset.name;
            item.style.display = name.includes(query) ? "block" : "none";
        });
    });
});

function sendDeviceBinding() {
    const deviceId = document.getElementById('device_id_input').value;
    const patientId = document.getElementById('patient_id_input').value;

    fetch("/api/bind_device_to_patient", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token() }}"
        },
        body: JSON.stringify({
            device_id: deviceId,
            patient_id: patientId
        })
    })
        .then(async response => {
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || "Network response was not ok");
            }
            alert(data.message || "Device bound successfully!");
            location.reload();
        })
        .catch(error => {
            console.error("There was an error:", error);
            alert(`Failed to bind device: ${error.message}`);
        });
}

function unbindDeviceFromPatient() {
    const deviceId = document.getElementById('device_id_input').value;
    const patientId = document.getElementById('patient_id_input').value;

    fetch("/api/unbind_device_to_patient", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token() }}"
        },
        body: JSON.stringify({
            device_id: deviceId,
            patient_id: patientId
        })
    })
        .then(async response => {
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || "Network response was not ok");
            }
            alert(data.message || "Device unbound successfully!");
            location.reload();
        })
        .catch(error => {
            console.error("There was an error:", error);
            alert(`Failed to unbind device: ${error.message}`);
        });
}

function addPamDevice() {
const label = document.getElementById('new_pam_label').value.trim();
const mac = document.getElementById('new_pam_mac').value.trim();

    if (!label || !mac) {
        alert('Please enter both PAM device label and MAC address.');
        return;
    }

    // Send data to backend using fetch (AJAX)
    fetch('/admin/add_pam_device', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            device_label: label,
            device_mac_addr: mac
        })
    })
    .then(response => {
        if (response.ok) {
        alert('PAM device added successfully!');
        window.location.reload(); // Reload page to show new device
    } else {
        response.text().then(text => alert('Error: ' + text));
    }
})
    .catch(err => alert('Request failed: ' + err));
}

document.getElementById('toggle-unoccupied-devices').addEventListener('click', function () {
    const items = document.querySelectorAll('.device-card-item');
    const showOnlyUnoccupied = this.dataset.filter !== 'on';
    this.dataset.filter = showOnlyUnoccupied ? 'on' : 'off';
    this.textContent = showOnlyUnoccupied ? 'Show All Devices' : 'Show Only Unoccupied Devices';

    items.forEach(item => {
        const isOccupied = item.dataset.occupied === 'true';
        item.style.display = showOnlyUnoccupied && isOccupied ? 'none' : 'block';
    });
});