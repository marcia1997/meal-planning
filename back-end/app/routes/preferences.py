from fastapi import APIRouter, Depends, HTTPException
from database import users_collection
from app.models import UserPreferences
from bson import ObjectId
from auth import get_current_user

router = APIRouter()

@router.put("/users/preferences")
async def update_preferences(preferences: UserPreferences, current_user: dict = Depends(get_current_user)):
    """ Update user preferences in the database """
    
    user_id = current_user["_id"]
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"preferences": preferences.dict()}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Preferences updated successfully"}
