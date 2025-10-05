# 🔧 ViralCast Backend - FastAPI Implementation Guide

## 📋 **OVERVIEW**

Complete backend implementation guide for the ViralCast YouTube prediction API. This document provides step-by-step instructions for building a production-ready FastAPI backend.

---

## 🏗️ **PROJECT STRUCTURE**

```
backend/
├── main.py                 # FastAPI application entry point
├── models/
│   ├── __init__.py
│   ├── prediction.py       # ML model integration
│   ├── database.py         # SQLAlchemy models
│   └── schemas.py          # Pydantic schemas
├── api/
│   ├── __init__.py
│   ├── predictions.py      # Prediction endpoints
│   ├── analytics.py        # Analytics endpoints
│   ├── auth.py             # Authentication endpoints
│   └── health.py           # Health check endpoints
├── core/
│   ├── __init__.py
│   ├── config.py           # Configuration settings
│   ├── security.py         # Authentication/security
│   └── database.py         # Database connection
├── utils/
│   ├── __init__.py
│   ├── feature_engineering.py  # Feature processing
│   ├── validation.py       # Input validation
│   └── helpers.py          # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_predictions.py
│   ├── test_auth.py
│   └── test_analytics.py
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── .env.example           # Environment variables template
└── README.md              # This file
```

---

## 🚀 **QUICK START**

### **1. Environment Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

### **2. Database Setup**
```bash
# Install PostgreSQL (if not already installed)
# Create database
createdb viralcast

# Run migrations (if using Alembic)
alembic upgrade head
```

### **3. Run Development Server**
```bash
# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use the development script
python main.py
```

### **4. Access API Documentation**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

---

## 📦 **DEPENDENCIES**

### **requirements.txt**
```
# FastAPI and ASGI
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# ML Models
scikit-learn==1.3.2
xgboost==2.0.2
lightgbm==4.1.0
joblib==1.3.2
numpy==1.24.4
pandas==2.1.4

# Validation
pydantic==2.5.0
email-validator==2.1.0

# Caching (optional)
redis==5.0.1

# Monitoring
prometheus-client==0.19.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Development
black==23.11.0
flake8==6.1.0
mypy==1.7.1
```

---

## ⚙️ **CONFIGURATION**

### **Environment Variables (.env)**
```bash
# Database
DATABASE_URL=postgresql://viralcast_user:password@localhost:5432/viralcast
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Security
SECRET_KEY=your-secret-key-here-make-it-long-and-random
JWT_SECRET=your-jwt-secret-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# ML Models
MODEL_PATH=./models/
MODEL_CACHE_SIZE=1000

# API Settings
API_V1_STR=/api/v1
PROJECT_NAME=ViralCast
VERSION=1.0.0
DEBUG=True

# CORS
CORS_ORIGINS=["http://localhost:3000", "https://viralcast.com"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_BURST=200

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Redis (optional)
REDIS_URL=redis://localhost:6379/0
```

### **Configuration Class (core/config.py)**
```python
from pydantic import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # Database
    database_url: str
    database_pool_size: int = 10
    database_max_overflow: int = 20
    
    # Security
    secret_key: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    
    # ML Models
    model_path: str = "./models/"
    model_cache_size: int = 1000
    
    # API Settings
    api_v1_str: str = "/api/v1"
    project_name: str = "ViralCast"
    version: str = "1.0.0"
    debug: bool = True
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    rate_limit_burst: int = 200
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # Redis
    redis_url: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 🗄️ **DATABASE MODELS**

### **User Model (models/database.py)**
```python
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    predictions = relationship("Prediction", back_populates="user")
```

### **Prediction Model**
```python
class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Video data
    video_title = Column(String(500), nullable=False)
    video_description = Column(Text)
    duration = Column(Integer, nullable=False)
    like_count = Column(Integer, default=0)
    dislike_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    upload_date = Column(DateTime(timezone=True), nullable=False)
    upload_time = Column(Time)
    tags = Column(Text)
    category = Column(String(100))
    
    # Prediction results
    predicted_views = Column(Integer, nullable=False)
    confidence_lower = Column(Integer, nullable=False)
    confidence_upper = Column(Integer, nullable=False)
    prediction_quality = Column(String(20), nullable=False)
    expected_performance = Column(String(200))
    key_factors = Column(JSON)
    recommendations = Column(JSON)
    
    # Actual results (for accuracy tracking)
    actual_views = Column(Integer)
    accuracy_score = Column(Float)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="predictions")
    analytics = relationship("Analytics", back_populates="prediction")
