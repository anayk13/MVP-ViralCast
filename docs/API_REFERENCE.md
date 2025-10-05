# 🔌 ViralCast API Reference

## 📋 **OVERVIEW**

Complete API documentation for the ViralCast YouTube prediction service. This reference covers all endpoints, request/response formats, error handling, and integration examples.

---

## 🌐 **BASE URL**

```
Development: http://localhost:8000
Production: https://api.viralcast.com
```

---

## 🔐 **AUTHENTICATION**

### **API Key Authentication**
```http
Authorization: Bearer <your-api-key>
```

### **Getting an API Key**
1. Register at `/api/v1/auth/register`
2. Login at `/api/v1/auth/login`
3. Get API key from response

---

## 📊 **PREDICTION ENDPOINTS**

### **1. Single Video Prediction**

#### **POST** `/api/v1/predict`

Predict view count for a single YouTube video.

**Request Body:**
```json
{
  "title": "How to Build a Machine Learning Model in Python",
  "description": "Complete tutorial covering data preprocessing, model training, and deployment",
  "duration": 900,
  "like_count": 1250,
  "dislike_count": 45,
  "comment_count": 89,
  "upload_date": "2024-01-15",
  "upload_time": "14:30",
  "tags": "python, machine learning, tutorial, coding",
  "category": "Education"
}
```

