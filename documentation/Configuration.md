# ⚙️ Configuration Guide

Complete guide to configuring the CCI Hackathon 2025 Backend application.

## 📋 Table of Contents

- [Environment Variables](#environment-variables)
- [Configuration Files](#configuration-files)
- [Database Configuration](#database-configuration)
- [AI Service Configuration](#ai-service-configuration)
- [Server Configuration](#server-configuration)
- [Security Configuration](#security-configuration)
- [Development vs Production](#development-vs-production)

## 🔧 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `PERPLEXITY_API_KEY` | Perplexity AI API key for receipt processing | `pplx-xxxxxxxxxxxxxxxx` |
| `KRONOSLABS_API_KEY` | KronosLabs API key for recipe generation | `kronos_xxxxxxxxxxxxxxxx` |
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/cci_hackathon` |

### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `HOST` | Server host address | `0.0.0.0` | `127.0.0.1` |
| `PORT` | Server port number | `8000` | `3000` |
| `APP_TITLE` | Application title | `CCI Hackathon 2025 Backend` | `My Food API` |
| `APP_DESCRIPTION` | Application description | `A food management system` | `Custom description` |
| `APP_VERSION` | Application version | `1.0.0` | `2.1.0` |
| `CORS_ORIGINS` | CORS allowed origins | `*` | `http://localhost:3000,https://myapp.com` |
| `CORS_CREDENTIALS` | CORS credentials | `true` | `false` |
| `CORS_METHODS` | CORS allowed methods | `*` | `GET,POST,PUT,DELETE` |
| `CORS_HEADERS` | CORS allowed headers | `*` | `Content-Type,Authorization` |
| `PERPLEXITY_MODEL` | Perplexity AI model | `sonar-pro` | `sonar-medium` |
| `KRONOSLABS_MODEL` | KronosLabs model | `hermes` | `gpt-4` |
| `KRONOSLABS_TEMPERATURE` | AI temperature setting | `0.8` | `0.5` |
| `STANDARDIZATION_THRESHOLD` | Item matching threshold | `80` | `75` |

## 📁 Configuration Files

### .env File Structure
```env
# API Keys (Required)
PERPLEXITY_API_KEY=your_perplexity_api_key_here
KRONOSLABS_API_KEY=your_kronoslabs_api_key_here

# Database (Required)
MONGODB_URI=your_mongodb_connection_string_here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Application Settings
APP_TITLE=CCI Hackathon 2025 Backend
APP_DESCRIPTION=A food management and recipe recommendation system
APP_VERSION=1.0.0

# CORS Settings
CORS_ORIGINS=*
CORS_CREDENTIALS=true
CORS_METHODS=*
CORS_HEADERS=*

# AI Model Settings
PERPLEXITY_MODEL=sonar-pro
KRONOSLABS_MODEL=hermes
KRONOSLABS_TEMPERATURE=0.8

# Standardization Settings
STANDARDIZATION_THRESHOLD=80
```

### .env.example Template
```env
# Copy this file to .env and fill in your actual values

# API Keys - Get these from your service providers
PERPLEXITY_API_KEY=your_perplexity_api_key_here
KRONOSLABS_API_KEY=your_kronoslabs_api_key_here

# Database - Replace with your MongoDB connection string
MONGODB_URI=your_mongodb_connection_string_here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Application Settings
APP_TITLE=CCI Hackathon 2025 Backend
APP_DESCRIPTION=A food management and recipe recommendation system
APP_VERSION=1.0.0

# CORS Settings
CORS_ORIGINS=*
CORS_CREDENTIALS=true
CORS_METHODS=*
CORS_HEADERS=*

# AI Model Settings
PERPLEXITY_MODEL=sonar-pro
KRONOSLABS_MODEL=hermes
KRONOSLABS_TEMPERATURE=0.8

# Standardization Settings
STANDARDIZATION_THRESHOLD=80
```

## 🗄️ Database Configuration

### MongoDB Connection Strings

#### Local Development
```env
MONGODB_URI=mongodb://localhost:27017/cci_hackathon
```

#### MongoDB Atlas (Cloud)
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/cci_hackathon?retryWrites=true&w=majority
```

#### MongoDB with Authentication
```env
MONGODB_URI=mongodb://username:password@localhost:27017/cci_hackathon?authSource=admin
```

#### MongoDB with SSL
```env
MONGODB_URI=mongodb://username:password@localhost:27017/cci_hackathon?ssl=true&ssl_cert_reqs=CERT_NONE
```

### Database Settings
```python
# MongoDB connection configuration
client = MongoClient(
    mongodb_uri, 
    tls=True, 
    tlsAllowInvalidCertificates=True
)
db = client["cci_hackathon"]
```

## 🤖 AI Service Configuration

### Perplexity AI Setup

1. **Get API Key**
   - Visit [Perplexity AI](https://www.perplexity.ai/)
   - Sign up for an account
   - Generate an API key

2. **Configure Model**
   ```env
   PERPLEXITY_MODEL=sonar-pro  # Recommended for vision tasks
   ```

3. **Available Models**
   - `sonar-pro`: Best for vision and complex tasks
   - `sonar-medium`: Balanced performance and cost
   - `sonar-small`: Fast and cost-effective

### KronosLabs Setup

1. **Get API Key**
   - Visit [KronosLabs](https://kronoslabs.ai/)
   - Sign up for an account
   - Generate an API key

2. **Configure Model**
   ```env
   KRONOSLABS_MODEL=hermes
   KRONOSLABS_TEMPERATURE=0.8
   ```

3. **Temperature Settings**
   - `0.0-0.3`: Very focused, deterministic
   - `0.4-0.7`: Balanced creativity and consistency
   - `0.8-1.0`: More creative and varied

## 🖥️ Server Configuration

### Development Server
```env
HOST=127.0.0.1
PORT=8000
```

### Production Server
```env
HOST=0.0.0.0
PORT=8000
```

### Custom Port Configuration
```env
PORT=3000  # Use port 3000 instead of 8000
```

### Uvicorn Configuration
```python
# In main.py
uvicorn.run(
    app, 
    host=os.getenv("HOST", "0.0.0.0"), 
    port=int(os.getenv("PORT", 8000))
)
```

## 🔒 Security Configuration

### CORS Configuration

#### Development (Permissive)
```env
CORS_ORIGINS=*
CORS_CREDENTIALS=true
CORS_METHODS=*
CORS_HEADERS=*
```

#### Production (Restrictive)
```env
CORS_ORIGINS=https://myapp.com,https://www.myapp.com
CORS_CREDENTIALS=true
CORS_METHODS=GET,POST,PUT,DELETE
CORS_HEADERS=Content-Type,Authorization
```

#### Multiple Origins
```env
CORS_ORIGINS=http://localhost:3000,https://staging.myapp.com,https://myapp.com
```

### Environment Security

#### .gitignore Configuration
```gitignore
# Environment files
.env
.env.local
.env.production
.env.staging

# API keys
*.key
*.pem
```

#### Environment File Permissions
```bash
# Set restrictive permissions
chmod 600 .env
```

## 🏗️ Development vs Production

### Development Configuration
```env
# .env.development
HOST=127.0.0.1
PORT=8000
CORS_ORIGINS=*
APP_TITLE=CCI Hackathon 2025 Backend (Dev)
KRONOSLABS_TEMPERATURE=0.9  # More creative for testing
STANDARDIZATION_THRESHOLD=70  # More lenient matching
```

### Production Configuration
```env
# .env.production
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=https://myapp.com
APP_TITLE=CCI Hackathon 2025 Backend
KRONOSLABS_TEMPERATURE=0.7  # More consistent
STANDARDIZATION_THRESHOLD=80  # Standard matching
```

### Staging Configuration
```env
# .env.staging
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=https://staging.myapp.com
APP_TITLE=CCI Hackathon 2025 Backend (Staging)
KRONOSLABS_TEMPERATURE=0.8
STANDARDIZATION_THRESHOLD=75
```

## 🔧 Configuration Validation

### Environment Variable Validation
```python
# Add to main.py for validation
def validate_environment():
    required_vars = [
        "PERPLEXITY_API_KEY",
        "KRONOSLABS_API_KEY", 
        "MONGODB_URI"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise RuntimeError(f"Missing required environment variables: {missing_vars}")

# Call validation on startup
validate_environment()
```

### Configuration Testing
```python
# Test configuration
def test_configuration():
    # Test MongoDB connection
    try:
        client = MongoClient(os.getenv("MONGODB_URI"))
        client.admin.command('ping')
        print("✅ MongoDB connection successful")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
    
    # Test API keys (optional)
    if os.getenv("PERPLEXITY_API_KEY"):
        print("✅ Perplexity API key configured")
    else:
        print("❌ Perplexity API key missing")
```

## 📊 Configuration Monitoring

### Health Check Endpoint
```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "development")
    }
```

### Configuration Endpoint (Development Only)
```python
@app.get("/config")
def get_config():
    if os.getenv("ENVIRONMENT") == "production":
        raise HTTPException(status_code=404, detail="Not found")
    
    return {
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT"),
        "cors_origins": os.getenv("CORS_ORIGINS"),
        "perplexity_model": os.getenv("PERPLEXITY_MODEL"),
        "kronoslabs_model": os.getenv("KRONOSLABS_MODEL"),
        "standardization_threshold": os.getenv("STANDARDIZATION_THRESHOLD")
    }
```

## 🚀 Deployment Configuration

### Docker Environment
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

### Docker Compose
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
```

### Kubernetes ConfigMap
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  HOST: "0.0.0.0"
  PORT: "8000"
  APP_TITLE: "CCI Hackathon 2025 Backend"
  PERPLEXITY_MODEL: "sonar-pro"
  KRONOSLABS_MODEL: "hermes"
  STANDARDIZATION_THRESHOLD: "80"
```

## 🔍 Troubleshooting Configuration

### Common Issues

1. **Missing Environment Variables**
   ```bash
   # Check if .env file exists
   ls -la .env
   
   # Verify environment variables are loaded
   python -c "import os; print(os.getenv('PERPLEXITY_API_KEY'))"
   ```

2. **MongoDB Connection Issues**
   ```bash
   # Test MongoDB connection
   mongosh "mongodb://localhost:27017/cci_hackathon"
   ```

3. **CORS Issues**
   ```bash
   # Check CORS configuration
   curl -H "Origin: http://localhost:3000" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        -X OPTIONS \
        http://localhost:8000/receipts/
   ```

### Configuration Debugging
```python
# Add to main.py for debugging
import logging
logging.basicConfig(level=logging.DEBUG)

@app.on_event("startup")
async def startup_event():
    logging.info(f"Starting server on {os.getenv('HOST')}:{os.getenv('PORT')}")
    logging.info(f"Using MongoDB: {os.getenv('MONGODB_URI')}")
    logging.info(f"Perplexity model: {os.getenv('PERPLEXITY_MODEL')}")
    logging.info(f"KronosLabs model: {os.getenv('KRONOSLABS_MODEL')}")
```
