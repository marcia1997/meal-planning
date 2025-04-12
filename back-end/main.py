from fastapi import FastAPI
from app.routes import auth, recipes ,preferences

app = FastAPI()

# Include authentication routes
app.include_router(auth.router, prefix="/auth") 
app.include_router(preferences.router, prefix="/preferences")
app.include_router(recipes.router)


@app.get("/")
def home():
    return {"message": "Healthy Meal Planner API is running!"}
