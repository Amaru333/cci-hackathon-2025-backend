from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os
from kronoslabs import KronosLabs

router = APIRouter()

kronosClient = KronosLabs(api_key=os.getenv("KRONOSLABS_API_KEY"))

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

@router.get("/{user}")
def get_recipes(user: str):
    item_list = list(ingredients_collection.find({"user": user}))
    for item in item_list:
        item["id"] = str(item["_id"])
        del item["_id"]
    item_names = ", ".join([item["name"] for item in item_list])
    user_preference = {"dietary_preference": "vegetarian",
  "spice_level": "medium",
  "food_allergy": ["peanuts", "shellfish"],
  "daily_calorie_target": { "$numberDouble": "2000.0" }
}
    response = kronosClient.chat.completions.create(
    prompt="You are an AI recipe assistant. Based on the following ingredients: " + item_names +
    ", and user preferences: " + str(user_preference) +
    ", suggest a list of recipes that can be made. Provide detailed recipe instructions including ingredients, quantities, and steps.",
    model="hermes",
    temperature=0.7,
    is_stream=False
)
    return {
        "ingredients": item_list,
        "recipes": response.choices[0].message.content
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