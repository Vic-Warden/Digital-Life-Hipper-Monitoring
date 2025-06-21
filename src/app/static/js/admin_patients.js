
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

    // displays validation or server errors inline, and redirects on success.
    document.addEventListener("DOMContentLoaded", () => {
      const form = document.getElementById("add-patient-form");
      const errorDiv = document.getElementById("error-msg");

      form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // clear any previous error
        errorDiv.textContent = "";

        const formData = new FormData(form);

        try {
          const res = await fetch(form.action, {
            method: form.method,
            body: formData,
            credentials: "same-origin"
          });

          if (!res.ok) {
            // If the server returned a 4xx/5xx
            const text = await res.text();
            errorDiv.textContent = text;
          } else {
            // On success we manually redirect
            window.location.href = "/admin/patients";
          }
        } catch (networkErr) {
          errorDiv.textContent = "Network error—please try again.";
          console.error(networkErr);
        }
      });
    });

    // Call fetch on page load
    // getPatients();