// A flag to ensure we only run the initial checks once per page load
if (!window.analyticsInitialized) {
    window.analyticsInitialized = true;

    // 1. Quick test to make sure frontend can read your Python Flask API on Render
    fetch('https://river-daz-portfolio-backend.onrender.com/api/status')
        .then(response => response.json())
        .then(data => {
            console.log("SUCCESS! Message from Python backend:", data.message);
        })
        .catch(err => console.error("Frontend can't see the backend yet:", err));

    // 2. Automatically send a visit log to the backend on page load
    recordPageView();
}

function recordPageView() {
    fetch('https://river-daz-portfolio-backend.onrender.com/api/track-visit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({}) 
    })
    .then(response => response.json())
    .then(data => {
        console.log(`[Analytics] Visit tracked successfully! Total views: ${data.total_views}`);
    })
    .catch(err => console.error("[Analytics Error] Failed to log visit:", err));
}

// 3. Function to send event data to our Flask backend
function sendEventToBackend(eventName, buttonText) {
    fetch('https://river-daz-portfolio-backend.onrender.com/api/track-event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            event_name: eventName,
            button_text: buttonText
        })
    })
    .then(response => response.json())
    .then(data => console.log(`[Event Tracked] ${buttonText} (${eventName})`))
    .catch(err => console.error("Event tracking failed:", err));
}

// 4. Set up tracking on specific elements once the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    // Prevent duplicate event listener attachments
    if (window.listenersAttached) return;
    window.listenersAttached = true;
    
    // Track Professional Profile Clicks (LinkedIn, JobStreet)
    const profileButtons = document.querySelectorAll('.profile-btn');
    profileButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetUrl = btn.href || btn.getAttribute('href');
            const buttonText = btn.textContent.trim() || "Professional Profile";
            
            if (targetUrl) {
                sendEventToBackend("click_professional_profile", buttonText);
            }
        });
    });

    // Track Instant Message & Social Links (Email, WhatsApp, Instagram, TikTok)
    const socialButtons = document.querySelectorAll('.social-links-container a');
    socialButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetUrl = btn.href || btn.getAttribute('href');
            const labelSpan = btn.querySelector('.icon-label');
            const buttonText = labelSpan ? labelSpan.textContent.trim() : "Social Link";
            
            if (targetUrl) {
                sendEventToBackend("click_social_link", buttonText);
            }
        });
    });
}, { once: true });

// 5. Fetch and Display Video Recommendations from Flask API
function loadVideoRecommendations(category = 'all') {
    const videoContainer = document.getElementById('featured-videos-container');
    if (!videoContainer) return; // Exit if the container element doesn't exist on this page

    // FIXED: Removed the double fetch() syntax error here
    fetch(`https://river-daz-portfolio-backend.onrender.com/api/recommendations?category=${category}`)
        .then(response => response.json())
        .then(data => {
            videoContainer.innerHTML = ''; // Clear out any loading or placeholder text
            
            if (!data.videos || data.videos.length === 0) {
                videoContainer.innerHTML = `<p class="no-videos">No featured videos found for this category.</p>`;
                return;
            }

            // Loop through the videos and inject them into your HTML structure
            data.videos.forEach(video => {
                const videoCard = document.createElement('div');
                videoCard.className = 'video-card';
                videoCard.innerHTML = `
                    <div class="video-thumbnail-placeholder">🎬</div>
                    <div class="video-info">
                        <h3>${video.title}</h3>
                        <span class="category-badge">${video.category}</span>
                        <a href="${video.url}" class="watch-btn" target="_blank">View Project</a>
                    </div>
                `;
                videoContainer.appendChild(videoCard);
            });
        })
        .catch(err => {
            console.error("Failed to load recommendations from API:", err);
            videoContainer.innerHTML = `<p class="error-msg">Could not load videos right now.</p>`;
        });
}