**Response:**
```json
{
  "prediction_id": "550e8400-e29b-41d4-a716-446655440000",
  "predicted_views": 831910,
  "confidence_lower": 582337,
  "confidence_upper": 1081483,
  "confidence_range": "582,337 - 1,081,483",
  "prediction_quality": "High",
  "expected_performance": "Strong performance - Expected to perform well",
  "key_factors": [
    "High engagement potential (8.2% engagement rate)",
    "Educational content (good for long-term views)",
    "Optimal duration for tutorial content (15 minutes)",
    "Strong title with clear value proposition"
  ],
  "recommendations": [
    "Add timestamps in description for better navigation",
    "Include code repository link in description",
    "Consider adding chapter markers in video",
    "Add more specific tags: 'scikit-learn', 'pandas', 'numpy'"
  ],
  "processing_time": 0.156,
  "timestamp": "2024-01-15T14:30:45.123Z"
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad Request (validation error)
- `401` - Unauthorized
- `429` - Rate limit exceeded
- `500` - Internal server error

---

### **2. Batch Video Prediction**

#### **POST** `/api/v1/predict/batch`

Predict view counts for multiple videos in a single request.

**Request Body:**
```json
{
  "videos": [
    {
      "video_id": "video_1",
      "title": "Python Tutorial for Beginners",
      "duration": 600,
      "upload_date": "2024-01-15",
      "category": "Education"
    },
    {
      "video_id": "video_2", 
      "title": "Machine Learning Explained",
      "duration": 1200,
      "upload_date": "2024-01-16",
      "category": "Education"
    }
  ]
}
```

**Response:**
```json
{
  "batch_id": "batch_550e8400-e29b-41d4-a716-446655440000",
  "total_videos": 2,
  "predictions": [
    {
      "video_id": "video_1",
      "predicted_views": 245000,
      "confidence_range": "171,500 - 318,500",
      "prediction_quality": "High",
      "expected_performance": "Good performance expected",
      "key_factors": ["Educational content", "Optimal duration"],
      "recommendations": ["Add more specific tags"]
    },
    {
      "video_id": "video_2",
      "predicted_views": 567000,
      "confidence_range": "396,900 - 617,100",
      "prediction_quality": "High", 
      "expected_performance": "Strong performance expected",
      "key_factors": ["Educational content", "Good duration"],
      "recommendations": ["Include practical examples"]
    }
  ],
  "processing_time": 0.234,
  "timestamp": "2024-01-15T14:30:45.123Z"
}
```

---

### **3. Prediction History**

#### **GET** `/api/v1/predictions`

Get user's prediction history with pagination.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20, max: 100)
- `category` (optional): Filter by category
- `date_from` (optional): Start date (YYYY-MM-DD)
- `date_to` (optional): End date (YYYY-MM-DD)

**Response:**
```json
{
  "predictions": [
    {
      "prediction_id": "550e8400-e29b-41d4-a716-446655440000",
      "video_title": "Python Tutorial for Beginners",
      "predicted_views": 245000,
      "actual_views": 267000,
      "accuracy_score": 0.92,
      "prediction_quality": "High",
      "created_at": "2024-01-15T14:30:45.123Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

---

## 📈 **ANALYTICS ENDPOINTS**

### **1. Dashboard Analytics**

#### **GET** `/api/v1/analytics/dashboard`

Get comprehensive analytics for user dashboard.

**Query Parameters:**
- `time_range` (optional): 7d, 30d, 90d, 1y (default: 30d)

**Response:**
```json
{
  "summary": {
    "total_predictions": 150,
    "average_accuracy": 0.89,
    "best_performing_category": "Education",
    "total_predicted_views": 12500000,
    "average_predicted_views": 83333
  },
  "trends": {
    "daily_predictions": [
      {"date": "2024-01-15", "count": 5},
      {"date": "2024-01-16", "count": 8}
    ],
    "accuracy_trend": [
      {"date": "2024-01-15", "accuracy": 0.92},
      {"date": "2024-01-16", "accuracy": 0.88}
    ]
  },
  "category_performance": [
    {
      "category": "Education",
      "predictions": 45,
      "average_accuracy": 0.94,
      "average_views": 125000
    },
    {
      "category": "Technology", 
      "predictions": 32,
      "average_accuracy": 0.87,
      "average_views": 89000
    }
  ]
}
```

### **2. Category Trends**

#### **GET** `/api/v1/analytics/categories`

Get trending categories and performance metrics.

**Response:**
```json
{
  "categories": [
    {
      "name": "Education",
      "trend_score": 0.95,
      "average_views": 125000,
      "prediction_count": 45,
      "growth_rate": 0.12
    },
    {
      "name": "Technology",
      "trend_score": 0.87,
      "average_views": 89000,
      "prediction_count": 32,
      "growth_rate": 0.08
    }
  ],
  "trending_keywords": [
    "machine learning",
    "python tutorial",
    "data science",
    "AI explained"
  ]
}
```

### **3. Save Prediction Result**

#### **POST** `/api/v1/analytics/save`

Save prediction result for analytics tracking.

**Request Body:**
```json
{
  "prediction_id": "550e8400-e29b-41d4-a716-446655440000",
  "actual_views": 267000,
  "feedback": "prediction_accurate"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Prediction result saved successfully",
  "updated_accuracy": 0.92
}
```

---

## 🔍 **MODEL ENDPOINTS**

### **1. Model Information**

#### **GET** `/api/v1/models/info`

Get information about loaded ML models.

**Response:**
```json
{
  "models": [
    {
      "name": "gradient_boosting",
      "version": "1.0.0",
      "accuracy": 0.9734,
      "last_trained": "2024-01-10T10:30:00Z",
      "status": "active"
    }
  ],
  "feature_count": 21,
  "training_samples": 49939,
  "model_size": "15.2MB"
}
```

### **2. Model Health Check**

#### **GET** `/api/v1/models/health`

Check if ML models are loaded and functioning.

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": true,
  "prediction_available": true,
  "last_model_check": "2024-01-15T14:30:45.123Z"
}
```

---

## 🏥 **HEALTH & MONITORING**

### **1. System Health**

#### **GET** `/api/v1/health`

Get overall system health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T14:30:45.123Z",
  "version": "1.0.0",
  "uptime": 86400,
  "components": {
    "database": "healthy",
    "models": "healthy",
    "cache": "healthy"
  },
  "metrics": {
    "memory_usage": "45%",
    "cpu_usage": "23%",
    "active_connections": 15
  }
}
```

### **2. Detailed Health Check**

#### **GET** `/api/v1/health/detailed`

Get detailed system health information.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T14:30:45.123Z",
  "database": {
    "status": "connected",
    "response_time": 12,
    "active_connections": 15,
    "max_connections": 100
  },
  "models": {
    "gradient_boosting": {
      "status": "loaded",
      "memory_usage": "15.2MB",
      "last_prediction": "2024-01-15T14:29:30Z"
    }
  },
  "cache": {
    "status": "connected",
    "hit_rate": 0.85,
    "memory_usage": "128MB"
  }
}
```

---

## 🔐 **AUTHENTICATION ENDPOINTS**

### **1. User Registration**

#### **POST** `/api/v1/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "creator123",
  "password": "secure_password123"
}
```

**Response:**
```json
{
  "user_id": "user_550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "creator123",
  "api_key": "ak_550e8400e29b41d4a716446655440000",
  "created_at": "2024-01-15T14:30:45.123Z"
}
```

### **2. User Login**

#### **POST** `/api/v1/auth/login`

Authenticate user and get API key.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password123"
}
```

