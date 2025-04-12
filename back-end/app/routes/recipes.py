from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, HTTPException
from database import recipes_collection  # Connect to MongoDB
from bson import ObjectId
import openai  # Import OpenAI
import os

router = APIRouter()


openai.api_key = os.getenv("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") 

# Recipe Model
class Recipe(BaseModel):
    title: str
    ingredients: List[str]
    instructions: str
    generated_by: str = "AI"  # Ensure all recipes are AI-generated

# Function to generate a recipe using OpenAI API
def generate_recipe(prompt: str):
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI chef."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Generate a recipe using AI
@router.post("/generate-recipe")
async def create_recipe(user_preferences: dict):
    """ Generate a recipe based on user preferences """
    
    prompt = f"Generate a healthy recipe considering these preferences: {user_preferences}"
    ai_recipe = generate_recipe(prompt)
    
    recipe_data = {
        "title": "AI Generated Recipe",
        "ingredients": ["Generated ingredient 1", "Generated ingredient 2"],
        "instructions": ai_recipe,
        "generated_by": "AI"
    }
    
    new_recipe = recipes_collection.insert_one(recipe_data)
    return {"id": str(new_recipe.inserted_id), "recipe": recipe_data}

# Get all AI-generated recipes
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
    return {**recipe, "_id": str(recipe["_id"])}

# Delete a recipe by ID
@router.delete("/recipes/{id}")
async def delete_recipe(id: str):
    deleted_recipe = recipes_collection.delete_one({"_id": ObjectId(id)})
    if deleted_recipe.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"}
