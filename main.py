from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes.receipt import router as receipt_router
from routes.recipe import router as recipe_router
from routes.user import router as user_router

# Initialize FastAPI app
app = FastAPI(
    title="My API",
    description="A base FastAPI application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    return {"status": "healthy"}

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)