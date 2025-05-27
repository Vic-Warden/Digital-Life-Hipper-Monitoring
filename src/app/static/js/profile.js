function setupToggleBar(toggleId) {
  const toggleBar = document.getElementById(toggleId);
  const halves = toggleBar.querySelectorAll('.half');

  halves.forEach(half => {
    half.addEventListener('click', () => {
      halves.forEach(h => h.classList.remove('selected'));
      half.classList.add('selected');
      
      const selectedValue = half.dataset.value;
      console.log(`${toggleId} selected:`, selectedValue);

      // Optional: apply changes here, like theme or language
    });
  });
}

// Init toggle bars
setupToggleBar('theme-toggle');
setupToggleBar('font-toggle');
setupToggleBar('language-toggle');
