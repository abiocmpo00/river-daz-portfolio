import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials

# Cleaned up imports from your modules
from analytics import log_visit, get_analytics_summary, log_event
from recommendation import get_videos_by_category

app = Flask(__name__)
CORS(app)

# --- SECURE FIREBASE INITIALIZATION FOR DEPLOYMENT ---
# 1. Checks Render's environment variables first for a variable named "FIREBASE_CREDENTIALS_JSON"
# 2. Falls back to your local file if the environment variable isn't found
firebase_json_env = os.environ.get("FIREBASE_CREDENTIALS_JSON")

if firebase_json_env:
    try:
        # Parse the JSON string directly from Render's environment variables
        cred_dict = json.loads(firebase_json_env)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        print("Firebase successfully initialized from Environment Variable!")
    except Exception as e:
        print(f"Error loading Firebase from environment variable: {e}")
else:
    # Local development fallback
    local_path = "../firebase-credentials.json"
    if os.path.exists(local_path):
        cred = credentials.Certificate(local_path)
        firebase_admin.initialize_app(cred)
        print("Firebase successfully initialized from local JSON file!")
    else:
        print("WARNING: No Firebase credentials found! Analytics logging will fail.")
# -----------------------------------------------------

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "online",
        "message": "Hello River Daz! Your Python backend is officially running smoothly."
    })

@app.route('/api/track-visit', methods=['POST'])
def track_visit():
    # When deployed on Render/behind a proxy, request.remote_addr might show Render's internal IP.
    # We fallback to 'X-Forwarded-For' to grab the actual mobile/desktop visitor's IP.
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_address:
        ip_address = ip_address.split(',')[0].strip() # Get the original client IP
        
    user_agent = request.headers.get('User-Agent', 'Unknown')
    result = log_visit(ip_address, user_agent)
    return jsonify(result)

@app.route('/api/track-event', methods=['POST'])
def track_event():
    event_data = request.get_json() or {}
    event_name = event_data.get('event_name', 'unknown_click')
    button_text = event_data.get('button_text', 'unknown_button')
    result = log_event(event_name, button_text)
    return jsonify(result)

@app.route('/api/analytics-dashboard', methods=['GET'])
def analytics_dashboard():
    summary = get_analytics_summary()
    return jsonify(summary)

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    category = request.args.get('category', 'all') 
    videos = get_videos_by_category(category)
    return jsonify({
        "category": category,
        "videos": videos
    })

if __name__ == '__main__':
    # Use the port assigned by the cloud platform, default to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)