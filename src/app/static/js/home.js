// Animate progress bars on load
document.addEventListener('DOMContentLoaded', function() {
    const progressBars = document.querySelectorAll('.progress-fill');
    
    setTimeout(() => {
        progressBars.forEach(bar => {
            const progress = bar.getAttribute('data-progress');
            bar.style.width = progress + '%';
        });
    }, 500);

    // Animate circular progress
    const scoreFill = document.getElementById('scoreFill');

    // Get the actual step value from the HTML
    const currentSteps = parseInt(document.querySelector('.score-number').textContent.trim());

    // Get the goal value from the HTML
    const goalSteps = parseInt(document.querySelector('.score-total').textContent.trim());

    // Calculate the progress in degrees
    const progress = (currentSteps / goalSteps) * 360;
    scoreFill.style.setProperty('--progress', progress + 'deg');

    // Animate chart bars
    const bars = document.querySelectorAll('.bar');
    bars.forEach((bar, index) => {
        const originalHeight = bar.style.height;
        bar.style.height = '0px';
        setTimeout(() => {
            bar.style.height = originalHeight;
        }, 800 + (index * 100));
    });
});

// Toggle chart view
const toggleBtns = document.querySelectorAll('.toggle-btn');
toggleBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        toggleBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
    });
});

// Add hover effects to activity items
const activityItems = document.querySelectorAll('.activity-item');
activityItems.forEach(item => {
    item.addEventListener('mouseenter', function() {
        this.style.transform = 'translateX(10px) scale(1.02)';
    });
    
    item.addEventListener('mouseleave', function() {
        this.style.transform = 'translateX(0) scale(1)';
    });
});

function showChart(period) {
    // Hide all charts
    document.querySelectorAll('[id$="-chart"]').forEach(chart => chart.style.display = 'none');
    
    // Show selected chart
    document.getElementById(period + '-chart').style.display = 'flex';
    
    // Update active button
    document.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
}

