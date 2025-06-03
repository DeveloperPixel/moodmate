# MoodMate API Documentation

## Base Information
- **API Version**: 1.0
- **Base URL (Local)**: `http://localhost:5000`
- **Base URL (Production)**: `https://moodmate-api-r6y2.onrender.com`
- **Authentication**: Bearer Token
- **Content-Type**: application/json

## Authentication
All protected endpoints require an Authorization header:
```
Authorization: Bearer YOUR_TOKEN
```

## Endpoints

### 1. Health Check
```http
GET /test
```
**Response**:
```json
{
    "status": "success",
    "message": "API is working correctly"
}
```

### 2. User Registration
```http
POST /api/register
```
**Body**:
```json
{
    "email": "test@example.com",
    "password": "test123",
    "name": "Test User"
}
```
**Response** (201 Created):
```json
{
    "message": "Successfully registered",
    "user_id": "uid123",
    "email": "test@example.com",
    "name": "Test User"
}
```

### 3. User Login
```http
POST /api/login
```
**Body**:
```json
{
    "email": "test@example.com",
    "password": "test123"
}
```
**Response**:
```json
{
    "message": "Successfully logged in",
    "user_id": "uid123",
    "email": "test@example.com",
    "name": "Test User",
    "id_token": "YOUR_AUTH_TOKEN"
}
```

### 4. User Logout
```http
POST /api/logout
```
**Headers**: Authorization Bearer Token
**Response**:
```json
{
    "message": "Successfully logged out"
}
```

### 5. Get User Profile
```http
GET /user/profile/
```
**Headers**: Authorization Bearer Token
**Response**:
```json
{
    "user_id": "uid123",
    "email": "test@example.com",
    "name": "Test User",
    "photo_url": "https://example.com/photo.jpg",
    "email_verified": false
}
```

### 6. Update User Profile
```http
PUT /user/profile/
```
**Headers**: Authorization Bearer Token
**Body**:
```json
{
    "display_name": "Updated Name",
    "photo_url": "https://example.com/photo.jpg"
}
```
**Response**:
```json
{
    "message": "Profile updated successfully",
    "user_id": "uid123",
    "email": "test@example.com",
    "name": "Updated Name",
    "photo_url": "https://example.com/photo.jpg"
}
```

### 7. Save Emotion
```http
POST /api/emotions
```
**Headers**: Authorization Bearer Token
**Body**:
```json
{
    "emotion": "happy",
    "intensity": 8,
    "note": "Had a great day!"
}
```
**Response** (201 Created):
```json
{
    "message": "Emotion saved successfully",
    "data": {
        "emotion": "happy",
        "intensity": 8,
        "note": "Had a great day!",
        "timestamp": "2025-06-03T10:30:45.123456",
        "user_id": "uid123"
    }
}
```

### 8. Get Emotion History
```http
GET /api/emotions/history?period={week|month|year}
```
**Headers**: Authorization Bearer Token
**Query Parameters**:
- `period`: week (default) | month | year

**Response**:
```json
{
    "period": "week",
    "start_date": "2025-05-27T00:00:00",
    "end_date": "2025-06-03T23:59:59",
    "emotions": [
        {
            "id": "-ORpvFDECk32tdzQDzcq",
            "emotion": "happy",
            "intensity": 8,
            "note": "Test note",
            "timestamp": "2025-06-03T10:30:45.123456"
        }
    ],
    "statistics": {
        "total_entries": 1,
        "emotion_frequency": {
            "happy": 1
        },
        "average_intensity": 8.0
    }
}
```

### 9. Get Emotion Analysis
```http
GET /api/emotions/analysis
```
**Headers**: Authorization Bearer Token
**Response**:
```json
{
    "weekly_data": [
        {
            "id": "-ORpvFDECk32tdzQDzcq",
            "emotion": "happy",
            "intensity": 8,
            "note": "Test note",
            "timestamp": "2025-06-03T10:30:45.123456",
            "day": "Tuesday"
        }
    ],
    "analysis": {
        "total_entries": 1,
        "date_range": {
            "start": "2025-05-27T00:00:00",
            "end": "2025-06-03T23:59:59"
        },
        "dominant_emotion": "happy",
        "average_intensity": 8.0,
        "daily_mood_pattern": {
            "Tuesday": 8.0
        },
        "emotion_distribution": {
            "happy": {
                "frequency": 1,
                "average_intensity": 8.0,
                "percentage": 100.0
            }
        },
        "mood_swings": false,
        "recommendations": [
            "Keep up the positive activities",
            "Share your joy with others"
        ]
    }
}
```

## Error Responses
All endpoints return error responses in this format:
```json
{
    "error": "Error message description"
}
```

## Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Server Error

## Rate Limiting
- Maximum 100 requests per minute per IP
- Maximum 1000 requests per hour per user

## Security Recommendations
1. Always use HTTPS
2. Keep tokens secure
3. Never share credentials
4. Implement token refresh mechanism
5. Log out when finished

## Support
For API support, contact: support@moodmate.com