# 🍽️ CCI Hackathon 2025 Backend

A comprehensive food management and recipe recommendation system built with FastAPI, featuring AI-powered receipt processing and personalized recipe generation.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB database
- Perplexity AI API key
- KronosLabs API key

### 1. Clone and Setup
```bash
git clone <repository-url>
cd cci-hackathon-2025-backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```env
PERPLEXITY_API_KEY=your_perplexity_api_key_here
KRONOSLABS_API_KEY=your_kronoslabs_api_key_here
MONGODB_URI=your_mongodb_connection_string_here
```

### 4. Run the Server
```bash
python main.py
```

🎉 **Server is now running at `http://localhost:8000`**

## 📚 Documentation

For detailed documentation, visit the [Documentation](./Documentation/) folder:

- [📖 API Reference](./Documentation/API-Reference.md) - Complete API endpoint documentation
- [🏗️ Architecture](./Documentation/Architecture.md) - System design and architecture
- [⚙️ Configuration](./Documentation/Configuration.md) - Environment variables and settings
- [🚀 Deployment](./Documentation/Deployment.md) - Production deployment guide
- [👨‍💻 Development](./Documentation/Development.md) - Development setup and guidelines
- [🔧 Troubleshooting](./Documentation/Troubleshooting.md) - Common issues and solutions

## 🌟 Features

### 🧾 Receipt Processing
- Upload receipt images (PNG, JPG, etc.)
- AI-powered text extraction using Perplexity Vision API
- Automatic item name standardization against 5000+ food database
- Price and quantity extraction

### 👤 User Management
- User profile creation with dietary preferences
- Spice level preferences
- Food allergy tracking
- Daily calorie target setting

### 🥘 Recipe Generation
- AI-powered recipe suggestions using KronosLabs
- Personalized based on available ingredients
- Dietary preference compliance
- Detailed cooking instructions with prep/cook times

### 📦 Ingredient Tracking
- MongoDB-based ingredient inventory
- User-specific ingredient management
- Expiry tracking integration

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/receipts/` | Process receipt images |
| `GET` | `/recipes/{user}` | Get personalized recipes |
| `POST` | `/recipes/ingredients/` | Add ingredients to inventory |
| `GET` | `/recipes/ingredients/{user}` | Get user's ingredients |
| `GET` | `/recipes/all-ingredients` | Get all available ingredients |
| `POST` | `/users/` | Create user account |
| `GET` | `/users/{user}` | Get user profile |
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Health check |

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **AI Services**: 
  - Perplexity AI (Vision API)
  - KronosLabs (Recipe Generation)
- **Server**: Uvicorn (ASGI)
- **Data Processing**: RapidFuzz (String Matching)

## 📊 API Documentation

Once running, access interactive documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔧 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `PERPLEXITY_API_KEY` | Perplexity AI API key | ✅ | - |
| `KRONOSLABS_API_KEY` | KronosLabs API key | ✅ | - |
| `MONGODB_URI` | MongoDB connection string | ✅ | - |
| `HOST` | Server host | ❌ | `0.0.0.0` |
| `PORT` | Server port | ❌ | `8000` |
| `PERPLEXITY_MODEL` | Perplexity model | ❌ | `sonar-pro` |
| `KRONOSLABS_MODEL` | KronosLabs model | ❌ | `hermes` |
| `STANDARDIZATION_THRESHOLD` | Item matching threshold | ❌ | `80` |

## 🧪 Testing the API

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Create a User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "john_doe",
    "dietary_preference": "vegetarian",
    "spice_level": "medium",
    "food_allergy": ["peanuts"],
    "daily_calorie_target": 2000
  }'
```

### 3. Add Ingredients
```bash
curl -X POST "http://localhost:8000/recipes/ingredients/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tomato",
    "quantity": 5,
    "unit": "pieces",
    "user": "john_doe"
  }'
```

### 4. Get Recipes
```bash
curl "http://localhost:8000/recipes/john_doe"
```

### 5. Get All Available Ingredients
```bash
curl "http://localhost:8000/recipes/all-ingredients"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

See [Development Guide](./Documentation/Development.md) for detailed instructions.

## 📄 License

This project is part of CCI Hackathon 2025.

## 🆘 Support

- Check [Troubleshooting Guide](./Documentation/Troubleshooting.md)
- Review [API Documentation](./Documentation/API-Reference.md)
- Open an issue for bugs or feature requests
