# 🔧 ViralCast - Technical Implementation Guide

## 📋 **OVERVIEW**

This document provides complete technical specifications for building the ViralCast YouTube prediction website. It includes backend API design, frontend architecture, database schema, and deployment requirements.

---

## 🏗️ **SYSTEM ARCHITECTURE**

### **High-Level Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   ML Models     │
│   (React.js)    │◄──►│   (FastAPI)     │◄──►│   (Python)      │
│   Port: 3000    │    │   Port: 8000    │    │   Local Files   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Static Files  │    │   Database      │    │   File Storage  │
│   (Nginx)       │    │   (PostgreSQL)  │    │   (Models)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Technology Stack**
- **Frontend**: React.js 18+ with TypeScript
- **Backend**: FastAPI with Python 3.8+
- **Database**: PostgreSQL 13+
- **ML Models**: scikit-learn, XGBoost, LightGBM
- **Caching**: Redis (optional)
- **Deployment**: Docker + Nginx

---

## 🔧 **BACKEND SPECIFICATIONS**

### **FastAPI Application Structure**
```
backend/
├── main.py                 # FastAPI app entry point
├── models/
│   ├── __init__.py
│   ├── prediction.py       # ML model integration
│   ├── database.py         # Database models
│   └── schemas.py          # Pydantic schemas
├── api/
│   ├── __init__.py
│   ├── predictions.py      # Prediction endpoints
│   ├── analytics.py        # Analytics endpoints
│   └── health.py           # Health check endpoints
├── core/
│   ├── __init__.py
│   ├── config.py           # Configuration settings
│   └── security.py         # Authentication/security
├── utils/
│   ├── __init__.py
│   ├── feature_engineering.py  # Feature processing
│   └── validation.py       # Input validation
├── requirements.txt        # Python dependencies
└── Dockerfile             # Docker configuration
```

### **API Endpoints Specification**

#### **1. Prediction Endpoints**
```python
# POST /api/v1/predict
{
    "title": "string (required, max 200 chars)",
    "description": "string (optional, max 5000 chars)",
    "duration": "integer (required, 1-7200 seconds)",
    "like_count": "integer (optional, >= 0)",
    "dislike_count": "integer (optional, >= 0)",
    "comment_count": "integer (optional, >= 0)",
    "upload_date": "string (required, ISO 8601 format)",
    "upload_time": "string (optional, HH:MM format)",
    "tags": "string (optional, comma-separated)",
    "category": "string (optional, predefined list)"
}

# Response
{
    "prediction_id": "uuid",
    "predicted_views": "integer",
    "confidence_lower": "integer",
    "confidence_upper": "integer",
    "confidence_range": "string",
    "prediction_quality": "string (High/Medium/Low)",
    "expected_performance": "string",
    "key_factors": ["string"],
    "recommendations": ["string"],
    "processing_time": "float (seconds)",
    "timestamp": "ISO 8601"
}
```

#### **2. Batch Prediction Endpoints**
```python
# POST /api/v1/predict/batch
{
    "videos": [
        {
            "video_id": "string (optional)",
            "title": "string",
            "description": "string",
            "duration": "integer",
            # ... other fields
        }
    ]
}

# Response
{
    "batch_id": "uuid",
    "total_videos": "integer",
    "predictions": [
        {
            "video_id": "string",
            "predicted_views": "integer",
            "confidence_range": "string",
            # ... other fields
        }
    ],
    "processing_time": "float",
    "timestamp": "ISO 8601"
}
```

#### **3. Analytics Endpoints**
```python
# GET /api/v1/analytics/trends
# Query Parameters: category, time_range, limit
# Response: Trending topics and performance metrics

# GET /api/v1/analytics/categories
# Response: Category performance statistics

# POST /api/v1/analytics/save
# Save user prediction results for analytics
```

#### **4. Health Check Endpoints**
```python
# GET /api/v1/health
{
    "status": "healthy",
    "timestamp": "ISO 8601",
    "version": "1.0.0",
    "models_loaded": "boolean",
    "database_connected": "boolean"
}
```

### **Database Schema**

#### **Users Table**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

#### **Predictions Table**
```sql
CREATE TABLE predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    video_title VARCHAR(500) NOT NULL,
    video_description TEXT,
    duration INTEGER NOT NULL,
    like_count INTEGER DEFAULT 0,
    dislike_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    upload_date DATE NOT NULL,
    upload_time TIME,
    tags TEXT,
    category VARCHAR(100),
    predicted_views INTEGER NOT NULL,
    confidence_lower INTEGER NOT NULL,
    confidence_upper INTEGER NOT NULL,
    prediction_quality VARCHAR(20) NOT NULL,
    actual_views INTEGER,
    accuracy_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Analytics Table**
```sql
CREATE TABLE analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prediction_id UUID REFERENCES predictions(id),
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **ML Model Integration**

