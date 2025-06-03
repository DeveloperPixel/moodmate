from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth
from functools import wraps
import pyrebase
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os
import json

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
            'update_profile': '/user/profile/ [PUT]'
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