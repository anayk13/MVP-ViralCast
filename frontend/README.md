# 🎨 ViralCast Frontend - React.js Implementation Guide

## 📋 **OVERVIEW**

Complete frontend implementation guide for the ViralCast YouTube prediction website. This document provides step-by-step instructions for building a modern, responsive React.js frontend.

---

## 🏗️ **PROJECT STRUCTURE**

```
frontend/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   ├── manifest.json
│   └── robots.txt
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Navigation.tsx
│   │   │   ├── LoadingSpinner.tsx
│   │   │   ├── ErrorBoundary.tsx
│   │   │   └── Modal.tsx
│   │   ├── prediction/
│   │   │   ├── PredictionForm.tsx
│   │   │   ├── PredictionResults.tsx
│   │   │   ├── PredictionHistory.tsx
│   │   │   └── VideoPreview.tsx
│   │   ├── analytics/
│   │   │   ├── AnalyticsDashboard.tsx
│   │   │   ├── PerformanceChart.tsx
│   │   │   ├── CategoryAnalysis.tsx
│   │   │   └── TrendAnalysis.tsx
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── AuthGuard.tsx
│   │   └── layout/
│   │       ├── MainLayout.tsx
│   │       ├── Sidebar.tsx
│   │       └── PageHeader.tsx
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── PredictionPage.tsx
│   │   ├── AnalyticsPage.tsx
│   │   ├── AboutPage.tsx
│   │   └── NotFoundPage.tsx
│   ├── services/
│   │   ├── api.ts
│   │   ├── predictionService.ts
│   │   ├── analyticsService.ts
│   │   └── authService.ts
│   ├── hooks/
│   │   ├── usePrediction.ts
│   │   ├── useAnalytics.ts
│   │   ├── useAuth.ts
│   │   └── useLocalStorage.ts
│   ├── store/
│   │   ├── index.ts
│   │   ├── slices/
│   │   │   ├── authSlice.ts
│   │   │   ├── predictionSlice.ts
│   │   │   └── analyticsSlice.ts
│   │   └── middleware.ts
│   ├── utils/
│   │   ├── validation.ts
│   │   ├── formatting.ts
│   │   ├── constants.ts
│   │   └── helpers.ts
│   ├── types/
│   │   ├── prediction.ts
│   │   ├── analytics.ts
│   │   ├── user.ts
│   │   └── api.ts
│   ├── styles/
│   │   ├── globals.css
│   │   ├── components.css
│   │   ├── variables.css
│   │   └── animations.css
│   ├── App.tsx
│   └── index.tsx
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── .env.example
└── README.md
```

---

## 🚀 **QUICK START**

### **1. Environment Setup**
```bash
# Install Node.js (18+ recommended)
# Install dependencies
npm install

# Copy environment file
cp .env.example .env
```

### **2. Development Server**
```bash
# Start development server
npm start

# Or with specific port
PORT=3000 npm start
```

### **3. Build for Production**
```bash
# Build the application
npm run build

# Serve the build
npm run serve
```

### **4. Run Tests**
```bash
# Run unit tests
npm test

# Run tests with coverage
npm run test:coverage

# Run e2e tests
npm run test:e2e
```

---

## 📦 **DEPENDENCIES**

### **package.json**
```json
{
  "name": "viralcast-frontend",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "react-redux": "^8.0.5",
    "@reduxjs/toolkit": "^1.9.3",
    "axios": "^1.3.4",
    "react-hook-form": "^7.43.5",
    "react-query": "^3.39.3",
    "chart.js": "^4.2.1",
    "react-chartjs-2": "^5.2.0",
    "date-fns": "^2.29.3",
    "clsx": "^1.2.1",
    "react-hot-toast": "^2.4.0",
    "framer-motion": "^10.0.1",
    "react-icons": "^4.7.1"
  },
  "devDependencies": {
    "@types/react": "^18.0.28",
    "@types/react-dom": "^18.0.11",
    "@types/node": "^18.15.0",
    "typescript": "^4.9.5",
    "tailwindcss": "^3.2.7",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.21",
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^5.16.5",
    "jest": "^29.4.3",
    "cypress": "^12.6.0",
    "eslint": "^8.35.0",
    "prettier": "^2.8.4"
  }
}
```

