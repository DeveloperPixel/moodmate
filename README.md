# MoodMate API

A Flask-based REST API for emotion analysis and user management using Firebase authentication.

## Features
- User authentication (register, login, logout)
- Profile management
- Protected routes
- Firebase integration

## Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `.\venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file with required environment variables
6. Run the application: `flask run`

## API Endpoints
- `/api/register` [POST] - Register new user
- `/api/login` [POST] - User login
- `/api/logout` [POST] - User logout
- `/user/profile/` [GET] - Get user profile
- `/user/profile/` [PUT] - Update user profile