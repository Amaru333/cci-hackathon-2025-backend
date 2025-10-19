from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from typing import List
from database import get_collection

router = APIRouter()

# Get users collection from centralized database connection (lazy loading)
def get_users_collection():
    """Get users collection from database."""
    return get_collection("users")

class User(BaseModel):
    user: str
    dietary_preference: str
    spice_level: str
    food_allergy: List[str]
    daily_calorie_target: float

class UserResponse(BaseModel):
    id: str
    user: str
    dietary_preference: str
    spice_level: str
    food_allergy: List[str]
    daily_calorie_target: float

@router.post("/")
def create_user(user_data: User):
    try:
        users_collection = get_users_collection()
        # Check if user already exists
        existing_user = users_collection.find_one({"user": user_data.user})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Insert user into MongoDB
        result = users_collection.insert_one(user_data.dict())
        
        # Return the created user with ID
        return {
            "id": str(result.inserted_id),
            "message": "User created successfully",
            **user_data.dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@router.get("/{user}")
def get_user(user: str):
    try:
        users_collection = get_users_collection()
        # Find user by username
        user_data = users_collection.find_one({"user": user})
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Convert ObjectId to string
        user_data["id"] = str(user_data["_id"])
        del user_data["_id"]
        
        return user_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {str(e)}")