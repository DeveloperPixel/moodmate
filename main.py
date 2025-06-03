from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth
from functools import wraps
import pyrebase
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Firebase configuration
firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
}

# Initialize Firebase Admin SDK
if os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON'):
    google_creds = json.loads(os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON'))
    cred = credentials.Certificate(google_creds)
else:
    cred = credentials.Certificate("config/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebase_config)
pb_auth = firebase.auth()

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        try:
            # Extract token from Bearer token
            token = auth_header.split(' ')[1]
            # Verify Firebase token
            decoded_token = auth.verify_id_token(token)
            request.user = decoded_token
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 401
            
    return decorated_function

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not email or not password or not name:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create user in Firebase
        user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )
        
        return jsonify({
            'message': 'Successfully registered',
            'user_id': user.uid,
            'email': user.email,
            'name': user.display_name
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400
        
        # Sign in with email and password
        user = pb_auth.sign_in_with_email_and_password(email, password)
        
        # Get user info
        user_info = auth.get_user(user['localId'])
        
        return jsonify({
            'message': 'Successfully logged in',
            'user_id': user_info.uid,
            'email': user_info.email,
            'name': user_info.display_name,
            'id_token': user['idToken']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/logout', methods=['POST'])
@require_auth
def logout():
    try:
        # Firebase doesn't have a server-side logout
        # Client should remove the token
        return jsonify({'message': 'Successfully logged out'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Protected route example
@app.route('/api/protected', methods=['GET'])
@require_auth
def protected_route():
    user_id = request.user['uid']
    return jsonify({
        'message': 'Access granted',
        'user_id': user_id
    })

@app.route('/user/profile/', methods=['GET'])
@require_auth
def get_profile():
    try:
        user_id = request.user['uid']
        user = auth.get_user(user_id)
        
        return jsonify({
            'user_id': user.uid,
            'email': user.email,
            'name': user.display_name,
            'photo_url': user.photo_url,
            'email_verified': user.email_verified
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/user/profile/', methods=['PUT'])
@require_auth
def update_profile():
    try:
        user_id = request.user['uid']
        data = request.get_json()
        
        update_params = {}
        if 'display_name' in data:
            update_params['display_name'] = data['display_name']
        if 'photo_url' in data:
            update_params['photo_url'] = data['photo_url']
        
        # Update user in Firebase
        user = auth.update_user(
            user_id,
            **update_params
        )
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user_id': user.uid,
            'email': user.email,
            'name': user.display_name,
            'photo_url': user.photo_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/emotions', methods=['POST'])
@require_auth
def save_emotion():
    try:
        user_id = request.user['uid']
        data = request.get_json()
        
        # Validate required fields
        if not data.get('emotion') or not data.get('intensity'):
            return jsonify({'error': 'Emotion and intensity are required'}), 400
            
        # Get Firebase Realtime Database reference
        db = firebase.database()
        
        # Create emotion data with timestamp as key for better querying
        emotion_data = {
            'emotion': data['emotion'],
            'intensity': int(data['intensity']),  # Ensure integer
            'note': data.get('note', ''),
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id
        }
        
        # Save to Firebase using timestamp as part of the path
        db.child('users').child(user_id).child('emotions').push(emotion_data)
        
        return jsonify({
            'message': 'Emotion saved successfully',
            'data': emotion_data
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/emotions/history', methods=['GET'])
@require_auth
def get_emotion_history():
    try:
        user_id = request.user['uid']
        period = request.args.get('period', 'week')  # Default to week
        
        # Get Firebase Realtime Database reference
        db = firebase.database()
        
        # Calculate date range
        end_date = datetime.now()
        if period == 'week':
            start_date = end_date - timedelta(days=7)
        elif period == 'month':
            start_date = end_date - timedelta(days=30)
        elif period == 'year':
            start_date = end_date - timedelta(days=365)
        else:
            return jsonify({'error': 'Invalid period'}), 400
            
        # Query emotions for the user within date range
        emotions = db.child('users').child(user_id).child('emotions').get()
        
        emotion_history = []
        if emotions.each():
            for emotion in emotions.each():
                data = emotion.val()
                emotion_date = datetime.fromisoformat(data['timestamp'])
                
                if start_date <= emotion_date <= end_date:
                    emotion_history.append({
                        'id': emotion.key(),
                        'emotion': data['emotion'],
                        'intensity': data['intensity'],
                        'note': data.get('note', ''),
                        'timestamp': data['timestamp']
                    })
        
        # Calculate statistics
        stats = {
            'total_entries': len(emotion_history),
            'emotion_frequency': {},
            'average_intensity': 0
        }
        
        if emotion_history:
            # Calculate emotion frequency
            for entry in emotion_history:
                stats['emotion_frequency'][entry['emotion']] = \
                    stats['emotion_frequency'].get(entry['emotion'], 0) + 1
            
            # Calculate average intensity
            total_intensity = sum(entry['intensity'] for entry in emotion_history)
            stats['average_intensity'] = round(total_intensity / len(emotion_history), 2)
        
        return jsonify({
            'period': period,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'emotions': emotion_history,
            'statistics': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Update the home endpoint to include new routes
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Welcome to MoodMate API',
        'version': '1.0',
        'endpoints': {
            'register': '/api/register [POST]',
            'login': '/api/login [POST]',
            'logout': '/api/logout [POST]',
            'protected': '/api/protected [GET]',
            'get_profile': '/user/profile/ [GET]',
            'update_profile': '/user/profile/ [PUT]',
            'save_emotion': '/api/emotions [POST]',
            'get_emotion_history': '/api/emotions/history?period={week|month|year} [GET]'
        }
    })

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'message': 'API is working correctly'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)