#### **Model Loading**
```python
import joblib
import numpy as np
import pandas as pd

class PredictionModel:
    def __init__(self):
        self.model = joblib.load('models/gradient_boosting_model.pkl')
        self.scaler = joblib.load('models/main_scaler.pkl')
        self.category_encoder = joblib.load('models/category_label_encoder.pkl')
        self.model_info = joblib.load('models/optimal_model_info.pkl')
    
    def predict(self, features):
        # Scale features
        scaled_features = self.scaler.transform(features)
        
        # Make prediction (log scale)
        log_prediction = self.model.predict(scaled_features)[0]
        
        # Convert to original scale
        prediction = np.expm1(log_prediction)
        
        return int(prediction)
```

#### **Feature Engineering**
```python
def process_video_features(video_data):
    features = {
        'duration': video_data['duration'],
        'duration_minutes': video_data['duration'] / 60,
        'log_duration': np.log1p(video_data['duration']),
        'like_count': video_data.get('like_count', 0),
        'dislike_count': video_data.get('dislike_count', 0),
        'like_ratio': calculate_like_ratio(video_data),
        'engagement_rate': calculate_engagement_rate(video_data),
        'title_length': len(video_data['title']),
        'description_length': len(video_data.get('description', '')),
        'tags_count': len(video_data.get('tags', '').split(',')),
        'title_word_count': len(video_data['title'].split()),
        'upload_hour': extract_hour(video_data['upload_date']),
        'upload_day_of_week': extract_day_of_week(video_data['upload_date']),
        'upload_month': extract_month(video_data['upload_date']),
        'is_weekend': is_weekend(video_data['upload_date']),
        'days_since_upload': calculate_days_since_upload(video_data['upload_date']),
        'log_days_since_upload': np.log1p(calculate_days_since_upload(video_data['upload_date']))
    }
    
    # Add cyclical encoding
    features.update(create_cyclical_features(video_data['upload_date']))
    
    return features
```

---

## 🎨 **FRONTEND SPECIFICATIONS**

### **React Application Structure**
```
frontend/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Navigation.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   ├── prediction/
│   │   │   ├── PredictionForm.tsx
│   │   │   ├── PredictionResults.tsx
│   │   │   └── PredictionHistory.tsx
│   │   ├── analytics/
│   │   │   ├── AnalyticsDashboard.tsx
│   │   │   ├── PerformanceChart.tsx
│   │   │   └── CategoryAnalysis.tsx
│   │   └── layout/
│   │       ├── MainLayout.tsx
│   │       └── Sidebar.tsx
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── PredictionPage.tsx
│   │   ├── AnalyticsPage.tsx
│   │   └── AboutPage.tsx
│   ├── services/
│   │   ├── api.ts
│   │   ├── predictionService.ts
│   │   └── analyticsService.ts
│   ├── hooks/
│   │   ├── usePrediction.ts
│   │   ├── useAnalytics.ts
│   │   └── useAuth.ts
│   ├── utils/
│   │   ├── validation.ts
│   │   ├── formatting.ts
│   │   └── constants.ts
│   ├── types/
│   │   ├── prediction.ts
│   │   ├── analytics.ts
│   │   └── user.ts
│   ├── styles/
│   │   ├── globals.css
│   │   ├── components.css
│   │   └── variables.css
│   ├── App.tsx
│   └── index.tsx
├── package.json
├── tsconfig.json
└── tailwind.config.js
```

### **Component Specifications**

#### **1. PredictionForm Component**
```typescript
interface PredictionFormProps {
  onSubmit: (data: PredictionInput) => void;
  loading: boolean;
  initialData?: Partial<PredictionInput>;
}

interface PredictionInput {
  title: string;
  description: string;
  duration: number;
  like_count: number;
  dislike_count: number;
  comment_count: number;
  upload_date: string;
  upload_time: string;
  tags: string;
  category: string;
}
```

#### **2. PredictionResults Component**
```typescript
interface PredictionResultsProps {
  prediction: PredictionResult;
  onPredictAnother: () => void;
  onSaveResult: () => void;
}

interface PredictionResult {
  prediction_id: string;
  predicted_views: number;
  confidence_lower: number;
  confidence_upper: number;
  confidence_range: string;
  prediction_quality: 'High' | 'Medium' | 'Low';
  expected_performance: string;
  key_factors: string[];
  recommendations: string[];
  processing_time: number;
  timestamp: string;
}
```

#### **3. AnalyticsDashboard Component**
```typescript
interface AnalyticsDashboardProps {
  userId: string;
  timeRange: '7d' | '30d' | '90d' | '1y';
}

interface AnalyticsData {
  total_predictions: number;
  average_accuracy: number;
  best_performing_category: string;
  prediction_trends: TrendData[];
  category_performance: CategoryData[];
}
```

### **State Management**
```typescript
// Redux Store Structure
interface RootState {
  auth: AuthState;
  prediction: PredictionState;
  analytics: AnalyticsState;
  ui: UIState;
}

interface PredictionState {
  currentPrediction: PredictionResult | null;
  predictionHistory: PredictionResult[];
  loading: boolean;
  error: string | null;
}

interface AnalyticsState {
  dashboardData: AnalyticsData | null;
  trends: TrendData[];
  loading: boolean;
  error: string | null;
}
```

