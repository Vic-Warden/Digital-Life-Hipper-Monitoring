
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
    // Call fetch on page load
    // getPatients();