from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class RecipeRequest(BaseModel):
    data: str

@router.get("/")
def get_recipes():
    return {
        "message": "Recipes retrieved successfully",
        "recipes": []
    }