**Response:**
```json
{
  "user_id": "user_550e8400-e29b-41d4-a716-446655440000",
  "api_key": "ak_550e8400e29b41d4a716446655440000",
  "expires_at": "2024-02-15T14:30:45.123Z"
}
```

---

## ❌ **ERROR HANDLING**

### **Error Response Format**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "duration",
      "issue": "Duration must be between 1 and 7200 seconds"
    },
    "timestamp": "2024-01-15T14:30:45.123Z",
    "request_id": "req_550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### **Common Error Codes**

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Input validation failed |
| `UNAUTHORIZED` | 401 | Invalid or missing API key |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `MODEL_ERROR` | 500 | ML model prediction failed |
| `DATABASE_ERROR` | 500 | Database connection issue |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

---

## 📝 **REQUEST VALIDATION**

### **Required Fields**
- `title`: Video title (1-200 characters)
- `duration`: Video duration in seconds (1-7200)
- `upload_date`: Upload date (YYYY-MM-DD format)

### **Optional Fields**
- `description`: Video description (max 5000 characters)
- `like_count`: Number of likes (≥ 0)
- `dislike_count`: Number of dislikes (≥ 0)
- `comment_count`: Number of comments (≥ 0)
- `upload_time`: Upload time (HH:MM format)
- `tags`: Comma-separated tags
- `category`: Video category (predefined list)

### **Validation Rules**
```json
{
  "title": {
    "required": true,
    "min_length": 1,
    "max_length": 200,
    "pattern": "^[\\s\\S]*[^\\s][\\s\\S]*$"
  },
  "duration": {
    "required": true,
    "type": "integer",
    "minimum": 1,
    "maximum": 7200
  },
  "upload_date": {
    "required": true,
    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
  },
  "like_count": {
    "type": "integer",
    "minimum": 0
  },
  "description": {
    "max_length": 5000
  }
}
```

---

## 🚀 **INTEGRATION EXAMPLES**

### **JavaScript/Node.js**
```javascript
const axios = require('axios');

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Authorization': 'Bearer your-api-key',
    'Content-Type': 'application/json'
  }
});

async function predictVideo(videoData) {
  try {
    const response = await api.post('/api/v1/predict', videoData);
    return response.data;
  } catch (error) {
    console.error('Prediction failed:', error.response.data);
    throw error;
  }
}

// Usage
const prediction = await predictVideo({
  title: "My Awesome Video",
  duration: 300,
  upload_date: "2024-01-15"
});
```

### **Python**
```python
import requests

class ViralCastAPI:
    def __init__(self, api_key, base_url="http://localhost:8000"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def predict_video(self, video_data):
        response = requests.post(
            f"{self.base_url}/api/v1/predict",
            json=video_data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

# Usage
api = ViralCastAPI("your-api-key")
prediction = api.predict_video({
    "title": "My Awesome Video",
    "duration": 300,
    "upload_date": "2024-01-15"
})
```

### **cURL**
```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Awesome Video",
    "duration": 300,
    "upload_date": "2024-01-15"
  }'
```

---

## 📊 **RATE LIMITING**

### **Rate Limits**
- **Free Tier**: 100 requests/hour
- **Pro Tier**: 1000 requests/hour
- **Enterprise**: 10000 requests/hour

### **Rate Limit Headers**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642252800
```

### **Rate Limit Exceeded Response**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again later.",
    "retry_after": 3600
  }
}
```

---

## 🔄 **WEBHOOKS**

### **Prediction Completed Webhook**
```json
{
  "event": "prediction.completed",
  "data": {
    "prediction_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user_123",
    "predicted_views": 831910,
    "prediction_quality": "High",
    "processing_time": 0.156
  },
  "timestamp": "2024-01-15T14:30:45.123Z"
}
```

### **Webhook Configuration**
- **URL**: Your webhook endpoint
- **Events**: `prediction.completed`, `batch.completed`
- **Retry Policy**: 3 attempts with exponential backoff
- **Timeout**: 30 seconds

---

This comprehensive API reference provides everything needed to integrate with the ViralCast prediction service. All endpoints are documented with examples, error handling, and integration code.