---

## ⚙️ **CONFIGURATION**

### **Environment Variables (.env)**
```bash
# API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_VERSION=v1

# App Configuration
REACT_APP_NAME=ViralCast
REACT_APP_VERSION=1.0.0
REACT_APP_ENVIRONMENT=development

# Feature Flags
REACT_APP_ENABLE_ANALYTICS=true
REACT_APP_ENABLE_BATCH_PREDICTION=true
REACT_APP_ENABLE_USER_ACCOUNTS=true

# External Services
REACT_APP_GOOGLE_ANALYTICS_ID=GA_MEASUREMENT_ID
REACT_APP_SENTRY_DSN=SENTRY_DSN_URL
```

### **TypeScript Configuration (tsconfig.json)**
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": [
    "src"
  ]
}
```

### **Tailwind Configuration (tailwind.config.js)**
```javascript
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e3f2fd',
          100: '#bbdefb',
          200: '#90caf9',
          300: '#64b5f6',
          400: '#42a5f5',
          500: '#2196f3',
          600: '#1e88e5',
          700: '#1976d2',
          800: '#1565c0',
          900: '#0d47a1',
        },
        success: '#4caf50',
        warning: '#ff9800',
        error: '#f44336',
        info: '#00bcd4',
      },
      fontFamily: {
        sans: ['Roboto', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

---

## 🎨 **COMPONENT IMPLEMENTATION**

### **Main Layout (components/layout/MainLayout.tsx)**
```typescript
import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from '../common/Header';
import Footer from '../common/Footer';
import Sidebar from './Sidebar';

const MainLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
      <Footer />
    </div>
  );
};

export default MainLayout;
```

### **Prediction Form (components/prediction/PredictionForm.tsx)**
```typescript
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { usePrediction } from '../../hooks/usePrediction';

const predictionSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
  description: z.string().max(5000, 'Description too long').optional(),
  duration: z.number().min(1, 'Duration must be at least 1 second').max(7200, 'Duration too long'),
  like_count: z.number().min(0, 'Likes cannot be negative').optional(),
  dislike_count: z.number().min(0, 'Dislikes cannot be negative').optional(),
  comment_count: z.number().min(0, 'Comments cannot be negative').optional(),
  upload_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Invalid date format'),
  upload_time: z.string().regex(/^\d{2}:\d{2}$/, 'Invalid time format').optional(),
  tags: z.string().optional(),
  category: z.string().optional(),
});

type PredictionFormData = z.infer<typeof predictionSchema>;

const PredictionForm: React.FC = () => {
  const { predictVideo, loading, error } = usePrediction();
  const { register, handleSubmit, formState: { errors }, reset } = useForm<PredictionFormData>({
    resolver: zodResolver(predictionSchema)
  });

  const onSubmit = async (data: PredictionFormData) => {
    try {
      await predictVideo(data);
      reset();
    } catch (err) {
      console.error('Prediction failed:', err);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          🎬 Predict Your Video Success
        </h1>
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Video Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Video Title *
            </label>
            <input
              {...register('title')}
              type="text"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Enter your video title..."
            />
            {errors.title && (
              <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
            )}
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              {...register('description')}
              rows={4}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Enter video description..."
            />
            {errors.description && (
              <p className="mt-1 text-sm text-red-600">{errors.description.message}</p>
            )}
          </div>

          {/* Duration and Category */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Duration (minutes) *
              </label>
              <input
                {...register('duration', { valueAsNumber: true })}
                type="number"
                min="1"
                max="120"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="15"
              />
              {errors.duration && (
                <p className="mt-1 text-sm text-red-600">{errors.duration.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Category
              </label>
              <select
                {...register('category')}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="">Select category...</option>
                <option value="Education">Education</option>
                <option value="Technology">Technology</option>
                <option value="Gaming">Gaming</option>
                <option value="Entertainment">Entertainment</option>
                <option value="Music">Music</option>
                <option value="Sports">Sports</option>
              </select>
            </div>
          </div>

          {/* Engagement Metrics */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Engagement (Optional)</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  👍 Likes
                </label>
                <input
                  {...register('like_count', { valueAsNumber: true })}
                  type="number"
                  min="0"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="0"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  👎 Dislikes
                </label>
                <input
                  {...register('dislike_count', { valueAsNumber: true })}
                  type="number"
                  min="0"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="0"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  💬 Comments
                </label>
                <input
                  {...register('comment_count', { valueAsNumber: true })}
                  type="number"
                  min="0"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="0"
                />
              </div>
            </div>
          </div>

          {/* Upload Details */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Upload Details</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  📅 Upload Date *
                </label>
                <input
                  {...register('upload_date')}
                  type="date"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
                {errors.upload_date && (
                  <p className="mt-1 text-sm text-red-600">{errors.upload_date.message}</p>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  🕐 Upload Time
                </label>
                <input
                  {...register('upload_time')}
                  type="time"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
            </div>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              🏷️ Tags (comma-separated)
            </label>
            <input
              {...register('tags')}
              type="text"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="python, tutorial, coding, machine learning"
            />
          </div>

          {/* Submit Buttons */}
          <div className="flex space-x-4">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-primary-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-primary-700 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? '🔮 Predicting...' : '🔮 PREDICT VIEWS'}
            </button>
            <button
              type="button"
              onClick={() => reset()}
              className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              🔄 Reset
            </button>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-600">{error}</p>
            </div>
          )}
        </form>
      </div>
    </div>
  );
};

export default PredictionForm;
```

### **Prediction Results (components/prediction/PredictionResults.tsx)**
```typescript
import React from 'react';
import { PredictionResult } from '../../types/prediction';

interface PredictionResultsProps {
  prediction: PredictionResult;
  onPredictAnother: () => void;
  onSaveResult: () => void;
}

const PredictionResults: React.FC<PredictionResultsProps> = ({
  prediction,
  onPredictAnother,
  onSaveResult
}) => {
  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US').format(num);
  };

  const getQualityColor = (quality: string) => {
    switch (quality.toLowerCase()) {
      case 'high':
        return 'text-green-600 bg-green-50';
      case 'medium':
        return 'text-yellow-600 bg-yellow-50';
      case 'low':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          🎯 Prediction Results
        </h1>

        {/* Video Title */}
        <div className="mb-8">
          <h2 className="text-xl font-medium text-gray-900 mb-2">
            📹 "{prediction.video_title}"
          </h2>
        </div>

        {/* Main Prediction Card */}
        <div className="bg-gradient-to-r from-primary-50 to-primary-100 rounded-lg p-8 mb-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold text-primary-900 mb-2">
              🎯 PREDICTED VIEWS: {formatNumber(prediction.predicted_views)}
            </h3>
            <p className="text-lg text-primary-700 mb-4">
              📊 Confidence Range: {prediction.confidence_range}
            </p>
            <div className="flex justify-center items-center space-x-4">
              <span className={`px-4 py-2 rounded-full text-sm font-medium ${getQualityColor(prediction.prediction_quality)}`}>
                ⭐ {prediction.prediction_quality} Quality
              </span>
              <span className="text-primary-700 font-medium">
                📈 {prediction.expected_performance}
              </span>
            </div>
          </div>
        </div>

        {/* Performance Breakdown */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white border border-gray-200 rounded-lg p-6 text-center">
            <div className="text-3xl font-bold text-primary-600 mb-2">
              📈 {formatNumber(Math.round(prediction.predicted_views / 30))}
            </div>
            <div className="text-gray-600">Views per day</div>
          </div>
          <div className="bg-white border border-gray-200 rounded-lg p-6 text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">
              👥 High
            </div>
            <div className="text-gray-600">Engagement</div>
          </div>
          <div className="bg-white border border-gray-200 rounded-lg p-6 text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">
              🎯 Education
            </div>
            <div className="text-gray-600">Category</div>
          </div>
        </div>

        {/* Key Success Factors */}
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            🔍 Key Success Factors:
          </h3>
          <ul className="space-y-2">
            {prediction.key_factors.map((factor, index) => (
              <li key={index} className="flex items-start">
                <span className="text-green-500 mr-2">✅</span>
                <span className="text-gray-700">{factor}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Recommendations */}
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            💡 Optimization Recommendations:
          </h3>
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">🎯 Content:</h4>
              <ul className="space-y-1 ml-4">
                {prediction.recommendations.filter(r => r.includes('description') || r.includes('timestamps')).map((rec, index) => (
                  <li key={index} className="text-gray-700">• {rec}</li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">🏷️ Tags:</h4>
              <ul className="space-y-1 ml-4">
                {prediction.recommendations.filter(r => r.includes('tag')).map((rec, index) => (
                  <li key={index} className="text-gray-700">• {rec}</li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">📅 Timing:</h4>
              <ul className="space-y-1 ml-4">
                {prediction.recommendations.filter(r => r.includes('upload') || r.includes('time')).map((rec, index) => (
                  <li key={index} className="text-gray-700">• {rec}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-4">
          <button
            onClick={onPredictAnother}
            className="flex-1 bg-primary-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-primary-700 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          >
            🔄 Predict Another Video
          </button>
          <button
            onClick={onSaveResult}
            className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          >
            💾 Save Results
          </button>
        </div>
      </div>
    </div>
  );
};

export default PredictionResults;
```

---

## 🔌 **API INTEGRATION**

### **API Service (services/api.ts)**
```typescript
import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { PredictionInput, PredictionResult } from '../types/prediction';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for auth
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('authToken');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Prediction endpoints
  async predictVideo(data: PredictionInput): Promise<PredictionResult> {
    const response: AxiosResponse<PredictionResult> = await this.api.post(
      '/api/v1/predict',
      data
    );
    return response.data;
  }

  async predictBatch(videos: PredictionInput[]): Promise<PredictionResult[]> {
    const response: AxiosResponse<{ predictions: PredictionResult[] }> = await this.api.post(
      '/api/v1/predict/batch',
      { videos }
    );
    return response.data.predictions;
  }

  async getPredictionHistory(page = 1, limit = 20): Promise<{
    predictions: PredictionResult[];
    pagination: {
      page: number;
      limit: number;
      total: number;
      pages: number;
    };
  }> {
    const response = await this.api.get('/api/v1/predictions', {
      params: { page, limit }
    });
    return response.data;
  }

  // Analytics endpoints
  async getDashboardData(timeRange = '30d') {
    const response = await this.api.get('/api/v1/analytics/dashboard', {
      params: { time_range: timeRange }
    });
    return response.data;
  }

  async getCategoryTrends() {
    const response = await this.api.get('/api/v1/analytics/categories');
    return response.data;
  }

  // Health check
  async healthCheck() {
    const response = await this.api.get('/api/v1/health');
    return response.data;
  }
}

export default new ApiService();
```

### **Custom Hooks (hooks/usePrediction.ts)**
```typescript
import { useState } from 'react';
import { useMutation, useQueryClient } from 'react-query';
import apiService from '../services/api';
import { PredictionInput, PredictionResult } from '../types/prediction';
import toast from 'react-hot-toast';

export const usePrediction = () => {
  const [currentPrediction, setCurrentPrediction] = useState<PredictionResult | null>(null);
  const queryClient = useQueryClient();

  const predictMutation = useMutation(
    (data: PredictionInput) => apiService.predictVideo(data),
    {
      onSuccess: (data) => {
        setCurrentPrediction(data);
        toast.success('Prediction completed successfully!');
        queryClient.invalidateQueries('predictionHistory');
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.detail || 'Prediction failed');
      },
    }
  );

  const predictVideo = async (data: PredictionInput) => {
    return predictMutation.mutateAsync(data);
  };

  const clearPrediction = () => {
    setCurrentPrediction(null);
  };

  return {
    predictVideo,
    currentPrediction,
    clearPrediction,
    loading: predictMutation.isLoading,
    error: predictMutation.error,
  };
};
```

---

## 🎨 **STYLING & THEMING**

### **Global Styles (styles/globals.css)**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap');

@layer base {
  html {
    font-family: 'Roboto', sans-serif;
  }
  
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

@layer components {
  .btn-primary {
    @apply bg-primary-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-primary-700 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors duration-200;
  }
  
  .btn-secondary {
    @apply bg-white text-gray-700 py-3 px-6 rounded-lg font-medium border border-gray-300 hover:bg-gray-50 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors duration-200;
  }
  
  .input-field {
    @apply w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors duration-200;
  }
  
  .card {
    @apply bg-white rounded-lg shadow-lg border border-gray-200;
  }
  
  .card-header {
    @apply px-6 py-4 border-b border-gray-200;
  }
  
  .card-body {
    @apply px-6 py-4;
  }
}

@layer utilities {
  .text-gradient {
    @apply bg-gradient-to-r from-primary-600 to-primary-800 bg-clip-text text-transparent;
  }
  
  .shadow-soft {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .shadow-medium {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }
  
  .shadow-strong {
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  }
}
```

### **Animation Styles (styles/animations.css)**
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

.animate-slide-up {
  animation: slideUp 0.3s ease-out;
}

.animate-pulse-slow {
  animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

---

## 🧪 **TESTING**

### **Component Tests (components/__tests__/PredictionForm.test.tsx)**
```typescript
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import PredictionForm from '../PredictionForm';

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const queryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('PredictionForm', () => {
  test('renders form fields correctly', () => {
    render(
      <TestWrapper>
        <PredictionForm />
      </TestWrapper>
    );

    expect(screen.getByLabelText(/video title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/duration/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/upload date/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /predict views/i })).toBeInTheDocument();
  });

  test('validates required fields', async () => {
    render(
      <TestWrapper>
        <PredictionForm />
      </TestWrapper>
    );

    const submitButton = screen.getByRole('button', { name: /predict views/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/title is required/i)).toBeInTheDocument();
    });
  });

  test('submits form with valid data', async () => {
    const mockPredict = jest.fn();
    jest.mock('../../hooks/usePrediction', () => ({
      usePrediction: () => ({
        predictVideo: mockPredict,
        loading: false,
        error: null,
      }),
    }));

    render(
      <TestWrapper>
        <PredictionForm />
      </TestWrapper>
    );

    fireEvent.change(screen.getByLabelText(/video title/i), {
      target: { value: 'Test Video' }
    });
    fireEvent.change(screen.getByLabelText(/duration/i), {
      target: { value: '300' }
    });
    fireEvent.change(screen.getByLabelText(/upload date/i), {
      target: { value: '2024-01-15' }
    });

    fireEvent.click(screen.getByRole('button', { name: /predict views/i }));

    await waitFor(() => {
      expect(mockPredict).toHaveBeenCalledWith({
        title: 'Test Video',
        duration: 300,
        upload_date: '2024-01-15',
      });
    });
  });
});
```

---

## 🚀 **DEPLOYMENT**

### **Build Configuration**
```json
{
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "build:prod": "NODE_ENV=production npm run build",
    "serve": "serve -s build -l 3000"
  }
}
```

### **Docker Configuration (Dockerfile)**
```dockerfile
# Build stage
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### **Nginx Configuration (nginx.conf)**
```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Handle client-side routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

This comprehensive frontend guide provides everything needed to build a modern, responsive React.js frontend for the ViralCast prediction service. All components, styling, and integration details are documented with code examples.
