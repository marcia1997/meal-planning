from pydantic import BaseModel
from typing import List, Optional, Dict

class UserPreferences(BaseModel):
    diet_type: Optional[str] = None
    allergies: Optional[List[str]] = []
    health_goals: Optional[str] = None

class User(BaseModel):
    username: str
    email: str
    password: str
    preferences: Optional[UserPreferences] = None

# Recipe Model
class Recipe(BaseModel):
    title: str
    ingredients: List[str]
    instructions: str
    owner: Optional[str] = None  # Username of creator

# Meal Plan Model
class MealPlan(BaseModel):
    user_id: str
    days: int
    meals: Dict[str, List[str]]  # Example: {"Monday": ["Breakfast Recipe", "Lunch Recipe"]}
