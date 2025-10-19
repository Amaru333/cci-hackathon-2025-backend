# 🏗️ System Architecture

Comprehensive overview of the CCI Hackathon 2025 Backend system architecture, design patterns, and technical decisions.

## 📋 Table of Contents

- [System Overview](#system-overview)
- [Architecture Diagram](#architecture-diagram)
- [Core Components](#core-components)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Design Patterns](#design-patterns)
- [Database Design](#database-design)
- [AI Integration](#ai-integration)
- [Security Architecture](#security-architecture)
- [Scalability Considerations](#scalability-considerations)

## 🎯 System Overview

The CCI Hackathon 2025 Backend is a microservices-inspired monolithic application built with FastAPI that provides:

- **Receipt Processing**: AI-powered image analysis and data extraction
- **Recipe Generation**: Personalized recipe recommendations
- **User Management**: Profile and preference management
- **Ingredient Tracking**: Inventory management system

## 🏛️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Applications                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Web App   │  │  Mobile App │  │   API Test  │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP/HTTPS
┌─────────────────────▼───────────────────────────────────────────┐
│                    FastAPI Application                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    API Gateway                              ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        ││
│  │  │   CORS      │  │  Middleware │  │  Validation │        ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘        ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Route Handlers                           ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        ││
│  │  │  Receipt    │  │   Recipe    │  │    User     │        ││
│  │  │  Routes     │  │   Routes    │  │   Routes    │        ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘        ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Business Logic                           ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        ││
│  │  │ Image Proc. │  │ Recipe Gen. │  │ User Mgmt.  │        ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘        ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                    External Services                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ Perplexity  │  │ KronosLabs  │  │  MongoDB    │            │
│  │    AI       │  │     AI      │  │  Database   │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

## 🧩 Core Components

### 1. **API Gateway Layer**
- **FastAPI Application**: Main application entry point
- **CORS Middleware**: Cross-origin request handling
- **Request Validation**: Pydantic model validation
- **Error Handling**: Centralized error management

### 2. **Route Layer**
- **Receipt Routes** (`/receipts/`): Image processing endpoints
- **Recipe Routes** (`/recipes/`): Recipe generation and ingredient management
- **User Routes** (`/users/`): User profile management

### 3. **Business Logic Layer**
- **Image Processing**: Receipt image analysis and data extraction
- **Recipe Generation**: AI-powered recipe recommendations
- **User Management**: Profile and preference handling
- **Data Standardization**: Item name normalization

### 4. **Data Access Layer**
- **MongoDB Integration**: Document-based data storage
- **Connection Management**: Database connection pooling
- **Query Optimization**: Efficient data retrieval

### 5. **External Service Integration**
- **Perplexity AI**: Vision API for receipt processing
- **KronosLabs**: Recipe generation AI service
- **HTTP Client**: RESTful API communication

## 🔄 Data Flow

### Receipt Processing Flow
```
1. Client uploads receipt image
2. FastAPI receives multipart form data
3. Image converted to base64
4. Perplexity AI processes image
5. Raw data extracted and parsed
6. Item names standardized using RapidFuzz
7. Structured data returned to client
```

### Recipe Generation Flow
```
1. Client requests recipes for user
2. System retrieves user ingredients from MongoDB
3. User preferences fetched from database
4. KronosLabs AI generates personalized recipes
5. Recipe data formatted and returned
6. YouTube suggestions included
```

### User Management Flow
```
1. Client creates/updates user profile
2. Data validated using Pydantic models
3. User data stored in MongoDB
4. Unique constraints enforced
5. Success response with user ID returned
```

## 🛠️ Technology Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for production deployment
- **Pydantic**: Data validation and settings management

### Database
- **MongoDB**: NoSQL document database
- **PyMongo**: MongoDB driver for Python

### AI Services
- **Perplexity AI**: Vision API for image processing
- **KronosLabs**: Recipe generation AI
- **RapidFuzz**: String matching and standardization

### Development Tools
- **Python 3.8+**: Programming language
- **python-dotenv**: Environment variable management
- **Requests**: HTTP client library

## 🎨 Design Patterns

### 1. **Repository Pattern**
```python
# Abstract data access layer
class UserRepository:
    def create_user(self, user_data: User) -> User
    def get_user(self, username: str) -> User
    def update_user(self, username: str, user_data: User) -> User
```

### 2. **Service Layer Pattern**
```python
# Business logic encapsulation
class ReceiptService:
    def process_receipt(self, image_file: UploadFile) -> ReceiptResponse
    def standardize_items(self, items: List[Item]) -> List[Item]
```

### 3. **Factory Pattern**
```python
# AI service factory
class AIServiceFactory:
    @staticmethod
    def create_perplexity_client() -> PerplexityClient
    @staticmethod
    def create_kronos_client() -> KronosClient
```

### 4. **Dependency Injection**
```python
# FastAPI dependency injection
@app.post("/receipts/")
async def process_receipt(
    file: UploadFile = File(...),
    receipt_service: ReceiptService = Depends(get_receipt_service)
):
    return await receipt_service.process_receipt(file)
```

## 🗄️ Database Design

### Collections Structure

#### Users Collection
```json
{
  "_id": "ObjectId",
  "user": "string",
  "dietary_preference": "string",
  "spice_level": "string",
  "food_allergy": ["string"],
  "daily_calorie_target": "number",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Ingredients Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "quantity": "number",
  "unit": "string",
  "user": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Indexes
```javascript
// Users collection indexes
db.users.createIndex({ "user": 1 }, { unique: true })
db.users.createIndex({ "created_at": 1 })

// Ingredients collection indexes
db.ingredients.createIndex({ "user": 1 })
db.ingredients.createIndex({ "name": 1 })
db.ingredients.createIndex({ "user": 1, "name": 1 })
```

## 🤖 AI Integration

### Perplexity AI Integration
```python
class PerplexityClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
    
    async def process_receipt_image(self, image_data: str) -> dict:
        # Vision API call with structured output
        pass
```

### KronosLabs Integration
```python
class KronosClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = KronosLabs(api_key=api_key)
    
    async def generate_recipes(self, prompt: str) -> str:
        # Recipe generation with personalized prompts
        pass
```

### Data Standardization
```python
class ItemStandardizer:
    def __init__(self, inventory_file: str):
        self.inventory = self.load_inventory(inventory_file)
        self.threshold = int(os.getenv("STANDARDIZATION_THRESHOLD", "80"))
    
    def standardize_items(self, items: List[Item]) -> List[Item]:
        # Fuzzy string matching for item names
        pass
```

## 🔒 Security Architecture

### Input Validation
- **Pydantic Models**: Type-safe data validation
- **File Upload Validation**: MIME type and size checking
- **SQL Injection Prevention**: Parameterized queries (MongoDB)

### Environment Security
- **Environment Variables**: Sensitive data in `.env` files
- **API Key Management**: Secure storage and rotation
- **CORS Configuration**: Configurable cross-origin policies

### Error Handling
- **Structured Error Responses**: Consistent error format
- **Logging**: Comprehensive error logging
- **Rate Limiting**: (To be implemented in production)

## 📈 Scalability Considerations

### Horizontal Scaling
- **Stateless Design**: No server-side session storage
- **Load Balancer Ready**: Multiple instance deployment
- **Database Sharding**: MongoDB sharding capabilities

### Performance Optimization
- **Connection Pooling**: MongoDB connection management
- **Caching Strategy**: (Redis integration recommended)
- **Async Processing**: Non-blocking I/O operations

### Monitoring and Observability
- **Health Checks**: `/health` endpoint for monitoring
- **Metrics Collection**: (Prometheus integration recommended)
- **Logging**: Structured logging for debugging

## 🔮 Future Enhancements

### Microservices Migration
```
Current: Monolithic FastAPI Application
Future: 
├── Receipt Service
├── Recipe Service
├── User Service
└── API Gateway
```

### Additional Features
- **Authentication & Authorization**: JWT-based auth
- **Real-time Updates**: WebSocket support
- **File Storage**: Cloud storage integration
- **Caching Layer**: Redis implementation
- **Message Queue**: Celery for background tasks

### Infrastructure Improvements
- **Containerization**: Docker deployment
- **Orchestration**: Kubernetes management
- **CI/CD Pipeline**: Automated deployment
- **Monitoring**: APM and logging solutions
