from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os

router = APIRouter()

# MongoDB connection
mongodb_uri = os.getenv("MONGODB_URI")
if not mongodb_uri:
    raise RuntimeError("MONGODB_URI not configured")

client = MongoClient(mongodb_uri, tls=True, tlsAllowInvalidCertificates=True)
db = client["cci_hackathon"]
ingredients_collection = db["ingredients"]

class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: str
    user: str

class IngredientResponse(BaseModel):
    id: str
    name: str
    quantity: float
    unit: str
    user: str

@router.get("/")
def get_recipes():
    return {
        "message": "Recipes retrieved successfully",
        "recipes": []
    }

@router.post("/ingredients/")
def add_ingredient(ingredient: Ingredient):
    try:
        # Insert ingredient into MongoDB
        result = ingredients_collection.insert_one(ingredient.dict())
        
        # Return the created ingredient with ID
        return {
            "id": str(result.inserted_id),
            "message": "Ingredient added successfully",
            **ingredient.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding ingredient: {str(e)}")

@router.get("/ingredients/{user}")
def get_ingredients_by_user(user: str):
    try:
        # Find all ingredients for the given user
        ingredients = list(ingredients_collection.find({"user": user}))
        
        # Convert ObjectId to string for JSON serialization
        for ingredient in ingredients:
            ingredient["id"] = str(ingredient["_id"])
            del ingredient["_id"]
            
        return {
            "user": user,
            "ingredients": ingredients,
            "count": len(ingredients)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving ingredients: {str(e)}")