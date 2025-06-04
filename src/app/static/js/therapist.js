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

// Draw the complete chart
function drawChart(ctx, width, height) {
  const padding = 60;
  const chartWidth = width - padding * 2;
  const chartHeight = height - padding * 2;
  
  // Clear canvas
  ctx.clearRect(0, 0, width, height);
  
  // Draw inactive day backgrounds (red highlights)
  drawInactiveDayBackgrounds(ctx, padding, chartWidth, chartHeight);
  
  // Draw step bars (blue)
  drawStepBars(ctx, padding, chartWidth, chartHeight);
  
  // Draw PAM score line (green)
  drawPamScoreLine(ctx, padding, chartWidth, chartHeight);
  
  // Draw axes and labels
  drawAxesAndLabels(ctx, padding, chartWidth, chartHeight, width, height);
}

// Draw red background for inactive days
function drawInactiveDayBackgrounds(ctx, padding, chartWidth, chartHeight) {
  const barWidth = chartWidth / chartData.dates.length;
  
  chartData.inactiveDays.forEach(dayIndex => {
    const x = padding + dayIndex * barWidth;
    
    ctx.fillStyle = 'rgba(255, 182, 193, 0.3)'; // Light red
    ctx.fillRect(x, padding, barWidth, chartHeight);
  });
}

// Draw step bars
function drawStepBars(ctx, padding, chartWidth, chartHeight) {
  const maxSteps = Math.max(...chartData.steps);
  const barWidth = chartWidth / chartData.dates.length * 0.6;
  const barSpacing = chartWidth / chartData.dates.length;
  
  chartData.steps.forEach((steps, index) => {
    const barHeight = (steps / maxSteps) * chartHeight * 0.8;
    const x = padding + index * barSpacing + (barSpacing - barWidth) / 2;
    const y = padding + chartHeight - barHeight;
    
    // Draw bar
    ctx.fillStyle = '#87CEEB'; // Light blue
    ctx.fillRect(x, y, barWidth, barHeight);
    
    // Draw step count on top of bar
    ctx.fillStyle = '#333';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(steps.toString(), x + barWidth / 2, y - 5);
  });
}

// Draw PAM score line
function drawPamScoreLine(ctx, padding, chartWidth, chartHeight) {
  const maxPamScore = Math.max(...chartData.pamScores);
  const pointSpacing = chartWidth / (chartData.dates.length - 1);
  
  ctx.strokeStyle = '#4CAF50'; // Green
  ctx.lineWidth = 3;
  ctx.beginPath();
  
  chartData.pamScores.forEach((score, index) => {
    const x = padding + index * pointSpacing;
    const y = padding + chartHeight - (score / maxPamScore) * chartHeight * 0.3 - chartHeight * 0.1;
    
    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
    
    // Draw point
    ctx.fillStyle = '#4CAF50';
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, 2 * Math.PI);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(x, y);
  });
  
  ctx.stroke();
  
  // Add PAM score labels
  chartData.pamScores.forEach((score, index) => {
    const x = padding + index * pointSpacing;
    const y = padding + chartHeight - (score / maxPamScore) * chartHeight * 0.3 - chartHeight * 0.1;
    
    ctx.fillStyle = '#4CAF50';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(score.toFixed(1), x, y - 15);
  });
}

// Draw axes and labels
function drawAxesAndLabels(ctx, padding, chartWidth, chartHeight, width, height) {
  // X-axis
  ctx.strokeStyle = '#ccc';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(padding, padding + chartHeight);
  ctx.lineTo(padding + chartWidth, padding + chartHeight);
  ctx.stroke();
  
  // Y-axis
  ctx.beginPath();
  ctx.moveTo(padding, padding);
  ctx.lineTo(padding, padding + chartHeight);
  ctx.stroke();
  
  // Date labels
  const labelSpacing = chartWidth / chartData.dates.length;
  chartData.dates.forEach((date, index) => {
    const x = padding + index * labelSpacing + labelSpacing / 2;
    const y = padding + chartHeight + 20;
    
    ctx.fillStyle = '#666';
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(date.substr(5), x, y); // Show only month-day
  });
  
  // Y-axis labels for steps
  ctx.fillStyle = '#666';
  ctx.font = '11px sans-serif';
  ctx.textAlign = 'right';
  for (let i = 0; i <= 4; i++) {
    const y = padding + chartHeight - (i / 4) * chartHeight;
    const value = (i / 4) * 8000;
    ctx.fillText(value.toString(), padding - 10, y + 3);
  }
  
  // Right Y-axis labels for PAM score
  ctx.textAlign = 'left';
  for (let i = 0; i <= 2; i++) {
    const y = padding + chartHeight * 0.9 - (i / 2) * chartHeight * 0.3;
    const value = (i / 2) * 2.5;
    ctx.fillText(value.toFixed(1), padding + chartWidth + 10, y + 3);
  }
}

// Update circular progress indicator
function updateCircularProgress() {
  const circle = document.querySelector('.progress-ring-fill');
  const radius = 90;
  const circumference = 2 * Math.PI * radius;
  const progress = 370 / 600; // Current score / Total score
  const offset = circumference - (progress * circumference);
  
  circle.style.strokeDasharray = circumference;
  circle.style.strokeDashoffset = offset;
}

// Initialize event handlers
function initializeEventHandlers() {
  // Time selector buttons
  const timeButtons = document.querySelectorAll('.time-btn');
  timeButtons.forEach(button => {
    button.addEventListener('click', function() {
      timeButtons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');
      // Here you could implement different time period views
    });
  });
  
  // Add goal button
  const addBtn = document.querySelector('.add-btn');
  if (addBtn) {
    addBtn.addEventListener('click', function() {
      // Here you could implement add goal functionality
      console.log('Add goal clicked');
    });
  }
  
  // Edit and delete buttons
  const editButtons = document.querySelectorAll('.edit-btn');
  const deleteButtons = document.querySelectorAll('.delete-btn');
  
  editButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      console.log('Edit goal clicked');
      // Implement edit functionality
    });
  });
  
  deleteButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      console.log('Delete goal clicked');
      // Implement delete functionality
    });
  });
}

// Handle window resize
window.addEventListener('resize', function() {
  // Redraw chart on resize
  setTimeout(() => {
    initializeChart();
  }, 100);
});