# 👨‍💻 Development Guide

Complete guide for developers working on the CCI Hackathon 2025 Backend project.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Code Structure](#code-structure)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Debugging](#debugging)
- [Contributing](#contributing)
- [Code Review Process](#code-review-process)
- [Release Process](#release-process)

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- MongoDB (local or cloud)
- API keys for Perplexity AI and KronosLabs

### Initial Setup
```bash
# Clone the repository
git clone <repository-url>
cd cci-hackathon-2025-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Run the application
python main.py
```

## 🛠️ Development Environment

### IDE Setup

#### VS Code Configuration
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

#### VS Code Extensions
- Python
- Pylance
- Black Formatter
- Python Test Explorer
- REST Client

### Development Dependencies
```txt
# requirements-dev.txt
pytest==7.4.0
pytest-asyncio==0.21.1
pytest-cov==4.1.0
black==23.7.0
flake8==6.0.0
mypy==1.5.1
pre-commit==3.3.3
httpx==0.24.1
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-PyYAML]
```

Install pre-commit hooks:
```bash
pre-commit install
```

## 📁 Code Structure

```
cci-hackathon-2025-backend/
├── main.py                 # Application entry point
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── .pre-commit-config.yaml # Pre-commit configuration
├── constants/             # Static data files
│   └── items.json        # Food inventory database
├── routes/               # API route handlers
│   ├── __init__.py
│   ├── receipt.py       # Receipt processing endpoints
│   ├── recipe.py        # Recipe generation endpoints
│   └── user.py          # User management endpoints
├── utils/                # Utility functions
│   └── standardize.py   # Item name standardization
├── tests/                # Test files
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_receipt.py
│   ├── test_recipe.py
│   └── test_user.py
└── Documentation/        # Project documentation
    ├── API-Reference.md
    ├── Architecture.md
    ├── Configuration.md
    ├── Deployment.md
    ├── Development.md
    └── Troubleshooting.md
```

### File Organization Principles

1. **Single Responsibility**: Each file has one clear purpose
2. **Modular Design**: Related functionality grouped together
3. **Clear Naming**: File and function names describe their purpose
4. **Separation of Concerns**: Business logic separated from API routes

## 📝 Coding Standards

### Python Style Guide

#### PEP 8 Compliance
```python
# Good: Clear, descriptive variable names
user_dietary_preference = "vegetarian"
receipt_processing_result = await process_receipt(image_file)

# Bad: Unclear abbreviations
usr_diet = "vegetarian"
rec_res = await proc_rec(img)
```

#### Function Documentation
```python
def smart_standardize(receipt_items: list, threshold: int = None) -> list:
    """
    Map receipt item names to inventory names using fuzzy matching.
    
    Args:
        receipt_items (list): List of items from receipt processing
        threshold (int, optional): Matching threshold (0-100). Defaults to env var.
        
    Returns:
        list: Standardized items with normalized names
        
    Raises:
        ValueError: If threshold is outside valid range
        
    Example:
        >>> items = [{"name": "tomatoes", "price": 2.50}]
        >>> standardized = smart_standardize(items)
        >>> print(standardized[0]["name"])
        "Tomato"
    """
    if threshold is None:
        threshold = int(os.getenv("STANDARDIZATION_THRESHOLD", "80"))
    
    if not 0 <= threshold <= 100:
        raise ValueError("Threshold must be between 0 and 100")
    
    # Implementation...
    return standardized_items
```

#### Type Hints
```python
from typing import List, Dict, Optional, Union
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    quantity: int

async def process_receipt(
    file: UploadFile,
    user_id: Optional[str] = None
) -> Dict[str, Union[List[Item], float]]:
    """Process receipt with optional user context."""
    # Implementation...
    return {"items": items, "total": total}
```

### Error Handling

#### Structured Error Responses
```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def process_receipt(file: UploadFile):
    try:
        # Processing logic
        result = await extract_receipt_data(file)
        return result
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise HTTPException(
            status_code=400,
            detail="Receipt file not found"
        )
    except Exception as e:
        logger.error(f"Unexpected error processing receipt: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error processing receipt"
        )
```

#### Custom Exception Classes
```python
class ReceiptProcessingError(Exception):
    """Raised when receipt processing fails."""
    pass

class AIServiceError(Exception):
    """Raised when AI service calls fail."""
    pass

class DatabaseError(Exception):
    """Raised when database operations fail."""
    pass
```

### Logging Standards

#### Structured Logging
```python
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

def log_api_call(endpoint: str, user_id: str, duration: float, status: int):
    """Log API call with structured data."""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "user_id": user_id,
        "duration_ms": duration * 1000,
        "status_code": status,
        "level": "INFO"
    }
    logger.info(json.dumps(log_data))
```

## 🧪 Testing

### Test Structure
```python
# tests/test_receipt.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from main import app

client = TestClient(app)

class TestReceiptProcessing:
    """Test cases for receipt processing functionality."""
    
    @pytest.fixture
    def sample_receipt_file(self):
        """Create a sample receipt file for testing."""
        return ("receipt.jpg", b"fake_image_data", "image/jpeg")
    
    @patch('routes.receipt.requests.post')
    def test_process_receipt_success(self, mock_post, sample_receipt_file):
        """Test successful receipt processing."""
        # Mock AI response
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"items": [{"name": "Tomato", "price": 2.50, "quantity": 3}], "total": 7.50}'
                }
            }]
        }
        mock_post.return_value = mock_response
        
        # Test API call
        response = client.post(
            "/receipts/",
            files={"file": sample_receipt_file}
        )
        
        assert response.status_code == 200
        assert "items" in response.json()
        assert "total" in response.json()
    
    def test_process_receipt_invalid_file(self):
        """Test receipt processing with invalid file."""
        response = client.post(
            "/receipts/",
            files={"file": ("test.txt", b"not an image", "text/plain")}
        )
        
        assert response.status_code == 400
    
    @patch('routes.receipt.requests.post')
    def test_process_receipt_ai_error(self, mock_post, sample_receipt_file):
        """Test receipt processing with AI service error."""
        mock_post.side_effect = Exception("AI service unavailable")
        
        response = client.post(
            "/receipts/",
            files={"file": sample_receipt_file}
        )
        
        assert response.status_code == 500
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_receipt.py

# Run with verbose output
pytest -v

# Run tests in parallel
pytest -n auto
```

### Test Configuration
```python
# conftest.py
import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_db():
    """Create a test database connection."""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.test_cci_hackathon
    yield db
    # Cleanup
    await db.drop_collection("users")
    await db.drop_collection("ingredients")
    client.close()
```

## 🐛 Debugging

### Development Debugging

#### Debug Logging
```python
import logging

# Configure debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def process_receipt(file: UploadFile):
    logger.debug(f"Processing receipt: {file.filename}")
    
    # Debug AI service call
    logger.debug(f"Calling Perplexity API with model: {os.getenv('PERPLEXITY_MODEL')}")
    
    # Debug response
    logger.debug(f"AI response: {response.json()}")
```

#### VS Code Debug Configuration
```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

### Production Debugging

#### Health Check Endpoint
```python
@app.get("/health")
def health_check():
    """Comprehensive health check for debugging."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "services": {
            "mongodb": check_mongodb_connection(),
            "perplexity": check_perplexity_api(),
            "kronoslabs": check_kronoslabs_api()
        }
    }
    return health_status

def check_mongodb_connection():
    """Check MongoDB connection status."""
    try:
        client = MongoClient(os.getenv("MONGODB_URI"))
        client.admin.command('ping')
        return {"status": "healthy", "response_time_ms": 0}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

#### Error Tracking
```python
import traceback
import logging

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for debugging."""
    logger.error(f"Unhandled exception: {exc}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("ENVIRONMENT") == "development" else "An error occurred"
        }
    )
```

## 🤝 Contributing

### Development Workflow

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/cci-hackathon-2025-backend.git
   cd cci-hackathon-2025-backend
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-recipe-endpoint
   ```

3. **Make Changes**
   - Write code following coding standards
   - Add tests for new functionality
   - Update documentation if needed

4. **Run Tests and Linting**
   ```bash
   # Run pre-commit hooks
   pre-commit run --all-files
   
   # Run tests
   pytest
   
   # Check code formatting
   black --check .
   
   # Run type checking
   mypy .
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new recipe filtering endpoint"
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/new-recipe-endpoint
   ```

### Commit Message Convention

Use conventional commits format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build process or auxiliary tool changes

Examples:
```
feat(receipt): add support for PDF receipt processing
fix(recipe): resolve ingredient matching threshold issue
docs(api): update endpoint documentation
test(user): add unit tests for user creation
```

## 👥 Code Review Process

### Review Checklist

#### Functionality
- [ ] Code works as intended
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] Performance is acceptable

#### Code Quality
- [ ] Code follows style guidelines
- [ ] Functions are well-documented
- [ ] Variable names are descriptive
- [ ] No code duplication

#### Testing
- [ ] Tests cover new functionality
- [ ] Tests pass
- [ ] Test coverage is maintained
- [ ] Integration tests are included

#### Security
- [ ] No sensitive data in code
- [ ] Input validation is present
- [ ] No security vulnerabilities
- [ ] API endpoints are properly secured

### Review Process
1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Peer Review**: At least one team member reviews the code
3. **Testing**: Reviewer tests the functionality
4. **Approval**: Code is approved and merged

## 🚀 Release Process

### Version Management
```python
# main.py
__version__ = "1.2.0"

app = FastAPI(
    title="CCI Hackathon 2025 Backend",
    version=__version__,
    description="A food management and recipe recommendation system"
)
```

### Release Steps

1. **Update Version**
   ```bash
   # Update version in main.py
   # Update CHANGELOG.md
   git add .
   git commit -m "chore: bump version to 1.2.0"
   ```

2. **Create Release Tag**
   ```bash
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

3. **Deploy to Production**
   ```bash
   # Deploy using your preferred method
   docker build -t cci-hackathon-backend:v1.2.0 .
   docker push your-registry/cci-hackathon-backend:v1.2.0
   ```

4. **Update Documentation**
   - Update API documentation
   - Update deployment guides
   - Create release notes

### Changelog Format
```markdown
# Changelog

## [1.2.0] - 2024-01-15

### Added
- New recipe filtering endpoint
- Support for PDF receipt processing
- Enhanced error logging

### Changed
- Improved ingredient matching algorithm
- Updated API response format

### Fixed
- Fixed memory leak in receipt processing
- Resolved CORS issues with mobile clients

### Security
- Added input validation for file uploads
- Implemented rate limiting
```

## 📚 Additional Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)

### Tools
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [MyPy Type Checker](https://mypy.readthedocs.io/)
- [Pre-commit Hooks](https://pre-commit.com/)

### Best Practices
- [Python Best Practices](https://docs.python-guide.org/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [API Design Best Practices](https://restfulapi.net/)
- [Testing Best Practices](https://docs.python.org/3/library/unittest.html)
