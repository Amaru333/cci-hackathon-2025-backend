from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os
from kronoslabs import KronosLabs
from bson import ObjectId
from fastapi import Path

class CustomPrompt(BaseModel):
    user: str
    prompt: str

router = APIRouter()

kronosClient = KronosLabs(api_key=os.getenv("KRONOSLABS_API_KEY"))

# MongoDB connection
mongodb_uri = os.getenv("MONGODB_URI")
if not mongodb_uri:
    raise RuntimeError("MONGODB_URI not configured")

client = MongoClient(mongodb_uri, tls=True, tlsAllowInvalidCertificates=True)
db = client["cci_hackathon"]
ingredients_collection = db["ingredients"]
users_collection = db["users"]

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
    user_preference = users_collection.find_one({"user": user})
    if user_preference:
        user_preference = {
            "dietary_preference": user_preference["dietary_preference"],
            "spice_level": user_preference["spice_level"],
            "food_allergy": user_preference["food_allergy"],
            "daily_calorie_target": user_preference["daily_calorie_target"]
        }
    else:
        user_preference = {
            "dietary_preference": "vegetarian",
            "spice_level": "medium",
            "food_allergy": ["peanuts", "shellfish"],
            "daily_calorie_target": 2000
        }
    for item in item_list:
        item["id"] = str(item["_id"])
        del item["_id"]
    item_names = ", ".join([item["name"] for item in item_list])
    meal_preference = "breakfast"

    # 🧠 Enhanced Prompt
    prompt_text = f"""
You are an empathetic AI Chef who designs recipes tailored to the user’s ingredients and preferences.

### USER CONTEXT:
Available ingredients: {item_names}.
Meal type: {meal_preference}.
User preferences: {user_preference}.

### TASK:
Based on the given ingredients and preferences, suggest 2-3 creative, realistic, and delicious recipes.

Each recipe should include the following fields in JSON format:

- "recipe_name": A clear, creative, and appealing name for the dish.
- "calories": Total calories in the dish.
- "prep_time": Estimated preparation time in minutes.
- "cook_time": Estimated cooking time in minutes.
- "ingredients": List of ingredients with appropriate quantities.
- "steps": Step-by-step cooking instructions (concise and easy to follow).
- "feel_good_phrase": A short, moody phrase that emotionally connects to the user’s craving or setting 
  (e.g., "Perfect for cozy nights", "Bright and zesty for a fresh start", or "A comforting bowl after a long day").
- "preference_match": A one-line explanation of how the dish aligns with the user’s preferences 
  (e.g., vegetarian, spice level, calorie target, or allergy-safe).
- "youtube": {{
    "title": "An exact YouTube recipe video title that closely matches this recipe name and really exists",
    "url": "A real, working YouTube link to that recipe"
  }}

### REQUIREMENTS:
1. Ensure that each YouTube link you provide is real, existing, and relevant to the recipe title. 
   For example:
   - For "Rice & Beans Breakfast Bowl" → https://www.youtube.com/watch?v=RycCxY18zno
   - For "Garlic Butter Rice" → https://www.youtube.com/watch?v=8V8Z6EYYa2E
   - For "Spicy Veggie Stir Fry" → https://www.youtube.com/watch?v=5eLR0x4Cbn4
2. Recipes should feel natural and use the ingredients listed by the user where possible.
3. Keep the tone empathetic, warm, and encouraging — make the user feel inspired to cook.
4. Return only valid, structured JSON (no extra commentary or text outside the JSON).
5. Keep the total response concise — under 600 words.
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
    
@router.put("/ingredients/{id}")
def update_ingredient(
    id: str = Path(..., description="MongoDB ObjectId of the ingredient"),
    ingredient: Ingredient = None
):
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ingredient ID")

        # Only update non-null fields
        update_data = {k: v for k, v in ingredient.dict().items() if v is not None}

        result = ingredients_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Ingredient not found")

        # Retrieve updated ingredient
        updated = ingredients_collection.find_one({"_id": ObjectId(id)})
        updated["id"] = str(updated["_id"])
        del updated["_id"]

        return {
            "message": "Ingredient updated successfully",
            "ingredient": updated
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating ingredient: {str(e)}")

@router.delete("/ingredients/{id}")
def delete_ingredient(id: str = Path(..., description="MongoDB ObjectId of the ingredient")):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ingredient ID")

        result = ingredients_collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Ingredient not found")

        return {"message": f"Ingredient {id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting ingredient: {str(e)}")

@router.post("/custom-prompt")
def get_recipes(custom_prompt: CustomPrompt):
    item_list = list(ingredients_collection.find({"user": custom_prompt.user}))
    user_preference = users_collection.find_one({"user": custom_prompt.user})
    if user_preference:
        user_preference = {
            "dietary_preference": user_preference["dietary_preference"],
            "spice_level": user_preference["spice_level"],
            "food_allergy": user_preference["food_allergy"],
            "daily_calorie_target": user_preference["daily_calorie_target"]
        }
    else:
        user_preference = {
            "dietary_preference": "vegetarian",
            "spice_level": "medium",
            "food_allergy": ["peanuts", "shellfish"],
            "daily_calorie_target": 2000
        }
    for item in item_list:
        item["id"] = str(item["_id"])
        del item["_id"]
    item_names = ", ".join([item["name"] for item in item_list])
    meal_preference = "breakfast"

    # 🧠 Enhanced Prompt
    prompt_text = f"""
You are an empathetic AI Chef who designs recipes tailored to the user’s ingredients and preferences.

### USER CONTEXT:
Available ingredients: {item_names}.
Meal type: {meal_preference}.
User preferences: {user_preference}.

The user has provided the following custom prompt: {custom_prompt}.

### TASK:
Based on the given ingredients and preferences, suggest 2-3 creative, realistic, and delicious recipes.

Each recipe should include the following fields in JSON format:

- "recipe_name": A clear, creative, and appealing name for the dish.
- "calories": Total calories in the dish.
- "prep_time": Estimated preparation time in minutes.
- "cook_time": Estimated cooking time in minutes.
- "ingredients": List of ingredients with appropriate quantities.
- "steps": Step-by-step cooking instructions (concise and easy to follow).
- "feel_good_phrase": A short, moody phrase that emotionally connects to the user’s craving or setting 
  (e.g., "Perfect for cozy nights", "Bright and zesty for a fresh start", or "A comforting bowl after a long day").
- "preference_match": A one-line explanation of how the dish aligns with the user’s preferences 
  (e.g., vegetarian, spice level, calorie target, or allergy-safe).
- "youtube": {{
    "title": "An exact YouTube recipe video title that closely matches this recipe name and really exists",
    "url": "A real, working YouTube link to that recipe"
  }}

### REQUIREMENTS:
1. Ensure that each YouTube link you provide is real, existing, and relevant to the recipe title. 
   For example:
   - For "Rice & Beans Breakfast Bowl" → https://www.youtube.com/watch?v=RycCxY18zno
   - For "Garlic Butter Rice" → https://www.youtube.com/watch?v=8V8Z6EYYa2E
   - For "Spicy Veggie Stir Fry" → https://www.youtube.com/watch?v=5eLR0x4Cbn4
2. Recipes should feel natural and use the ingredients listed by the user where possible.
3. Keep the tone empathetic, warm, and encouraging — make the user feel inspired to cook.
4. Return only valid, structured JSON (no extra commentary or text outside the JSON).
5. Keep the total response concise — under 600 words.
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