// Chart data based on the screenshot
const chartData = window.chartData;
//const chartData = {
//  // Weekly data
//  weekly: {
//    dates: ['2025-05-19', '2025-05-20', '2025-05-21', '2025-05-22', '2025-05-23', '2025-05-24', '2025-05-25'],
//    steps: [1000, 3000, 5000, 5800, 7200, 4000, 2000],
//    pamScores: [0.25, 1.0, 1.5, 2.0, 2.5, 1.75, 0.5],
//    inactiveDays: [0, 1, 6] // indices of inactive days (red background)
//  },
//  // Daily data (hourly breakdown for today - 2025-05-23)
//  daily: {
//    hours: ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
//    steps: [5, 2, 0, 0, 0, 8, 120, 450, 680, 820, 950, 1100, 1350, 1580, 1750, 1920, 2100, 2350, 2580, 2750, 2900, 3100, 15, 3],
//    pamScores: [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.5, 2.3, 2.1, 1.8, 0.1, 0.0],
//    inactiveHours: [0, 1, 2, 3, 4, 5, 22, 23] // indices of sleeping/inactive hours
//  }
//};

// Current view mode
let currentView = 'daily';

// Inactive period management
let inactivePeriod = {
  startTime: null,
  endTime: null,
  isSet: false
};

// Original inactive minutes (before excluding period)
const originalInactiveMinutes = 180;

// Chart instance
let activityChart = null;

// Initialize the dashboard when DOM loads
document.addEventListener('DOMContentLoaded', function() {
  initializeChart();
  initializeEventHandlers();
  updateCircularProgress();
});

// Initialize Chart.js chart
function initializeChart() {
  const ctx = document.getElementById('activityChart').getContext('2d');
  
  // Start with daily view and set the daily button as active
  updateChart('daily');
  
  // Set the daily button as active on load
  const dailyButton = Array.from(document.querySelectorAll('.time-btn')).find(btn => 
    btn.textContent.toLowerCase().trim() === 'daily'
  );
  if (dailyButton) {
    document.querySelectorAll('.time-btn').forEach(btn => btn.classList.remove('active'));
    dailyButton.classList.add('active');
  }
}

// Update chart based on view mode
function updateChart(viewMode) {
  const ctx = document.getElementById('activityChart').getContext('2d');
  
  let labels, stepsData, pamData, inactiveIndices;
  
  if (viewMode === 'weekly') {
    labels = chartData.weekly.dates.map(date => {
      const d = new Date(date);
      return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    stepsData = chartData.weekly.steps;
    pamData = chartData.weekly.pamScores;
    inactiveIndices = chartData.weekly.inactiveDays;
  } else {
    labels = chartData.daily.hours;
    stepsData = chartData.daily.steps;
    pamData = chartData.daily.pamScores;
    inactiveIndices = chartData.daily.inactiveHours;
  }

  // Destroy existing chart if it exists
  if (activityChart) {
    activityChart.destroy();
  }

  activityChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Steps',
          data: stepsData,
          backgroundColor: labels.map((_, index) => 
            inactiveIndices.includes(index) ? '#ffcccb' : '#4a90e2'
          ),
          borderColor: labels.map((_, index) => 
            inactiveIndices.includes(index) ? '#ff6b6b' : '#357abd'
          ),
          borderWidth: 1,
          yAxisID: 'y'
        },
        {
          label: 'PAM Score',
          data: pamData,
          type: 'line',
          borderColor: '#b8e986',
          backgroundColor: 'rgba(184, 233, 134, 0.1)',
          borderWidth: 3,
          fill: false,
          tension: 0.4,
          pointBackgroundColor: '#b8e986',
          pointBorderColor: '#9ed65f',
          pointBorderWidth: 2,
          pointRadius: 5,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: 'white',
          bodyColor: 'white',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          callbacks: {
            title: function(context) {
              if (viewMode === 'daily') {
                return `Hour: ${context[0].label}`;
              } else {
                return `Date: ${context[0].label}`;
              }
            },
            label: function(context) {
              if (context.datasetIndex === 0) {
                return `Steps: ${context.parsed.y.toLocaleString()}`;
              } else {
                return `PAM Score: ${context.parsed.y.toFixed(1)}`;
              }
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: '#666',
            maxRotation: viewMode === 'daily' ? 45 : 0
          }
        },
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: 'Steps',
            color: '#666'
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            color: '#666',
            callback: function(value) {
              return value.toLocaleString();
            }
          }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: 'PAM Score',
            color: '#666'
          },
          grid: {
            drawOnChartArea: false,
          },
          ticks: {
            color: '#666'
          }
        }
      }
    }
  });
}

// Initialize event handlers
function initializeEventHandlers() {
  // Time selector buttons
  const timeButtons = document.querySelectorAll('.time-btn');
  timeButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      timeButtons.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      
      // Get the view mode from button text
      const viewMode = this.textContent.toLowerCase().trim();
      
      if (viewMode === 'daily' || viewMode === 'weekly') {
        currentView = viewMode;
        updateChart(currentView);
        console.log('Time period selected:', viewMode);
      }
    });
  });

  // Add goal button
  const addBtn = document.querySelector('.add-btn');
  if (addBtn) {
    addBtn.addEventListener('click', function() {
      addNewGoal();
    });
  }
}

