from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import json
from typing import List, Dict, Any
from kronoslabs import KronosLabs
from database import get_collection

router = APIRouter()

# Get ingredients collection from centralized database connection (lazy loading)
def get_ingredients_collection():
    """Get ingredients collection from database."""
    return get_collection("ingredients")

# Initialize KronosLabs client only when needed
def get_kronos_client():
    """Get KronosLabs client instance."""
    api_key = os.getenv("KRONOSLABS_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="KRONOSLABS_API_KEY not configured")
    return KronosLabs(api_key=api_key)

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

class AllIngredient(BaseModel):
    name: str
    expiry: int
    category: str

class AllIngredientsResponse(BaseModel):
    ingredients: List[AllIngredient]
    total_count: int
    categories: List[str]

@router.get("/all-ingredients", response_model=AllIngredientsResponse)
def get_all_ingredients():
    """
    Get all available ingredients from the master ingredients database.
    
    Returns:
        AllIngredientsResponse: Complete list of all ingredients with metadata
    """
    try:
        # Get all ingredients collection from database
        all_ingredients_collection = get_collection("all_ingredients")
        
        # Fetch all ingredients from database
        ingredients_data = list(all_ingredients_collection.find({}))
        
        if not ingredients_data:
            raise HTTPException(
                status_code=404, 
                detail="No ingredients found in database"
            )
        
        # Convert to AllIngredient objects
        all_ingredients = [
            AllIngredient(
                name=item["name"],
                expiry=item["expiry"],
                category=item["category"]
            )
            for item in ingredients_data
        ]
        
        # Get unique categories
        categories = list(set(item["category"] for item in ingredients_data))
        categories.sort()  # Sort alphabetically
        
        return AllIngredientsResponse(
            ingredients=all_ingredients,
            total_count=len(all_ingredients),
            categories=categories
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving all ingredients from database: {str(e)}"
        )

@router.get("/{user}")
def get_recipes(user: str):
    ingredients_collection = get_ingredients_collection()
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

    kronosClient = get_kronos_client()
    response = kronosClient.chat.completions.create(
        prompt=prompt_text,
        model=os.getenv("KRONOSLABS_MODEL", "hermes"),
        temperature=float(os.getenv("KRONOSLABS_TEMPERATURE", "0.8")),
        is_stream=False
    )

    return {
        "ingredients": item_list,
        "recipes": response.choices[0].message.content
    }


@router.post("/ingredients/")
def add_ingredient(ingredient: Ingredient):
    try:
        ingredients_collection = get_ingredients_collection()
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
        ingredients_collection = get_ingredients_collection()
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