### **API Service Layer**
```typescript
class PredictionService {
  private baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  
  async predictVideo(data: PredictionInput): Promise<PredictionResult> {
    const response = await fetch(`${this.baseURL}/api/v1/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.getToken()}`
      },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      throw new Error('Prediction failed');
    }
    
    return response.json();
  }
  
  async getPredictionHistory(): Promise<PredictionResult[]> {
    // Implementation
  }
  
  async getBatchPredictions(videos: PredictionInput[]): Promise<PredictionResult[]> {
    // Implementation
  }
}
```

---

## 🗄️ **DATABASE SPECIFICATIONS**

### **PostgreSQL Configuration**
```sql
-- Database setup
CREATE DATABASE viralcast;
CREATE USER viralcast_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE viralcast TO viralcast_user;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create indexes for performance
CREATE INDEX idx_predictions_user_id ON predictions(user_id);
CREATE INDEX idx_predictions_created_at ON predictions(created_at);
CREATE INDEX idx_predictions_category ON predictions(category);
CREATE INDEX idx_analytics_prediction_id ON analytics(prediction_id);
```

### **Database Connection**
```python
# Database configuration
DATABASE_URL = "postgresql://viralcast_user:secure_password@localhost:5432/viralcast"

# SQLAlchemy setup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

---

## 🚀 **DEPLOYMENT SPECIFICATIONS**

### **Docker Configuration**

#### **Backend Dockerfile**
```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **Frontend Dockerfile**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

#### **Docker Compose**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://viralcast_user:password@db:5432/viralcast
    depends_on:
      - db
    volumes:
      - ./models:/app/models

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=viralcast
      - POSTGRES_USER=viralcast_user
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### **Environment Variables**
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:password@localhost:5432/viralcast
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
MODEL_PATH=./models/
LOG_LEVEL=INFO

# Frontend (.env)
REACT_APP_API_URL=http://localhost:8000
REACT_APP_VERSION=1.0.0
```

---

## 🔒 **SECURITY SPECIFICATIONS**

### **Authentication**
```python
# JWT Token implementation
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### **Input Validation**
```python
from pydantic import BaseModel, validator

class PredictionInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    duration: int = Field(..., ge=1, le=7200)
    like_count: int = Field(0, ge=0)
    dislike_count: int = Field(0, ge=0)
    upload_date: str = Field(..., regex=r'^\d{4}-\d{2}-\d{2}$')
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
```

### **Rate Limiting**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/predict")
@limiter.limit("10/minute")
async def predict_video(request: Request, data: PredictionInput):
    # Implementation
```

---

## 📊 **MONITORING & LOGGING**

### **Logging Configuration**
```python
import logging
from pythonjsonlogger import jsonlogger

# Setup structured logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Log prediction requests
logger.info("Prediction request", extra={
    "user_id": user_id,
    "video_title": data.title,
    "predicted_views": prediction,
    "processing_time": processing_time
})
```

### **Health Monitoring**
```python
@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "models_loaded": check_models_loaded(),
        "database_connected": check_database_connection(),
        "memory_usage": get_memory_usage(),
        "cpu_usage": get_cpu_usage()
    }
```

---

## 🧪 **TESTING SPECIFICATIONS**

### **Backend Tests**
```python
# test_prediction.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_predict_video():
    response = client.post("/api/v1/predict", json={
        "title": "Test Video",
        "duration": 300,
        "upload_date": "2024-01-15"
    })
    assert response.status_code == 200
    assert "predicted_views" in response.json()
```

### **Frontend Tests**
```typescript
// PredictionForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { PredictionForm } from './PredictionForm';

test('submits form with valid data', () => {
  const mockSubmit = jest.fn();
  render(<PredictionForm onSubmit={mockSubmit} loading={false} />);
  
  fireEvent.change(screen.getByLabelText(/video title/i), {
    target: { value: 'Test Video' }
  });
  fireEvent.change(screen.getByLabelText(/duration/i), {
    target: { value: '300' }
  });
  fireEvent.click(screen.getByText(/predict views/i));
  
  expect(mockSubmit).toHaveBeenCalledWith({
    title: 'Test Video',
    duration: 300,
    // ... other fields
  });
});
```

---

## 📈 **PERFORMANCE SPECIFICATIONS**

### **Response Time Targets**
- **Single Prediction**: < 200ms
- **Batch Prediction**: < 1s per 100 videos
- **Page Load**: < 2s
- **API Health Check**: < 50ms

### **Scalability Requirements**
- **Concurrent Users**: 1000+
- **Requests per Minute**: 10,000+
- **Database Connections**: 100+
- **Memory Usage**: < 2GB per instance

### **Caching Strategy**
```python
# Redis caching for predictions
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_prediction(expiry=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"prediction:{hash(str(args) + str(kwargs))}"
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, expiry, json.dumps(result))
            return result
        return wrapper
    return decorator
```

---

This comprehensive technical specification provides everything needed to build a production-ready YouTube prediction website. The developer has complete API specifications, database schemas, frontend architecture, and deployment requirements.

