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

    user_preference = {
        "dietary_preference": "vegetarian",
        "spice_level": "medium",
        "food_allergy": ["peanuts", "shellfish"],
        "daily_calorie_target": 2000
    }
    meal_preference = "breakfast"

    # 🧠 Enhanced Prompt
    prompt_text = f"""
You are an empathetic AI Chef who designs recipes tailored to the user’s ingredients and preferences.

### USER CONTEXT:
Available ingredients: {item_names}.
Meal type: {meal_preference}.
User preferences: {user_preference}.

### TASK:
1. Suggest 2-3 recipes that can be prepared using the given ingredients.
2. Each recipe should include:
   - "recipe_name": A creative and catchy title.
   - "prep_time": Estimated preparation time (in minutes).
   - "cook_time": Estimated cooking time (in minutes).
   - "ingredients": List of ingredients with quantities.
   - "steps": Step-by-step cooking instructions.
   - "feel_good_phrase": A short moody phrase that makes the user feel happy, cozy, or inspired to cook (e.g., "Perfect for a rainy morning" or "A cozy bowl that feels like home").
   - "preference_match": Brief explanation of how this dish aligns with the user's preferences (diet, spice, allergy, calorie target).
   - "youtube": A real or close-matching YouTube recipe suggestion — return a JSON object:
        {{
          "title": "Exact YouTube video title (short and descriptive)",
          "url": "https://www.youtube.com/..."
        }}
3. Make sure the JSON output is clean, properly formatted, and human-readable.
4. Keep total response under 600 words.
"""

    response = kronosClient.chat.completions.create(
        prompt=prompt_text,
        model="hermes",
        temperature=0.8,
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
    
# Same as above but post array of ingredients
@router.post("/ingredients/batch/")
def add_ingredients_batch(ingredients: list[Ingredient]):
    try:
        # Insert multiple ingredients into MongoDB
        ingredient_dicts = [ingredient.dict() for ingredient in ingredients]
        result = ingredients_collection.insert_many(ingredient_dicts)
        
        # Return the created ingredients with IDs
        return {
            "ids": [str(id) for id in result.inserted_ids],
            "message": "Ingredients added successfully",
            "count": len(result.inserted_ids)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding ingredients: {str(e)}")

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