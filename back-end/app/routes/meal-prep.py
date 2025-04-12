from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user
from database import mealplans_collection, recipes_collection, users_collection
import openai
import os

router = APIRouter()

openai.api_key = "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"




@router.post("/generate-meal-plan")
async def generate_meal_plan(days: int = 7, current_user: dict = Depends(get_current_user)):
    """ Generate a meal plan considering user preferences """

    user = users_collection.find_one({"_id": current_user["_id"]})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get user preferences
    preferences = user.get("preferences", {})
    dietary_restrictions = preferences.get("dietary_restrictions", "No restrictions")
    allergies = preferences.get("allergies", "No allergies")

    # Get recipes that match user preferences
    recipes = list(recipes_collection.find())

    filtered_recipes = [
        recipe for recipe in recipes
        if not any(allergy.lower() in recipe["ingredients"] for allergy in allergies.split(","))
        and dietary_restrictions.lower() in recipe.get("tags", "").lower()
    ]

    if not filtered_recipes:
        raise HTTPException(status_code=404, detail="No suitable recipes found")

    # Generate meal plan
    meal_plan = {}
    
    for i in range(days):
        day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][i % 7]
        
        prompt = f"""
        Create a meal plan for {day_name} using only these recipes: {', '.join([r['title'] for r in filtered_recipes])}.
        Make sure they align with the dietary restrictions: {dietary_restrictions} and avoid these allergens: {allergies}.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )

        generated_meals = response["choices"][0]["message"]["content"].split("\n")
        meal_plan[day_name] = generated_meals

    # Store meal plan in MongoDB
    mealplan_doc = {"user_id": current_user["_id"], "days": days, "meals": meal_plan}
    mealplans_collection.insert_one(mealplan_doc)

    return {"message": "Meal plan generated successfully", "meal_plan": meal_plan}
