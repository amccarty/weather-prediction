// Climate Impact Predictor Dashboard JavaScript

// Configuration
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'  // Local development
    : 'https://ui-c-pvquos2rbq.merced.obp.outerbounds.com';  // Production API

let tempChart = null;
let precipChart = null;
let currentRegion = 'Austin, TX';

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadRegionData(currentRegion);

    // Auto-refresh every 5 minutes
    setInterval(() => loadRegionData(currentRegion), 5 * 60 * 1000);
});

function setupEventListeners() {
    document.getElementById('regionSelect').addEventListener('change', (e) => {
        currentRegion = e.target.value;
        loadRegionData(currentRegion);
    });

    document.getElementById('refreshBtn').addEventListener('click', () => {
        loadRegionData(currentRegion);
    });
}

async function loadRegionData(region) {
    showLoading();
    hideError();

    try {
        // Load API status
        const statusData = await fetchJSON(`${API_BASE_URL}/status`);

        // Load region predictions
        const predictionsData = await fetchJSON(`${API_BASE_URL}/predictions/${encodeURIComponent(region)}`);

        // Load alerts
        const alertsData = await fetchJSON(`${API_BASE_URL}/alerts`);

        // Update UI
        updateDashboard(predictionsData, statusData, alertsData);
        hideLoading();

    } catch (error) {
        console.error('Error loading data:', error);
        showError(`Failed to load data: ${error.message}`);
        hideLoading();
    }
}

async function fetchJSON(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return response.json();
}

function updateDashboard(predictions, status, alerts) {
    // Update data mode badge
    const dataModeBadge = document.getElementById('dataMode');
    if (status.predictions_loaded && predictions.last_updated !== 'mock-data') {
        dataModeBadge.textContent = 'Real Data';
        dataModeBadge.className = 'badge real-data';
    } else {
        dataModeBadge.textContent = 'Mock Data';
        dataModeBadge.className = 'badge mock-data';
    }

    // Update stats
    document.getElementById('currentTemp').textContent = `${predictions.current_temp}°C`;
    document.getElementById('lastUpdated').textContent = formatLastUpdated(predictions.last_updated);

    // Update API info
    document.getElementById('trainingRunId').textContent = status.training_run_id || 'N/A';
    document.getElementById('refreshRunId').textContent = status.refresh_run_id || 'N/A';
    document.getElementById('apiStatus').textContent = status.status || 'unknown';

    // Update charts
    updateTemperatureChart(predictions.predicted_temp_change);
    updatePrecipitationChart(predictions.precipitation_change);

    // Update extreme events
    updateExtremeEvents(predictions.extreme_event_probabilities);

    // Update alerts
    updateAlerts(alerts);
}

function updateTemperatureChart(tempData) {
    const ctx = document.getElementById('tempChart').getContext('2d');

    if (tempChart) {
        tempChart.destroy();
    }

    tempChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['1 Year', '5 Years', '10 Years'],
            datasets: [{
                label: 'Temperature Change (°C)',
                data: [
                    tempData['1_year'],
                    tempData['5_year'],
                    tempData['10_year']
                ],
                backgroundColor: [
                    'rgba(102, 126, 234, 0.6)',
                    'rgba(118, 75, 162, 0.6)',
                    'rgba(244, 67, 54, 0.6)'
                ],
                borderColor: [
                    'rgba(102, 126, 234, 1)',
                    'rgba(118, 75, 162, 1)',
                    'rgba(244, 67, 54, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Temperature Change (°C)'
                    }
                }
            }
        }
    });
}

function updatePrecipitationChart(precipData) {
    const ctx = document.getElementById('precipChart').getContext('2d');

    if (precipChart) {
        precipChart.destroy();
    }

    precipChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['1 Year', '5 Years', '10 Years'],
            datasets: [{
                label: 'Precipitation Change (%)',
                data: [
                    precipData['1_year'],
                    precipData['5_year'],
                    precipData['10_year']
                ],
                borderColor: 'rgba(33, 150, 243, 1)',
                backgroundColor: 'rgba(33, 150, 243, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Precipitation Change (%)'
                    }
                }
            }
        }
    });
}

function updateExtremeEvents(events) {
    const container = document.getElementById('eventsGrid');
    container.innerHTML = '';

    for (const [eventType, probability] of Object.entries(events)) {
        const card = document.createElement('div');
        card.className = 'event-card';
        card.innerHTML = `
            <h4>${eventType.replace('_', ' ')}</h4>
            <div class="event-probability">${(probability * 100).toFixed(1)}%</div>
        `;
        container.appendChild(card);
    }
}

function updateAlerts(alertsData) {
    const container = document.getElementById('alertsContainer');
    container.innerHTML = '';

    if (!alertsData.alerts || alertsData.alerts.length === 0) {
        container.innerHTML = '<div class="no-alerts">No active alerts at this time</div>';
        return;
    }

    alertsData.alerts.forEach(alert => {
        const card = document.createElement('div');
        card.className = `alert-card ${alert.severity}`;
        card.innerHTML = `
            <h4>${alert.type.replace('_', ' ').toUpperCase()} Alert</h4>
            <p><strong>Region:</strong> ${alert.region}</p>
            <p><strong>Probability:</strong> ${(alert.probability * 100).toFixed(1)}%</p>
            <p><strong>Severity:</strong> ${alert.severity.toUpperCase()}</p>
            <p><strong>Issued:</strong> ${formatLastUpdated(alert.issued_at)}</p>
        `;
        container.appendChild(card);
    });
}

function formatLastUpdated(timestamp) {
    if (!timestamp || timestamp === 'unknown' || timestamp === 'mock-data') {
        return 'Mock Data';
    }

    try {
        const date = new Date(timestamp);
        return date.toLocaleString();
    } catch (e) {
        return timestamp;
    }
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('dashboard').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';
}

function showError(message) {
    const errorEl = document.getElementById('error');
    errorEl.textContent = message;
    errorEl.style.display = 'block';
}

function hideError() {
    document.getElementById('error').style.display = 'none';
}
