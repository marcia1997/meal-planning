from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, preferences, recipes

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the auth routes with the "/auth" prefix
app.include_router(auth.router, prefix="/auth")

# Include other routes
app.include_router(preferences.router, prefix="/preferences")
app.include_router(recipes.router, prefix="/recipes")

# Health check route
@app.get("/")
def home():
    return {"message": "Healthy Meal Planner API is running!"}
