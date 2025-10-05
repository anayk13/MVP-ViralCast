# 🚀 ViralCast - Complete Deployment Guide

## 📋 **OVERVIEW**

This guide provides step-by-step instructions for deploying the ViralCast YouTube prediction website to production. It covers both development and production deployment scenarios.

---

## 🏗️ **DEPLOYMENT OPTIONS**

### **1. Local Development**
- **Backend**: FastAPI on localhost:8000
- **Frontend**: React on localhost:3000
- **Database**: PostgreSQL on localhost:5432
- **Best for**: Development and testing

### **2. Docker Development**
- **All services**: Docker containers
- **Backend**: localhost:8000
- **Frontend**: localhost:3000
- **Database**: localhost:5432
- **Best for**: Consistent development environment

### **3. Production Deployment**
- **Cloud Platform**: AWS, Google Cloud, or Azure
- **Backend**: FastAPI with Gunicorn
- **Frontend**: Nginx static files
- **Database**: Managed PostgreSQL
- **Best for**: Live production environment

---

## 🚀 **QUICK START - LOCAL DEVELOPMENT**

### **Prerequisites**
- Python 3.8+
- Node.js 18+
- PostgreSQL 13+
- Git

### **1. Clone and Setup**
```bash
# Clone the repository
git clone <repository-url>
cd Website

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials

# Setup frontend
cd ../frontend
npm install
cp .env.example .env
# Edit .env with your API URL
```

### **2. Database Setup**
```bash
# Create database
createdb viralcast

# Run migrations (if using Alembic)
cd backend
alembic upgrade head
```

### **3. Start Services**
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm start
```

### **4. Access Application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🐳 **DOCKER DEPLOYMENT**

### **Prerequisites**
- Docker 20.10+
- Docker Compose 2.0+

### **1. Quick Start with Docker**
```bash
# Clone repository
git clone <repository-url>
cd Website

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### **2. Environment Configuration**
```bash
# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit configuration
nano backend/.env
nano frontend/.env
```

### **3. Database Initialization**
```bash
# The database will be automatically initialized with init.sql
# Check if tables are created
docker-compose exec db psql -U viralcast_user -d viralcast -c "\dt"
```

### **4. Access Services**
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Database**: localhost:5432
- **Redis**: localhost:6379

---

## ☁️ **PRODUCTION DEPLOYMENT**

### **Option 1: AWS Deployment**

#### **1.1 EC2 Instance Setup**
```bash
# Launch EC2 instance (t3.medium or larger)
# Install Docker and Docker Compose
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### **1.2 RDS Database Setup**
```bash
# Create RDS PostgreSQL instance
# Note the endpoint and credentials
# Update docker-compose.yml with RDS endpoint
```

#### **1.3 Application Deployment**
```bash
# Clone repository
git clone <repository-url>
cd Website

# Update environment variables
nano backend/.env
nano frontend/.env

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

### **Option 2: Google Cloud Platform**

#### **2.1 Cloud Run Deployment**
```bash
# Install gcloud CLI
# Authenticate
gcloud auth login

# Build and push images
gcloud builds submit --tag gcr.io/PROJECT_ID/viralcast-backend ./backend
gcloud builds submit --tag gcr.io/PROJECT_ID/viralcast-frontend ./frontend

# Deploy to Cloud Run
gcloud run deploy viralcast-backend --image gcr.io/PROJECT_ID/viralcast-backend --platform managed --region us-central1
gcloud run deploy viralcast-frontend --image gcr.io/PROJECT_ID/viralcast-frontend --platform managed --region us-central1
```

#### **2.2 Cloud SQL Setup**
```bash
# Create Cloud SQL instance
gcloud sql instances create viralcast-db --database-version=POSTGRES_13 --tier=db-f1-micro --region=us-central1

# Create database
gcloud sql databases create viralcast --instance=viralcast-db
```

### **Option 3: Azure Deployment**

#### **3.1 Container Instances**
```bash
# Install Azure CLI
# Login to Azure
az login

# Create resource group
az group create --name viralcast-rg --location eastus

# Deploy container instances
az container create --resource-group viralcast-rg --name viralcast-backend --image your-registry/viralcast-backend --ports 8000
az container create --resource-group viralcast-rg --name viralcast-frontend --image your-registry/viralcast-frontend --ports 80
```

---

## 🔧 **PRODUCTION CONFIGURATION**

### **Environment Variables**

