    let allPatients = [];

    // Fetch patients from the backend
    function getPatients() {
      fetch('/admin/patients', {
        method: 'GET',
        headers: { 'Accept': 'application/json' },
        credentials: 'include'  // if using cookies/session
      })
      .then(response => {
        if (!response.ok) throw new Error("Failed to fetch patients");
        return response.json();
      })
      .then(data => {
        allPatients = data;
        displayPatients(allPatients);
      })
      .catch(error => {
        console.error("Error fetching patients:", error);
      });
    }

    // Display patients in the DOM
    function displayPatients(patients) {
      const container = document.getElementById('patient-list');
      container.innerHTML = '';

      if (patients.length === 0) {
        container.innerHTML = '<p>No patients found.</p>';
        return;
      }

      patients.forEach(patient => {
        const div = document.createElement('div');
        div.className = 'patient-card';
        div.innerHTML = `<strong>${User.name}</strong><br>Email: ${User.email}`;
        container.appendChild(div);
      });
    }

    // Filter patients based on search
    document.getElementById('search').addEventListener('input', function () {
      const query = this.value.toLowerCase();
      const filtered = allPatients.filter(p =>
        p.name.toLowerCase().includes(query)
      );
      displayPatients(filtered);
    });

    // Call fetch on page load
    getPatients();