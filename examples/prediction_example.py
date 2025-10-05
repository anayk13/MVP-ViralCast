"""
Video Prediction Output Example
Shows exactly what the system will output for users
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

class VideoPredictionExample:
    """Example of what the video prediction system will output"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_models()
    
    def load_models(self):
        """Load the trained models"""
        try:
            # Load the best model (Gradient Boosting)
            self.model = joblib.load('/Users/anaykumar/Desktop/Ly Project/03_MODELS/gradient_boosting_model.pkl')
            self.scaler = joblib.load('/Users/anaykumar/Desktop/Ly Project/03_MODELS/main_scaler.pkl')
            print("✅ Models loaded successfully")
        except:
            print("⚠️  Models not found, using mock data for demonstration")
            self.model = None
            self.scaler = None
    
    def create_sample_video_input(self):
        """Create sample video input data"""
        sample_videos = [
            {
                "title": "How to Build a Machine Learning Model in Python - Complete Tutorial",
                "description": "In this comprehensive tutorial, we'll walk through building a complete machine learning model from scratch using Python, pandas, and scikit-learn. Perfect for beginners!",
                "duration": 1800,  # 30 minutes
                "like_count": 1250,
                "dislike_count": 45,
                "upload_date": "2024-01-15",
                "tags": "python, machine learning, tutorial, data science, programming",
                "channel_id": "tech_tutorials_123"
            },
            {
                "title": "Amazing Cat Compilation - Funny Moments",
                "description": "The funniest cat videos you'll ever see! Watch these adorable cats do the most hilarious things. Guaranteed to make you laugh!",
                "duration": 420,  # 7 minutes
                "like_count": 8500,
                "dislike_count": 120,
                "upload_date": "2024-01-20",
                "tags": "cats, funny, compilation, animals, cute",
                "channel_id": "funny_pets_456"
            },
            {
                "title": "Advanced Quantum Computing Explained",
                "description": "Deep dive into quantum computing principles, quantum algorithms, and their applications in cryptography and optimization problems.",
                "duration": 2400,  # 40 minutes
                "like_count": 320,
                "dislike_count": 15,
                "upload_date": "2024-01-18",
                "tags": "quantum computing, physics, science, technology, research",
                "channel_id": "science_channel_789"
            }
        ]
        return sample_videos
    
    def process_video_features(self, video_data):
        """Process video data into features for prediction"""
        # This would be the actual feature engineering pipeline
        # For demo purposes, we'll create mock features
        
        features = {
            'duration': video_data['duration'],
            'duration_minutes': video_data['duration'] / 60,
            'log_duration': np.log1p(video_data['duration']),
            'like_count': video_data['like_count'],
            'dislike_count': video_data['dislike_count'],
            'like_ratio': video_data['like_count'] / (video_data['like_count'] + video_data['dislike_count'] + 1),
            'engagement_rate': (video_data['like_count'] + video_data['dislike_count']) / 1000,  # Mock view count
            'title_length': len(video_data['title']),
            'description_length': len(video_data['description']),
            'tags_count': len(video_data['tags'].split(',')),
            'title_word_count': len(video_data['title'].split()),
            'upload_hour': 14,  # Mock upload hour
            'upload_day_of_week': 1,  # Mock day
            'upload_month': 1,
            'is_weekend': 0,
            'upload_hour_sin': np.sin(2 * np.pi * 14 / 24),
            'upload_hour_cos': np.cos(2 * np.pi * 14 / 24),
            'upload_day_sin': np.sin(2 * np.pi * 1 / 7),
            'upload_day_cos': np.cos(2 * np.pi * 1 / 7),
            'days_since_upload': 10,
            'log_days_since_upload': np.log1p(10)
        }
        
        return features
    
    def predict_video_views(self, video_data):
        """Predict views for a single video"""
        # Process features
        features = self.process_video_features(video_data)
        
        # Convert to DataFrame
        feature_df = pd.DataFrame([features])
        
        # Scale features
        if self.scaler:
            feature_array = self.scaler.transform(feature_df)
        else:
            feature_array = feature_df.values
        
        # Make prediction
        if self.model:
            # Predict on log scale
            log_prediction = self.model.predict(feature_array)[0]
            # Convert back to original scale
            prediction = np.expm1(log_prediction)
        else:
            # Mock prediction for demo
            prediction = np.random.randint(10000, 1000000)
        
        # Calculate confidence interval (mock)
        confidence_lower = prediction * 0.7
        confidence_upper = prediction * 1.3
        
        return {
            'predicted_views': int(prediction),
            'confidence_lower': int(confidence_lower),
            'confidence_upper': int(confidence_upper),
            'confidence_range': f"{int(confidence_lower):,} - {int(confidence_upper):,}",
            'prediction_quality': 'High' if prediction > 100000 else 'Medium' if prediction > 10000 else 'Low'
        }
    
    def generate_detailed_output(self, video_data, prediction):
        """Generate detailed output for the video"""
        return {
            'video_info': {
                'title': video_data['title'],
                'description': video_data['description'][:100] + '...' if len(video_data['description']) > 100 else video_data['description'],
                'duration': f"{video_data['duration'] // 60}:{video_data['duration'] % 60:02d}",
                'upload_date': video_data['upload_date'],
                'tags': video_data['tags']
            },
            'prediction': {
                'predicted_views': f"{prediction['predicted_views']:,}",
                'confidence_range': prediction['confidence_range'],
                'prediction_quality': prediction['prediction_quality']
            },
            'analysis': {
                'expected_performance': self._get_performance_analysis(prediction['predicted_views']),
                'key_factors': self._get_key_factors(video_data),
                'recommendations': self._get_recommendations(video_data, prediction['predicted_views'])
            }
        }
    
    def _get_performance_analysis(self, predicted_views):
        """Get performance analysis based on predicted views"""
        if predicted_views > 1000000:
            return "Viral potential - High chance of going viral"
        elif predicted_views > 100000:
            return "Strong performance - Expected to perform well"
        elif predicted_views > 10000:
            return "Moderate performance - Decent viewership expected"
        else:
            return "Niche content - Targeted audience expected"
    
    def _get_key_factors(self, video_data):
        """Identify key factors affecting prediction"""
        factors = []
        
        if video_data['duration'] > 1800:  # 30 minutes
            factors.append("Long-form content (good for educational videos)")
        elif video_data['duration'] < 300:  # 5 minutes
            factors.append("Short-form content (good for entertainment)")
        
        if video_data['like_count'] > 1000:
            factors.append("High engagement potential")
        
        if 'tutorial' in video_data['title'].lower() or 'how to' in video_data['title'].lower():
            factors.append("Educational content (good for long-term views)")
        
        if 'funny' in video_data['title'].lower() or 'compilation' in video_data['title'].lower():
            factors.append("Entertainment content (good for immediate views)")
        
        return factors if factors else ["Standard content factors"]
    
    def _get_recommendations(self, video_data, predicted_views):
        """Get recommendations for improving video performance"""
        recommendations = []
        
        if predicted_views < 50000:
            recommendations.append("Consider optimizing title for better discoverability")
            recommendations.append("Add more engaging thumbnail")
            recommendations.append("Improve video description with keywords")
        
        if video_data['duration'] > 2400:  # 40 minutes
            recommendations.append("Consider breaking into shorter segments")
        
        if video_data['like_count'] < 100:
            recommendations.append("Focus on improving content engagement")
        
        return recommendations if recommendations else ["Content looks good - no major changes needed"]
    
    def run_example(self):
        """Run the complete example"""
        print("🎬 VIDEO PREDICTION SYSTEM OUTPUT EXAMPLE")
        print("=" * 60)
        
        # Get sample videos
        sample_videos = self.create_sample_video_input()
        
        for i, video in enumerate(sample_videos, 1):
            print(f"\n📹 VIDEO {i}: {video['title']}")
            print("-" * 50)
            
            # Make prediction
            prediction = self.predict_video_views(video)
            
            # Generate detailed output
            detailed_output = self.generate_detailed_output(video, prediction)
            
            # Display results
            print(f"🎯 PREDICTED VIEWS: {detailed_output['prediction']['predicted_views']}")
            print(f"📊 CONFIDENCE RANGE: {detailed_output['prediction']['confidence_range']}")
            print(f"⭐ QUALITY: {detailed_output['prediction']['prediction_quality']}")
            print(f"📈 PERFORMANCE: {detailed_output['analysis']['expected_performance']}")
            
            print(f"\n🔍 KEY FACTORS:")
            for factor in detailed_output['analysis']['key_factors']:
                print(f"   • {factor}")
            
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in detailed_output['analysis']['recommendations']:
                print(f"   • {rec}")
            
            print("\n" + "=" * 60)

def main():
    """Run the prediction example"""
    example = VideoPredictionExample()
    example.run_example()

if __name__ == "__main__":
    main()

