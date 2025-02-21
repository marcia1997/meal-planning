from fastapi import FastAPI
from app.routes import auth

app = FastAPI()

# Include authentication routes
app.include_router(auth.router, prefix="/auth")

@app.get("/")
def home():
    return {"message": "Healthy Meal Planner API is running!"}
