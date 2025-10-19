from dotenv import load_dotenv
import os
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes.receipt import router as receipt_router
from routes.recipe import router as recipe_router
from routes.user import router as user_router
from database import database_lifespan

# Initialize FastAPI app with database lifespan management
app = FastAPI(
    title=os.getenv("APP_TITLE", "CCI Hackathon 2025 Backend"),
    description=os.getenv("APP_DESCRIPTION", "A food management and recipe recommendation system"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    lifespan=database_lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "*")],
    allow_credentials=os.getenv("CORS_CREDENTIALS", "true").lower() == "true",
    allow_methods=[os.getenv("CORS_METHODS", "*")],
    allow_headers=[os.getenv("CORS_HEADERS", "*")],
)

# Include routers
app.include_router(receipt_router, prefix="/receipts", tags=["receipts"])
app.include_router(recipe_router, prefix="/recipes", tags=["recipes"])
app.include_router(user_router, prefix="/users", tags=["users"])

# Health check routes
@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/health")
def health_check():
    from database import db_manager
    db_health = db_manager.health_check()
    
    return {
        "status": "healthy" if db_health["status"] == "healthy" else "degraded",
        "timestamp": "2024-01-01T00:00:00Z",  # You can add datetime import
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "database": db_health
    }

# Run the app
if __name__ == "__main__":
    uvicorn.run(
        app, 
        host=os.getenv("HOST", "0.0.0.0"), 
        port=int(os.getenv("PORT", 8000))
    )