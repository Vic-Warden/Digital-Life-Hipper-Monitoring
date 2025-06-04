// Chart data with numbers and scores
const chartData = {
  dates: ['2025-05-19', '2025-05-20', '2025-05-21', '2025-05-22', '2025-05-23', '2025-05-24', '2025-05-25'],
  steps: [1000, 3000, 5000, 5800, 7200, 4000, 2000],
  pamScores: [0.25, 1.0, 1.5, 2.0, 2.5, 1.75, 0.5],
  inactiveDays: [0, 1, 4, 6] // indices of inactive days (red background)
};

// Initialize the dashboard when DOM loads
document.addEventListener('DOMContentLoaded', function() {
  initializeChart();
  initializeEventHandlers();
  updateCircularProgress();
});

// Initialize the activity chart
function initializeChart() {
  const canvas = document.getElementById('activityChart');
  const ctx = canvas.getContext('2d');
  
  // Set canvas dimensions
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * window.devicePixelRatio;
  canvas.height = rect.height * window.devicePixelRatio;
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  
  drawChart(ctx, rect.width, rect.height);
}