function updateCircularProgress() {
  const scoreCircle = document.querySelector('.score-circle');
  const circle = document.querySelector('.progress-ring-fill');

  const current = parseFloat(scoreCircle.dataset.current);
  const total = parseFloat(scoreCircle.dataset.total);
  
  const percentage = (current / total) * 100;

  // Circle calculations
  const radius = 90;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;

  circle.style.strokeDasharray = `${circumference}`;
  circle.style.strokeDashoffset = offset;
}

// Calculate excluded minutes based on time period
function calculateExcludedMinutes(startTime, endTime) {
  const start = new Date(`2000-01-01T${startTime}:00`);
  const end = new Date(`2000-01-01T${endTime}:00`);
  
  // Handle overnight periods
  if (end < start) {
    end.setDate(end.getDate() + 1);
  }
  
  const diffMs = end - start;
  const diffMinutes = Math.floor(diffMs / (1000 * 60));
  
  // Return a portion of the excluded time (simplified calculation)
  // In a real app, this would be more sophisticated
  return Math.min(diffMinutes, 120); // Cap at 2 hours for demo
}

// Format time for display
function formatTime(timeString) {
  const [hours, minutes] = timeString.split(':');
  const hour = parseInt(hours);
  const ampm = hour >= 12 ? 'PM' : 'AM';
  const displayHour = hour % 12 || 12;
  return `${displayHour}:${minutes} ${ampm}`;
}

// Load saved period from localStorage
function loadSavedPeriod() {
  const savedPeriod = localStorage.getItem('inactivePeriod');
  if (savedPeriod) {
    try {
      inactivePeriod = JSON.parse(savedPeriod);
      updatePeriodDisplay();
      updateInactiveMinutes();
    } catch (error) {
      console.error('Error loading saved period:', error);
      // Reset to default if corrupted
      inactivePeriod = {
        startTime: null,
        endTime: null,
        isSet: false
      };
    }
  }
}

// Save period to backend (localStorage simulation)
function savePeriodToBackend(period) {
  try {
    localStorage.setItem('inactivePeriod', JSON.stringify(period));
    console.log('Period saved to backend:', period);
  } catch (error) {
    console.error('Error saving period:', error);
    showNotification('Error saving period. Please try again.', 'error');
  }
}

// Show notification
function showNotification(message, type = 'info') {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  
  // Style the notification
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    color: white;
    font-weight: 500;
    z-index: 9999;
    animation: slideInRight 0.3s ease;
    max-width: 300px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  `;
  
  // Set background color based on type
  switch (type) {
    case 'success':
      notification.style.backgroundColor = '#4CAF50';
      break;
    case 'error':
      notification.style.backgroundColor = '#f44336';
      break;
    case 'warning':
      notification.style.backgroundColor = '#ff9800';
      break;
    default:
      notification.style.backgroundColor = '#2196F3';
  }
  
  // Add to DOM
  document.body.appendChild(notification);
  
  // Remove after 3 seconds
  setTimeout(() => {
    notification.style.animation = 'slideOutRight 0.3s ease';
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 300);
  }, 3000);
}

function deleteGoal(button) {
  if (confirm('Are you sure you want to delete this goal?')) {
    const goalItem = button.closest('.goal-item');
    goalItem.style.animation = 'fadeOut 0.3s ease';
    setTimeout(() => {
      goalItem.remove();
      showNotification('Goal deleted successfully!', 'success');
    }, 300);
  }
}

function addNewGoal() {
  const goalName = prompt('Enter goal name:');
  if (!goalName) return;
  
  const goalTarget = prompt('Enter target value:');
  if (!goalTarget) return;
  
  const goalCurrent = prompt('Enter current value:', '0');
  if (goalCurrent === null) return;
  
  // Create new goal element
  const goalsPanel = document.querySelector('.client-goals-panel');
  const addGoalElement = document.querySelector('.add-goal');
  
  const newGoal = document.createElement('div');
  newGoal.className = 'goal-item';
  newGoal.style.animation = 'fadeIn 0.3s ease';
  
  const percentage = (parseInt(goalCurrent) / parseInt(goalTarget)) * 100;
  
  newGoal.innerHTML = `
    <div class="goal-header">
      <span class="goal-label">${goalName}</span>
      <div class="goal-actions">
        <span class="goal-value">${goalCurrent} / ${goalTarget}</span>
        <button class="delete-btn" onclick="deleteGoal(this)">🗑️</button>
      </div>
    </div>
    <div class="goal-progress">
      <div class="goal-progress-fill" style="width: ${Math.min(percentage, 100)}%"></div>
    </div>
  `;
  
  goalsPanel.insertBefore(newGoal, addGoalElement);
  showNotification('Goal added successfully!', 'success');
}

// Add CSS animations if not already present
if (!document.querySelector('#dynamic-animations')) {
  const style = document.createElement('style');
  style.id = 'dynamic-animations';
  style.textContent = `
    @keyframes slideInRight {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    
    @keyframes slideOutRight {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(100%);
        opacity: 0;
      }
    }
    
    @keyframes fadeOut {
      from {
        opacity: 1;
        transform: scale(1);
      }
      to {
        opacity: 0;
        transform: scale(0.95);
      }
    }
    
    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: scale(0.95);
      }
      to {
        opacity: 1;
        transform: scale(1);
      }
    }
  `;
  document.head.appendChild(style);
}

document.addEventListener('DOMContentLoaded', updateCircularProgress);