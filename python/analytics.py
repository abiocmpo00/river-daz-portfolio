import datetime
from firebase_admin import firestore

# Initialize Firestore client (it uses the Firebase app initialized in app.py)
def get_db():
    return firestore.client()

def log_visit(ip_address, user_agent):
    """Saves a unique website visit to Cloud Firestore."""
    try:
        db = get_db()
        
        visit_data = {
            "ip_address": ip_address,
            "user_agent": user_agent,
            "timestamp": datetime.datetime.now(datetime.timezone.utc)
        }
        
        # Add a new document to the 'visits' collection
        ref = db.collection("visits").add(visit_data)
        
        # Get total view count across the entire collection
        total_views = len(list(db.collection("visits").list_documents()))
        
        return {
            "status": "success",
            "message": "Visit logged to Firebase cloud successfully!",
            "total_views": total_views
        }
    except Exception as e:
        print(f"Error logging visit to Firebase: {e}")
        return {"status": "error", "message": str(e), "total_views": 0}

def log_event(event_name, button_text):
    """Saves a button or link click event to Cloud Firestore."""
    try:
        db = get_db()
        
        event_data = {
            "event_name": event_name,
            "button_text": button_text,
            "timestamp": datetime.datetime.now(datetime.timezone.utc)
        }
        
        # Add a new document to the 'events' collection
        db.collection("events").add(event_data)
        
        return {
            "status": "success",
            "message": f"Event '{button_text}' tracked in Firebase!"
        }
    except Exception as e:
        print(f"Error logging event to Firebase: {e}")
        return {"status": "error", "message": str(e)}

def get_analytics_summary():
    """Fetches total counts from Firestore for your dashboard preview."""
    try:
        db = get_db()
        
        total_visits = len(list(db.collection("visits").list_documents()))
        total_events = len(list(db.collection("events").list_documents()))
        
        return {
            "total_views": total_visits,
            "total_clicks": total_events
        }
    except Exception as e:
        return {"total_views": 0, "total_clicks": 0, "error": str(e)}