#### **Backend (.env)**
```bash
# Production Database
DATABASE_URL=postgresql://username:password@your-db-host:5432/viralcast

# Security (Generate strong keys)
SECRET_KEY=your-super-secret-key-here-make-it-very-long-and-random
JWT_SECRET=your-jwt-secret-here-different-from-secret-key

# Production Settings
DEBUG=False
LOG_LEVEL=WARNING
CORS_ORIGINS=["https://yourdomain.com"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=1000
RATE_LIMIT_BURST=2000

# External Services
GOOGLE_ANALYTICS_ID=GA_MEASUREMENT_ID
SENTRY_DSN=YOUR_SENTRY_DSN
```

#### **Frontend (.env)**
```bash
# Production API
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENVIRONMENT=production

# External Services
REACT_APP_GOOGLE_ANALYTICS_ID=GA_MEASUREMENT_ID
REACT_APP_SENTRY_DSN=YOUR_SENTRY_DSN
```

### **Nginx Configuration (Production)**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Frontend
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API Proxy
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # Static Assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 📊 **MONITORING & LOGGING**

### **Health Checks**
```bash
# Backend health
curl http://localhost:8000/api/v1/health

# Frontend health
curl http://localhost:3000

# Database health
docker-compose exec db pg_isready -U viralcast_user -d viralcast
```

### **Log Monitoring**
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# View logs with timestamps
docker-compose logs -f -t
```

### **Performance Monitoring**
```bash
# Check container resource usage
docker stats

# Check disk usage
docker system df

# Clean up unused resources
docker system prune -a
```

---

## 🔒 **SECURITY CONSIDERATIONS**

### **1. Environment Security**
- Use strong, unique passwords
- Rotate secrets regularly
- Never commit secrets to version control
- Use environment-specific configurations

### **2. Database Security**
- Enable SSL connections
- Use strong authentication
- Regular backups
- Monitor access logs

### **3. Application Security**
- Enable HTTPS in production
- Implement rate limiting
- Validate all inputs
- Regular security updates

### **4. Infrastructure Security**
- Use VPC/private networks
- Implement firewall rules
- Regular security patches
- Monitor for vulnerabilities

---

## 📈 **SCALING CONSIDERATIONS**

### **Horizontal Scaling**
```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  backend:
    deploy:
      replicas: 3
    environment:
      - DATABASE_POOL_SIZE=20
      - REDIS_URL=redis://redis:6379/0

  frontend:
    deploy:
      replicas: 2

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
      - frontend
```

### **Load Balancing**
```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

upstream frontend {
    server frontend1:80;
    server frontend2:80;
}
```

---

## 🚨 **TROUBLESHOOTING**

### **Common Issues**

#### **1. Database Connection Issues**
```bash
# Check database status
docker-compose exec db pg_isready -U viralcast_user -d viralcast

# Check database logs
docker-compose logs db

# Reset database
docker-compose down
docker volume rm website_postgres_data
docker-compose up -d
```

#### **2. Backend API Issues**
```bash
# Check backend logs
docker-compose logs backend

# Test API directly
curl http://localhost:8000/api/v1/health

# Restart backend
docker-compose restart backend
```

#### **3. Frontend Issues**
```bash
# Check frontend logs
docker-compose logs frontend

# Test frontend
curl http://localhost:3000

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

#### **4. Model Loading Issues**
```bash
# Check if models exist
ls -la models/

# Check model permissions
docker-compose exec backend ls -la /app/models/

# Restart backend with model volume
docker-compose restart backend
```

---

## 📋 **DEPLOYMENT CHECKLIST**

### **Pre-Deployment**
- [ ] Environment variables configured
- [ ] Database credentials updated
- [ ] SSL certificates ready
- [ ] Domain DNS configured
- [ ] Security settings reviewed

### **Deployment**
- [ ] Code deployed to production
- [ ] Database migrations run
- [ ] Services started successfully
- [ ] Health checks passing
- [ ] SSL certificates installed

### **Post-Deployment**
- [ ] Application accessible via domain
- [ ] API endpoints responding
- [ ] Database connections working
- [ ] Monitoring configured
- [ ] Backup strategy implemented

---

## 🎯 **SUCCESS METRICS**

### **Performance Targets**
- **Page Load Time**: < 2 seconds
- **API Response Time**: < 200ms
- **Uptime**: > 99.9%
- **Error Rate**: < 0.1%

### **Monitoring Tools**
- **Application**: Built-in health checks
- **Infrastructure**: Docker stats, system monitoring
- **Database**: PostgreSQL logs and metrics
- **External**: Google Analytics, Sentry

---

This comprehensive deployment guide ensures successful deployment of the ViralCast website in any environment. Follow the steps carefully and monitor the application after deployment.
