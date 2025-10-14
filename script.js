// Carousel auto-rotation
document.addEventListener('DOMContentLoaded', function() {
    // Mode selection on modes page
    const modeOptions = document.querySelectorAll('.mode-option');
    modeOptions.forEach(option => {
        option.addEventListener('click', function() {
            modeOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
            const mode = this.getAttribute('data-mode');
            document.getElementById('mode').value = mode;
        });
    });

    // Search bar functionality
    const searchButton = document.getElementById('searchButton');
    const searchInput = document.getElementById('searchInput');
    if (searchButton && searchInput) {
        searchButton.addEventListener('click', function() {
            const location = searchInput.value.trim();
            if (location) {
                // Redirect to itinerary page with the searched location
                window.location.href = `itinerary.html?location=${encodeURIComponent(location)}`;
            }
        });

        // Allow Enter key to trigger search
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchButton.click();
            }
        });
    }

    // Travel form submission
    const travelForm = document.getElementById('travelForm');
    if (travelForm) {
        travelForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const mode = formData.get('mode');
            const location = formData.get('location');
            const date = formData.get('date');

            // Placeholder for API call - Replace with actual API integration
            searchTravelOptions(mode, location, date);
        });
    }

    // Itinerary form submission
    const itineraryForm = document.getElementById('itineraryForm');
    if (itineraryForm) {
        itineraryForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const location = formData.get('location');
            const duration = formData.get('duration');

            // Placeholder for API call - Replace with actual API integration
            generateItinerary(location, duration);
        });
    }

    // Pre-fill itinerary form if location is passed via URL
    const urlParams = new URLSearchParams(window.location.search);
    const searchLocation = urlParams.get('location');
    if (searchLocation && document.getElementById('itineraryLocation')) {
        document.getElementById('itineraryLocation').value = searchLocation;
    }
});

// Function to search travel options (Real API call)
function searchTravelOptions(mode, location, date) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<p>Loading travel options...</p>';

    fetch('http://localhost:5000/api/search_transport', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            mode: mode,
            location: location,
            date: date
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayTravelResults(data);
        } else {
            resultsDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        resultsDiv.innerHTML = '<p class="error">Failed to load travel options. Please try again.</p>';
    });
}

// Function to display travel results
function displayTravelResults(data) {
    const resultsDiv = document.getElementById('results');
    let html = `<h3>Travel Options for ${data.location} on ${data.date}</h3>`;
    html += `<p><strong>Estimated Distance:</strong> ${data.distance_km} km</p>`;

    html += '<div class="transport-recommendations">';
    data.recommendations.forEach(rec => {
        html += `
            <div class="transport-option">
                <h4>${rec.name}</h4>
                <p>${rec.description}</p>
                <div class="option-details">
                    <span><strong>Estimated Time:</strong> ${rec.estimated_time}</span>
                    <span><strong>Cost:</strong> ₹${rec.estimated_cost}</span>
                    <span><strong>Comfort:</strong> ${'★'.repeat(Math.round(rec.comfort_rating))}</span>
                    <span><strong>Availability:</strong> ${rec.availability}</span>
                </div>
            </div>
        `;
    });
    html += '</div>';
    resultsDiv.innerHTML = html;
}

// Function to generate itinerary (Real API call)
function generateItinerary(location, duration) {
    const resultsDiv = document.getElementById('itineraryResults');
    resultsDiv.innerHTML = '<p>Generating your personalized itinerary...</p>';

    fetch('http://localhost:5000/api/generate_itinerary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            location: location,
            duration: parseInt(duration)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayItinerary(data);
        } else {
            resultsDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        resultsDiv.innerHTML = '<p class="error">Failed to generate itinerary. Please try again.</p>';
    });
}

// Function to display itinerary
function displayItinerary(data) {
    const resultsDiv = document.getElementById('itineraryResults');
    const itinerary = data.itinerary;

    let html = `
        <div class="itinerary-header">
            <h3>${itinerary.duration}-Day Itinerary for ${itinerary.location}</h3>
            <div class="itinerary-meta">
                <span><strong>Best Time to Visit:</strong> ${itinerary.best_time_to_visit}</span>
                <span><strong>Rating:</strong> ${'★'.repeat(Math.round(itinerary.rating))}</span>
                <span><strong>Estimated Cost:</strong> ₹${itinerary.total_estimated_cost}</span>
            </div>
        </div>
    `;

    itinerary.days.forEach(day => {
        html += `<div class="day-plan">`;
        html += `<h4>Day ${day.day}</h4>`;
        html += '<ul>';
        day.activities.forEach(activity => {
            html += `<li>${activity}</li>`;
        });
        html += '</ul>';
        html += '</div>';
    });

    // Add similar locations
    if (data.similar_locations && data.similar_locations.length > 0) {
        html += '<div class="similar-locations">';
        html += '<h4>You might also like:</h4>';
        html += '<div class="similar-grid">';
        data.similar_locations.forEach(loc => {
            html += `
                <div class="similar-location">
                    <h5>${loc.name}</h5>
                    <p>Rating: ${'★'.repeat(Math.round(loc.rating))}</p>
                    <p>Features: ${loc.features.join(', ')}</p>
                </div>
            `;
        });
        html += '</div></div>';
    }

    resultsDiv.innerHTML = html;
}