from pydantic import BaseModel
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from database import recipes_collection  # Connect to MongoDB
from bson import ObjectId


router = APIRouter()

class Recipe(BaseModel):
    title: str
    ingredients: List[str]
    instructions: str
    owner: Optional[str] = None  # Will store the username of the creator

# Create a new recipe
@router.post("/recipes")
async def create_recipe(recipe: Recipe):
    recipe_dict = recipe.dict()
    new_recipe = recipes_collection.insert_one(recipe_dict)
    return {"id": str(new_recipe.inserted_id), "message": "Recipe added successfully"}

# Get all recipes
@router.get("/recipes")
async def get_recipes():
    recipes = []
    for recipe in recipes_collection.find():
        recipes.append({**recipe, "_id": str(recipe["_id"])})  # Convert ObjectId to string
    return recipes

# Get a single recipe by ID
@router.get("/recipes/{id}")
async def get_recipe(id: str):
    recipe = recipes_collection.find_one({"_id": ObjectId(id)})
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {**recipe, "_id": str(recipe["_id"])}  # Convert ObjectId to string

# Update a recipe by ID
@router.put("/recipes/{id}")
async def update_recipe(id: str, recipe_data: Recipe):
    updated_recipe = recipes_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": recipe_data.dict()}
    )
    if updated_recipe.matched_count == 0:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe updated successfully"}

# Delete a recipe by ID
@router.delete("/recipes/{id}")
async def delete_recipe(id: str):
    deleted_recipe = recipes_collection.delete_one({"_id": ObjectId(id)})
    if deleted_recipe.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"}