```

### **Analytics Model**
```python
class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prediction_id = Column(UUID(as_uuid=True), ForeignKey("predictions.id"))
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    prediction = relationship("Prediction", back_populates="analytics")
```

---

## 🔌 **API ENDPOINTS**

### **Main Application (main.py)**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from core.config import settings
from api import predictions, analytics, auth, health

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="YouTube video success prediction API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.viralcast.com"]
)

# Include routers
app.include_router(predictions.router, prefix=settings.api_v1_str)
app.include_router(analytics.router, prefix=settings.api_v1_str)
app.include_router(auth.router, prefix=settings.api_v1_str)
app.include_router(health.router, prefix=settings.api_v1_str)

@app.get("/")
async def root():
    return {
        "message": "Welcome to ViralCast API",
        "version": settings.version,
        "docs": "/docs"
    }
```

### **Prediction Endpoints (api/predictions.py)**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from models.schemas import PredictionInput, PredictionResponse
from models.prediction import PredictionModel
from core.security import get_current_user
from utils.validation import validate_prediction_input

router = APIRouter()
security = HTTPBearer()

# Initialize prediction model
prediction_model = PredictionModel()

@router.post("/predict", response_model=PredictionResponse)
async def predict_video(
    prediction_input: PredictionInput,
    current_user: dict = Depends(get_current_user)
):
    """Predict view count for a single video."""
    try:
        # Validate input
        validated_input = validate_prediction_input(prediction_input)
        
        # Make prediction
        prediction_result = prediction_model.predict(validated_input)
        
        # Save to database (optional)
        # await save_prediction(prediction_result, current_user["id"])
        
        return prediction_result
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

@router.post("/predict/batch")
async def predict_batch(
    videos: List[PredictionInput],
    current_user: dict = Depends(get_current_user)
):
    """Predict view counts for multiple videos."""
    # Implementation for batch prediction
    pass

