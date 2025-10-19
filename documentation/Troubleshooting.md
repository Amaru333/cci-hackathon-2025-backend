# 🔧 Troubleshooting Guide

Comprehensive troubleshooting guide for the CCI Hackathon 2025 Backend application.

## 📋 Table of Contents

- [Common Issues](#common-issues)
- [Installation Problems](#installation-problems)
- [Configuration Issues](#configuration-issues)
- [API Issues](#api-issues)
- [Database Issues](#database-issues)
- [AI Service Issues](#ai-service-issues)
- [Performance Issues](#performance-issues)
- [Debugging Tools](#debugging-tools)
- [Getting Help](#getting-help)

## 🚨 Common Issues

### Application Won't Start

#### Issue: Module Import Errors
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Check if virtual environment is activated
which python
# Should show path to venv/bin/python

# If not activated, activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Issue: Port Already in Use
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000  # On macOS/Linux
netstat -ano | findstr :8000  # On Windows

# Kill the process
kill -9 <PID>  # On macOS/Linux
taskkill /PID <PID> /F  # On Windows

# Or use a different port
export PORT=3000
python main.py
```

#### Issue: Environment Variables Not Loaded
```
RuntimeError: PERPLEXITY_API_KEY not configured
```

**Solution:**
```bash
# Check if .env file exists
ls -la .env

# Check if variables are loaded
python -c "import os; print(os.getenv('PERPLEXITY_API_KEY'))"

# If empty, edit .env file
nano .env
# Add your API keys
```

### API Endpoints Not Working

#### Issue: 404 Not Found
```
{"detail": "Not Found"}
```

**Solution:**
```bash
# Check if server is running
curl http://localhost:8000/health

# Check available endpoints
curl http://localhost:8000/docs

# Verify endpoint URL
curl -X POST http://localhost:8000/receipts/ \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test.jpg"
```

#### Issue: CORS Errors
```
Access to fetch at 'http://localhost:8000/receipts/' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**
```bash
# Check CORS configuration in .env
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Or allow all origins for development
CORS_ORIGINS=*

# Restart the server
python main.py
```

## 📦 Installation Problems

### Python Version Issues

#### Issue: Python Version Too Old
```
ERROR: Package 'fastapi' requires a different Python: 3.7.9 not in '>=3.8'
```

**Solution:**
```bash
# Check Python version
python --version

# Install Python 3.8+ using pyenv
pyenv install 3.9.0
pyenv local 3.9.0

# Or use conda
conda create -n cci-backend python=3.9
conda activate cci-backend
```

### Dependency Installation Issues

#### Issue: NumPy Compatibility
```
A module that was compiled using NumPy 1.x cannot be run in NumPy 2.1.3
```

**Solution:**
```bash
# Downgrade NumPy
pip install "numpy<2.0.0"

# Or upgrade all packages
pip install --upgrade -r requirements.txt
```

#### Issue: MongoDB Driver Issues
```
ERROR: Could not find a version that satisfies the requirement pymongo
```

**Solution:**
```bash
# Update pip
pip install --upgrade pip

# Install with specific version
pip install pymongo==4.6.0

# Or install from requirements
pip install -r requirements.txt --force-reinstall
```

## ⚙️ Configuration Issues

### Environment Variables

#### Issue: API Keys Not Working
```
HTTPException: 401 Unauthorized
```

**Solution:**
```bash
# Verify API key format
echo $PERPLEXITY_API_KEY
# Should start with 'pplx-'

# Test API key manually
curl -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  https://api.perplexity.ai/models

# Check for extra spaces or quotes
# Remove quotes if present
PERPLEXITY_API_KEY=pplx-your-key-here  # Not "pplx-your-key-here"
```

#### Issue: MongoDB Connection Failed
```
ServerSelectionTimeoutError: localhost:27017: [Errno 61] Connection refused
```

**Solution:**
```bash
# Check if MongoDB is running
brew services list | grep mongodb  # On macOS
systemctl status mongod  # On Linux

# Start MongoDB
brew services start mongodb-community  # On macOS
sudo systemctl start mongod  # On Linux

# Test connection
mongosh "mongodb://localhost:27017"

# Check connection string format
MONGODB_URI=mongodb://localhost:27017/cci_hackathon
```

### File Permissions

#### Issue: Permission Denied
```
PermissionError: [Errno 13] Permission denied: '.env'
```

**Solution:**
```bash
# Check file permissions
ls -la .env

# Fix permissions
chmod 600 .env

# Check directory permissions
ls -la .

# Fix directory permissions if needed
chmod 755 .
```

## 🔌 API Issues

### Receipt Processing

#### Issue: File Upload Fails
```
HTTPException: 400 Bad Request - Invalid file format
```

**Solution:**
```bash
# Check file format
file test.jpg
# Should show: JPEG image data

# Check file size
ls -lh test.jpg
# Should be reasonable size (< 10MB)

# Test with different file
curl -X POST http://localhost:8000/receipts/ \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test.png"
```

#### Issue: AI Processing Timeout
```
HTTPException: 500 Internal Server Error - AI processing timeout
```

**Solution:**
```bash
# Check AI service status
curl -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  https://api.perplexity.ai/models

# Reduce file size
convert large_image.jpg -resize 1024x1024 small_image.jpg

# Check network connectivity
ping api.perplexity.ai
```

### Recipe Generation

#### Issue: No Recipes Generated
```
{"recipes": "No recipes could be generated"}
```

**Solution:**
```bash
# Check if user has ingredients
curl http://localhost:8000/recipes/ingredients/john_doe

# Add some ingredients first
curl -X POST http://localhost:8000/recipes/ingredients/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Tomato", "quantity": 5, "unit": "pieces", "user": "john_doe"}'

# Check KronosLabs API key
curl -H "Authorization: Bearer $KRONOSLABS_API_KEY" \
  https://api.kronoslabs.ai/health
```

## 🗄️ Database Issues

### MongoDB Connection

#### Issue: Authentication Failed
```
OperationFailure: Authentication failed
```

**Solution:**
```bash
# Check MongoDB credentials
mongosh "mongodb://username:password@localhost:27017/cci_hackathon"

# Update connection string
MONGODB_URI=mongodb://username:password@localhost:27017/cci_hackathon?authSource=admin

# Create user if needed
mongosh
use cci_hackathon
db.createUser({
  user: "app_user",
  pwd: "app_password",
  roles: ["readWrite"]
})
```

#### Issue: Database Not Found
```
DatabaseNotFound: Database cci_hackathon not found
```

**Solution:**
```bash
# Create database
mongosh
use cci_hackathon
db.test.insertOne({test: "data"})

# Or let the application create it automatically
# The app will create collections when first used
```

### Data Issues

#### Issue: Duplicate User Creation
```
HTTPException: 400 Bad Request - User already exists
```

**Solution:**
```bash
# Check existing users
mongosh
use cci_hackathon
db.users.find()

# Delete user if needed
db.users.deleteOne({user: "john_doe"})

# Or use different username
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"user": "john_doe_2", ...}'
```

## 🤖 AI Service Issues

### Perplexity AI

#### Issue: API Rate Limit
```
HTTPException: 429 Too Many Requests
```

**Solution:**
```bash
# Check API usage
curl -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  https://api.perplexity.ai/usage

# Wait and retry
sleep 60
# Or implement exponential backoff in code
```

#### Issue: Invalid Model
```
HTTPException: 400 Bad Request - Invalid model
```

**Solution:**
```bash
# Check available models
curl -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  https://api.perplexity.ai/models

# Update model in .env
PERPLEXITY_MODEL=sonar-pro  # or sonar-medium, sonar-small
```

### KronosLabs

#### Issue: Recipe Generation Fails
```
HTTPException: 500 Internal Server Error - Recipe generation failed
```

**Solution:**
```bash
# Check API key
curl -H "Authorization: Bearer $KRONOSLABS_API_KEY" \
  https://api.kronoslabs.ai/health

# Check model availability
PERPLEXITY_MODEL=hermes  # or other supported model

# Reduce prompt complexity
# Check if ingredients list is too long
```

## ⚡ Performance Issues

### Slow Response Times

#### Issue: Receipt Processing Takes Too Long
```
Response time > 30 seconds
```

**Solution:**
```bash
# Check image size
ls -lh receipt.jpg
# Optimize image size
convert receipt.jpg -resize 1024x1024 -quality 85 optimized.jpg

# Check network latency
ping api.perplexity.ai

# Monitor system resources
htop
# Check CPU and memory usage
```

#### Issue: Database Queries Slow
```
MongoDB queries taking > 5 seconds
```

**Solution:**
```bash
# Check database indexes
mongosh
use cci_hackathon
db.users.getIndexes()
db.ingredients.getIndexes()

# Create missing indexes
db.users.createIndex({user: 1})
db.ingredients.createIndex({user: 1, name: 1})

# Check query performance
db.users.find({user: "john_doe"}).explain("executionStats")
```

### Memory Issues

#### Issue: High Memory Usage
```
Memory usage > 1GB
```

**Solution:**
```bash
# Check memory usage
ps aux | grep python

# Monitor memory leaks
# Restart application periodically
# Implement connection pooling
# Optimize image processing
```

## 🔍 Debugging Tools

### Logging

#### Enable Debug Logging
```python
# Add to main.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Or set in environment
export LOG_LEVEL=DEBUG
python main.py
```

#### View Application Logs
```bash
# If using Docker
docker logs cci-backend

# If using systemd
journalctl -u cci-backend -f

# If running directly
tail -f app.log
```

### Network Debugging

#### Test API Endpoints
```bash
# Health check
curl -v http://localhost:8000/health

# Test with verbose output
curl -v -X POST http://localhost:8000/receipts/ \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test.jpg"
```

#### Check External Services
```bash
# Test Perplexity AI
curl -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  https://api.perplexity.ai/models

# Test KronosLabs
curl -H "Authorization: Bearer $KRONOSLABS_API_KEY" \
  https://api.kronoslabs.ai/health

# Test MongoDB
mongosh "mongodb://localhost:27017/cci_hackathon"
```

### Database Debugging

#### MongoDB Debugging
```bash
# Connect to MongoDB
mongosh

# Check database status
db.stats()

# Check collections
show collections

# Check document count
db.users.countDocuments()
db.ingredients.countDocuments()

# Check recent documents
db.users.find().sort({_id: -1}).limit(5)
```

#### Query Performance
```bash
# Explain query execution
db.users.find({user: "john_doe"}).explain("executionStats")

# Check slow queries
db.setProfilingLevel(2, {slowms: 100})
db.system.profile.find().sort({ts: -1}).limit(5)
```

## 🆘 Getting Help

### Self-Help Resources

1. **Check Logs**
   ```bash
   # Application logs
   tail -f app.log
   
   # System logs
   journalctl -u your-service-name
   
   # Docker logs
   docker logs container-name
   ```

2. **Verify Configuration**
   ```bash
   # Check environment variables
   env | grep -E "(PERPLEXITY|KRONOSLABS|MONGODB)"
   
   # Test configuration
   python -c "from main import app; print('Config OK')"
   ```

3. **Test Components Individually**
   ```bash
   # Test database
   python -c "from pymongo import MongoClient; print(MongoClient('$MONGODB_URI').admin.command('ping'))"
   
   # Test AI services
   python -c "import requests; print(requests.get('https://api.perplexity.ai/models', headers={'Authorization': f'Bearer $PERPLEXITY_API_KEY'}).status_code)"
   ```

### Community Support

1. **GitHub Issues**
   - Create detailed issue reports
   - Include logs and error messages
   - Provide reproduction steps

2. **Documentation**
   - Check API documentation
   - Review configuration guide
   - Read architecture documentation

3. **Stack Overflow**
   - Tag questions with relevant technologies
   - Provide minimal reproducible examples
   - Include error messages and logs

### Professional Support

For production issues or complex problems:

1. **Contact Development Team**
   - Provide detailed error logs
   - Include system information
   - Describe steps to reproduce

2. **Service Provider Support**
   - Perplexity AI support
   - KronosLabs support
   - MongoDB support

### Issue Reporting Template

```markdown
## Issue Description
Brief description of the problem

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: macOS/Linux/Windows
- Python version: 3.x.x
- Application version: 1.x.x

## Error Logs
```
Paste relevant error logs here
```

## Configuration
- MongoDB URI: (masked)
- API keys: (masked)
- Other relevant config

## Additional Context
Any other relevant information
```

### Emergency Procedures

#### Application Down
1. Check server status
2. Restart application
3. Check resource usage
4. Review recent changes
5. Rollback if necessary

#### Data Loss
1. Stop application
2. Check database backups
3. Restore from backup
4. Verify data integrity
5. Restart application

#### Security Incident
1. Isolate affected systems
2. Change API keys
3. Review access logs
4. Update security measures
5. Notify stakeholders
