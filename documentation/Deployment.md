# 🚀 Deployment Guide

Comprehensive guide for deploying the CCI Hackathon 2025 Backend to various platforms and environments.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Considerations](#production-considerations)
- [Monitoring and Logging](#monitoring-and-logging)
- [Scaling Strategies](#scaling-strategies)
- [Security Hardening](#security-hardening)

## 🔧 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: Minimum 512MB RAM
- **Storage**: 1GB free space
- **Network**: Internet connection for AI services

### External Dependencies
- **MongoDB**: Database server (local or cloud)
- **Perplexity AI**: API key for receipt processing
- **KronosLabs**: API key for recipe generation

### Required Environment Variables
```env
PERPLEXITY_API_KEY=your_perplexity_api_key
KRONOSLABS_API_KEY=your_kronoslabs_api_key
MONGODB_URI=your_mongodb_connection_string
```

## 🏠 Local Development

### 1. Clone Repository
```bash
git clone <repository-url>
cd cci-hackathon-2025-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Start Development Server
```bash
python main.py
```

### 6. Verify Deployment
```bash
curl http://localhost:8000/health
```

## 🐳 Docker Deployment

### 1. Create Dockerfile
```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python", "main.py"]
```

### 2. Build Docker Image
```bash
docker build -t cci-hackathon-backend .
```

### 3. Run Container
```bash
docker run -d \
  --name cci-backend \
  -p 8000:8000 \
  --env-file .env \
  cci-hackathon-backend
```

### 4. Docker Compose Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY}
      - KRONOSLABS_API_KEY=${KRONOSLABS_API_KEY}
      - MONGODB_URI=${MONGODB_URI}
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped

volumes:
  mongodb_data:
```

### 5. Deploy with Docker Compose
```bash
docker-compose up -d
```

## ☁️ Cloud Deployment

### AWS Deployment

#### 1. EC2 Instance
```bash
# Launch EC2 instance (Ubuntu 20.04)
# Install Docker
sudo apt update
sudo apt install docker.io docker-compose

# Clone and deploy
git clone <repository-url>
cd cci-hackathon-2025-backend
docker-compose up -d
```

#### 2. ECS (Elastic Container Service)
```json
// task-definition.json
{
  "family": "cci-hackathon-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "cci-backend",
      "image": "your-account.dkr.ecr.region.amazonaws.com/cci-hackathon-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "PERPLEXITY_API_KEY",
          "value": "your-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/cci-hackathon-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 3. Lambda (Serverless)
```python
# lambda_handler.py
import json
from mangum import Mangum
from main import app

handler = Mangum(app)

def lambda_handler(event, context):
    return handler(event, context)
```

### Google Cloud Platform

#### 1. Cloud Run
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/cci-hackathon-backend', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/cci-hackathon-backend']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: [
      'run', 'deploy', 'cci-hackathon-backend',
      '--image', 'gcr.io/$PROJECT_ID/cci-hackathon-backend',
      '--region', 'us-central1',
      '--platform', 'managed',
      '--allow-unauthenticated'
    ]
```

#### 2. Deploy to Cloud Run
```bash
gcloud builds submit --config cloudbuild.yaml
```

### Heroku Deployment

#### 1. Create Heroku App
```bash
heroku create cci-hackathon-backend
```

#### 2. Set Environment Variables
```bash
heroku config:set PERPLEXITY_API_KEY=your_key
heroku config:set KRONOSLABS_API_KEY=your_key
heroku config:set MONGODB_URI=your_mongodb_uri
```

#### 3. Deploy
```bash
git push heroku main
```

#### 4. Procfile
```
web: python main.py
```

### DigitalOcean App Platform

#### 1. app.yaml
```yaml
name: cci-hackathon-backend
services:
- name: api
  source_dir: /
  github:
    repo: your-username/cci-hackathon-2025-backend
    branch: main
  run_command: python main.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: PERPLEXITY_API_KEY
    value: your_api_key
  - key: KRONOSLABS_API_KEY
    value: your_api_key
  - key: MONGODB_URI
    value: your_mongodb_uri
  http_port: 8000
  routes:
  - path: /
```

## 🏭 Production Considerations

### Performance Optimization

#### 1. Gunicorn Configuration
```python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

#### 2. Nginx Configuration
```nginx
# /etc/nginx/sites-available/cci-backend
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # File upload size limit
    client_max_body_size 10M;
}
```

#### 3. Database Optimization
```python
# MongoDB connection with optimizations
client = MongoClient(
    mongodb_uri,
    maxPoolSize=50,
    minPoolSize=10,
    maxIdleTimeMS=30000,
    serverSelectionTimeoutMS=5000,
    socketTimeoutMS=20000
)
```

### Security Hardening

#### 1. Environment Security
```bash
# Set restrictive file permissions
chmod 600 .env
chmod 600 /etc/ssl/private/your-key.pem
```

#### 2. Firewall Configuration
```bash
# UFW firewall rules
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

#### 3. SSL/TLS Configuration
```nginx
# SSL configuration
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/ssl/certs/your-cert.pem;
    ssl_certificate_key /etc/ssl/private/your-key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
}
```

## 📊 Monitoring and Logging

### Application Monitoring

#### 1. Health Check Endpoint
```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "uptime": time.time() - start_time
    }
```

#### 2. Prometheus Metrics
```python
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(time.time() - start_time)
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

#### 3. Logging Configuration
```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

### Infrastructure Monitoring

#### 1. Docker Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

#### 2. System Monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor system resources
htop
iotop
nethogs
```

## 📈 Scaling Strategies

### Horizontal Scaling

#### 1. Load Balancer Configuration
```nginx
upstream backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

#### 2. Docker Swarm
```yaml
# docker-stack.yml
version: '3.8'
services:
  app:
    image: cci-hackathon-backend
    deploy:
      replicas: 4
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    ports:
      - "8000:8000"
    environment:
      - PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY}
```

#### 3. Kubernetes Deployment
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cci-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cci-backend
  template:
    metadata:
      labels:
        app: cci-backend
    spec:
      containers:
      - name: cci-backend
        image: cci-hackathon-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: PERPLEXITY_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: perplexity-key
---
apiVersion: v1
kind: Service
metadata:
  name: cci-backend-service
spec:
  selector:
    app: cci-backend
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Vertical Scaling

#### 1. Resource Limits
```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

#### 2. Database Scaling
```python
# MongoDB replica set configuration
MONGODB_URI = "mongodb://primary:27017,secondary1:27017,secondary2:27017/cci_hackathon?replicaSet=rs0"
```

## 🔒 Security Hardening

### 1. Container Security
```dockerfile
# Use non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Remove unnecessary packages
RUN apt-get purge -y gcc && apt-get autoremove -y
```

### 2. Network Security
```bash
# Configure iptables
sudo iptables -A INPUT -p tcp --dport 8000 -s 192.168.1.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8000 -j DROP
```

### 3. API Security
```python
# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/receipts/")
@limiter.limit("10/minute")
async def process_receipt(request: Request, file: UploadFile = File(...)):
    # Implementation
    pass
```

## 🚨 Disaster Recovery

### 1. Backup Strategy
```bash
# MongoDB backup
mongodump --uri="mongodb://localhost:27017/cci_hackathon" --out=/backup/$(date +%Y%m%d)

# Application backup
tar -czf app-backup-$(date +%Y%m%d).tar.gz /app
```

### 2. Recovery Procedures
```bash
# Restore MongoDB
mongorestore --uri="mongodb://localhost:27017/cci_hackathon" /backup/20240101

# Restore application
tar -xzf app-backup-20240101.tar.gz -C /
```

### 3. High Availability
```yaml
# docker-compose.yml with restart policies
services:
  app:
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```