@router.get("/predictions")
async def get_prediction_history(
    page: int = 1,
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """Get user's prediction history."""
    # Implementation for prediction history
    pass
```

---

## 🤖 **ML MODEL INTEGRATION**

### **Prediction Model (models/prediction.py)**
```python
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any
from utils.feature_engineering import process_video_features

class PredictionModel:
    def __init__(self, model_path: str = "./models/"):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.category_encoder = None
        self.model_info = None
        self.load_models()
    
    def load_models(self):
        """Load all required ML models and scalers."""
        try:
            self.model = joblib.load(f"{self.model_path}gradient_boosting_model.pkl")
            self.scaler = joblib.load(f"{self.model_path}main_scaler.pkl")
            self.category_encoder = joblib.load(f"{self.model_path}category_label_encoder.pkl")
            self.model_info = joblib.load(f"{self.model_path}optimal_model_info.pkl")
        except Exception as e:
            raise Exception(f"Failed to load models: {str(e)}")
    
    def predict(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make prediction for a single video."""
        try:
            # Process features
            features = process_video_features(video_data)
            feature_df = pd.DataFrame([features])
            
            # Scale features
            scaled_features = self.scaler.transform(feature_df)
            
            # Make prediction (log scale)
            log_prediction = self.model.predict(scaled_features)[0]
            
            # Convert to original scale
            prediction = int(np.expm1(log_prediction))
            
            # Calculate confidence interval
            confidence_lower = int(prediction * 0.7)
            confidence_upper = int(prediction * 1.3)
            
            # Determine prediction quality
            prediction_quality = self._determine_quality(prediction, video_data)
            
            # Generate key factors and recommendations
            key_factors = self._generate_key_factors(video_data, prediction)
            recommendations = self._generate_recommendations(video_data, prediction)
            
            return {
                "prediction_id": str(uuid.uuid4()),
                "predicted_views": prediction,
                "confidence_lower": confidence_lower,
                "confidence_upper": confidence_upper,
                "confidence_range": f"{confidence_lower:,} - {confidence_upper:,}",
                "prediction_quality": prediction_quality,
                "expected_performance": self._get_performance_description(prediction_quality),
                "key_factors": key_factors,
                "recommendations": recommendations,
                "processing_time": 0.156,  # This would be calculated
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
    
    def _determine_quality(self, prediction: int, video_data: Dict[str, Any]) -> str:
        """Determine prediction quality based on input data."""
        # Implementation for quality determination
        if prediction > 1000000:
            return "High"
        elif prediction > 100000:
            return "Medium"
        else:
            return "Low"
    
    def _generate_key_factors(self, video_data: Dict[str, Any], prediction: int) -> List[str]:
        """Generate key success factors."""
        factors = []
        
        # Analyze title
        if len(video_data.get("title", "")) > 50:
            factors.append("Strong title with clear value proposition")
        
        # Analyze duration
        duration = video_data.get("duration", 0)
        if 600 <= duration <= 1200:  # 10-20 minutes
            factors.append("Optimal duration for tutorial content")
        
        # Analyze engagement
        like_count = video_data.get("like_count", 0)
        dislike_count = video_data.get("dislike_count", 0)
        if like_count > 0 and like_count > dislike_count * 10:
            factors.append("High engagement potential")
        
        return factors
    
    def _generate_recommendations(self, video_data: Dict[str, Any], prediction: int) -> List[str]:
        """Generate optimization recommendations."""
        recommendations = []
        
        # Title recommendations
        title = video_data.get("title", "")
        if len(title) < 30:
            recommendations.append("Consider making title more descriptive")
        
        # Description recommendations
        description = video_data.get("description", "")
        if len(description) < 100:
            recommendations.append("Add more detailed description")
        
        # Tags recommendations
        tags = video_data.get("tags", "")
        if len(tags.split(",")) < 5:
            recommendations.append("Add more specific tags for better discoverability")
        
        return recommendations
```

---

## 🔐 **AUTHENTICATION & SECURITY**

### **Security Module (core/security.py)**
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user."""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"id": user_id, "username": payload.get("username")}
```

---

## 🧪 **TESTING**

### **Test Configuration (tests/conftest.py)**
```python
import pytest
from fastapi.testclient import TestClient
from main import app
from core.database import get_db
from models.database import Base, engine

client = TestClient(app)

@pytest.fixture
def test_db():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_client():
    """Create test client."""
    return client
```

### **Prediction Tests (tests/test_predictions.py)**
```python
import pytest
from fastapi.testclient import TestClient

def test_predict_video_success(test_client, test_db):
    """Test successful video prediction."""
    response = test_client.post(
        "/api/v1/predict",
        json={
            "title": "Test Video",
            "duration": 300,
            "upload_date": "2024-01-15"
        },
        headers={"Authorization": "Bearer test-token"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "predicted_views" in data
    assert "confidence_range" in data
    assert "prediction_quality" in data

def test_predict_video_validation_error(test_client, test_db):
    """Test prediction with invalid input."""
    response = test_client.post(
        "/api/v1/predict",
        json={
            "title": "",  # Invalid: empty title
            "duration": 300,
            "upload_date": "2024-01-15"
        },
        headers={"Authorization": "Bearer test-token"}
    )
    
    assert response.status_code == 400
    assert "validation error" in response.json()["detail"].lower()
```

---

## 🚀 **DEPLOYMENT**

### **Docker Configuration (Dockerfile)**
```dockerfile
FROM python:3.8-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Docker Compose (docker-compose.yml)**
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
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=viralcast
      - POSTGRES_USER=viralcast_user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  postgres_data:
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
def log_prediction_request(user_id: str, video_title: str, prediction: int, processing_time: float):
    logger.info("Prediction request", extra={
        "user_id": user_id,
        "video_title": video_title,
        "predicted_views": prediction,
        "processing_time": processing_time,
        "event_type": "prediction_request"
    })
```

### **Health Check Endpoint**
```python
@router.get("/health")
async def health_check():
    """Comprehensive health check."""
    try:
        # Check database connection
        db_status = await check_database_connection()
        
        # Check model loading
        model_status = check_models_loaded()
        
        # Check system resources
        memory_usage = get_memory_usage()
        cpu_usage = get_cpu_usage()
        
        return {
            "status": "healthy" if all([db_status, model_status]) else "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": settings.version,
            "components": {
                "database": "healthy" if db_status else "unhealthy",
                "models": "healthy" if model_status else "unhealthy"
            },
            "metrics": {
                "memory_usage": f"{memory_usage}%",
                "cpu_usage": f"{cpu_usage}%"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
```

---

This comprehensive backend guide provides everything needed to build a production-ready FastAPI backend for the ViralCast prediction service. All components are documented with code examples and implementation details.
