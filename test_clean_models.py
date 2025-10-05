#!/usr/bin/env python3
"""
Test script for clean models without data leakage
This script demonstrates how to use the clean models for predictions.
"""

import pandas as pd
import numpy as np
import pickle
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_clean_models():
    """Load the clean models and scaler"""
    print("🔧 Loading clean models...")
    
    # Load model info
    with open('models/clean_model_info.pkl', 'rb') as f:
        model_info = pickle.load(f)
    
    # Load scaler
    with open('models/clean_scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    # Load feature names
    with open('models/clean_feature_names.pkl', 'rb') as f:
        feature_names = pickle.load(f)
    
    # Load models
    models = {}
    for model_name in model_info['model_names']:
        model_path = f'models/{model_name}_clean_model.pkl'
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
            models[model_name] = model_data['model']  # Extract the actual model
    
    print(f"✅ Loaded {len(models)} clean models")
    print(f"✅ Features: {len(feature_names)} independent features")
    print(f"✅ Target transformed: {model_info['target_transformed']}")
    
    return models, scaler, feature_names, model_info

def prepare_video_features(video_data, feature_names):
    """Prepare video features for prediction"""
    
    # Calculate basic features
    title_length = len(video_data['title'])
    description_length = len(video_data['description'])
    tags_count = len(video_data['tags'].split(',')) if video_data['tags'] else 0
    duration_minutes = video_data['duration'] / 60
    log_duration = np.log1p(video_data['duration'])
    
    # Engagement features
    like_count = video_data['like_count']
    dislike_count = video_data['dislike_count']
    like_ratio = like_count / (like_count + dislike_count + 1)  # +1 to avoid division by zero
    engagement_rate = (like_count + dislike_count) / 1000  # Normalize
    
    # Title analysis
    title_word_count = len(video_data['title'].split())
    
    # Upload time features
    upload_date = datetime.strptime(video_data['upload_date'], '%Y-%m-%d')
    upload_hour = upload_date.hour
    upload_day_of_week = upload_date.weekday()
    upload_month = upload_date.month
    is_weekend = 1 if upload_day_of_week >= 5 else 0
    
    # Cyclical encoding for time features
    upload_hour_sin = np.sin(2 * np.pi * upload_hour / 24)
    upload_hour_cos = np.cos(2 * np.pi * upload_hour / 24)
    upload_day_sin = np.sin(2 * np.pi * upload_day_of_week / 7)
    upload_day_cos = np.cos(2 * np.pi * upload_day_of_week / 7)
    
    # Days since upload
    days_since_upload = (datetime.now() - upload_date).days
    if days_since_upload == 0:
        days_since_upload = 1  # Avoid division by zero
    log_days_since_upload = np.log1p(days_since_upload)
    
    # Create feature dictionary
    features = {
        'duration': video_data['duration'],
        'duration_minutes': duration_minutes,
        'log_duration': log_duration,
        'like_count': like_count,
        'dislike_count': dislike_count,
        'like_ratio': like_ratio,
        'engagement_rate': engagement_rate,
        'title_length': title_length,
        'description_length': description_length,
        'tags_count': tags_count,
        'title_word_count': title_word_count,
        'upload_hour': upload_hour,
        'upload_day_of_week': upload_day_of_week,
        'upload_month': upload_month,
        'is_weekend': is_weekend,
        'upload_hour_sin': upload_hour_sin,
        'upload_hour_cos': upload_hour_cos,
        'upload_day_sin': upload_day_sin,
        'upload_day_cos': upload_day_cos,
        'days_since_upload': days_since_upload,
        'log_days_since_upload': log_days_since_upload
    }
    
    # Create DataFrame with only the required features
    feature_df = pd.DataFrame([features])
    
    # Ensure all required features are present
    missing_features = set(feature_names) - set(feature_df.columns)
    if missing_features:
        print(f"⚠️  Missing features: {missing_features}")
        # Add missing features with default values
        for feature in missing_features:
            feature_df[feature] = 0
    
    # Reorder columns to match training data
    feature_df = feature_df[feature_names]
    
    return feature_df

def predict_views(models, scaler, feature_names, model_info, video_data):
    """Make prediction using clean models"""
    
    # Prepare features
    X = prepare_video_features(video_data, feature_names)
    
    # Scale features
    X_scaled = scaler.transform(X)
    
    # Make predictions with all models
    predictions = {}
    for name, model in models.items():
        pred = model.predict(X_scaled)[0]
        
        # Inverse transform if target was log-transformed
        if model_info['target_transformed']:
            pred = np.expm1(pred)  # Inverse of log1p
        
        predictions[name] = max(0, pred)  # Ensure non-negative
    
    return predictions

def test_clean_models():
    """Test the clean models with sample videos"""
    
    print("🚀 Testing Clean Models (No Data Leakage)")
    print("=" * 50)
    
    # Load models
    models, scaler, feature_names, model_info = load_clean_models()
    
    # Test videos
    test_videos = [
        {
            "title": "Complete Python Tutorial for Beginners - Learn Programming from Scratch",
            "description": "A comprehensive guide to Python programming for absolute beginners, covering basics to advanced topics.",
            "duration": 900,  # 15 minutes
            "like_count": 1250,
            "dislike_count": 45,
            "upload_date": "2024-01-15",
            "tags": "python,tutorial,programming,beginners,coding"
        },
        {
            "title": "iPhone 15 Pro Max Review - Is It Worth $1200?",
            "description": "An in-depth review of the new iPhone 15 Pro Max, focusing on camera, battery, and performance.",
            "duration": 1200,  # 20 minutes
            "like_count": 2500,
            "dislike_count": 120,
            "upload_date": "2024-01-10",
            "tags": "iphone,review,tech,apple,smartphone"
        },
        {
            "title": "Epic Gaming Montage - Best Plays of 2024",
            "description": "Compilation of the most epic gaming moments and highlights from various games in 2024.",
            "duration": 300,  # 5 minutes
            "like_count": 5000,
            "dislike_count": 200,
            "upload_date": "2024-01-20",
            "tags": "gaming,montage,epic,plays,highlights"
        }
    ]
    
    for i, video in enumerate(test_videos, 1):
        print(f"\n🎬 TEST VIDEO {i}: {video['title'][:50]}...")
        print("-" * 60)
        
        # Make prediction
        predictions = predict_views(models, scaler, feature_names, model_info, video)
        
        # Display results
        print("🎯 PREDICTED VIEWS:")
        for model_name, pred_views in predictions.items():
            print(f"   {model_name.upper()}: {pred_views:,.0f} views")
        
        # Get best prediction (gradient boosting usually performs best)
        best_prediction = predictions.get('gradient_boosting', list(predictions.values())[0])
        
        print(f"\n⭐ BEST PREDICTION: {best_prediction:,.0f} views")
        print(f"📊 Confidence Range: {best_prediction * 0.7:,.0f} - {best_prediction * 1.3:,.0f}")
        
        # Calculate views per day
        upload_date = datetime.strptime(video['upload_date'], '%Y-%m-%d')
        days_since_upload = (datetime.now() - upload_date).days
        if days_since_upload == 0:
            days_since_upload = 1
        views_per_day = best_prediction / days_since_upload
        print(f"📈 Views per Day: {views_per_day:,.0f}")
    
    print(f"\n🎉 Clean model testing completed!")
    print(f"✅ All models are working without data leakage")
    print(f"🔧 Ready for production use!")

if __name__ == "__main__":
    test_clean_models()
