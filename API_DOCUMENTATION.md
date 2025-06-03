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

### 10. Get Emotion Regression Analysis
```http
GET /api/emotions/regression
```
**Headers**: Authorization Bearer Token
**Response**:
```json
{
    "period": {
        "start": "2025-05-27T00:00:00",
        "end": "2025-06-03T23:59:59"
    },
    "regression_analysis": {
        "trend": "improving",
        "trend_strength": 0.15,
        "r_squared": 0.75,
        "prediction_next_24h": 7.2,
        "confidence_score": 75.0,
        "data_points": {
            "timestamps": [0, 24, 48, 72, 96, 120, 144],
            "intensities": [5, 6, 6, 7, 7, 8, 8],
            "predicted_values": [5.2, 5.8, 6.4, 7.0, 7.6, 8.2, 8.8]
        },
        "statistics": {
            "mean_intensity": 6.71,
            "std_intensity": 1.11,
            "slope": 0.025,
            "intercept": 5.1
        },
        "recommendations": [
            "Your mood is showing positive improvement!",
            "Keep track of activities that might be contributing to this upward trend."
        ]
    }
}
```

### Enhanced Mood Recommendations
The API now provides more detailed recommendations based on:
- Emotion type (happy, sad, angry, anxious)
- Intensity levels (high, medium, low)
- Chatbot interaction suggestions

Example response structure in emotion analysis:
```json
{
    "recommendations": {
        "actions": [
            "Share your joy with friends or family",
            "Document what made you happy today",
            "Express gratitude through journaling"
        ],
        "chatbot_suggestion": "I'm so glad you're feeling happy! Would you like to share what made your day special?",
        "intensity_specific": [
            "Channel your positive energy into a creative project",
            "Consider mentoring or helping others",
            "Start a gratitude journal"
        ]
    }
}
```

## Mood Categories
The API supports these primary mood categories with specialized recommendations:

### Happy
- High Intensity (8-10): Focus on sharing and creative activities
- Medium Intensity (5-7): Social engagement and memory creation
- Low Intensity (1-4): Mood maintenance and light activities

### Sad
- High Intensity (8-10): Professional support and grounding techniques
- Medium Intensity (5-7): Self-care and gentle activities
- Low Intensity (1-4): Comfort activities and mild mood elevation

### Angry
- High Intensity (8-10): Immediate cooling down techniques
- Medium Intensity (5-7): Physical activities and expression
- Low Intensity (1-4): Simple calming techniques

### Anxious
- High Intensity (8-10): Structured coping techniques
- Medium Intensity (5-7): Mindfulness and physical activity
- Low Intensity (1-4): Gentle relaxation methods

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