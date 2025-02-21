from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

# Secret key for signing JWT tokens
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

# Password encryption configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Temporary in-memory user database (to be replaced with MongoDB later)
fake_users_db = {}

# User model for registration and login
class User(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Function to hash passwords
def hash_password(password: str):
    return pwd_context.hash(password)

# Function to verify passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to generate JWT tokens
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# User registration
@router.post("/register")
async def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already registered")
    
    fake_users_db[user.username] = {
        "email": user.email,
        "password": hash_password(user.password),
    }
    return {"message": "User registered successfully"}

# User login and JWT token generation
@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    print("Fake users DB:", fake_users_db)  # Debugging: check database
    print("User trying to log in:", user.username)
    
    db_user = fake_users_db.get(user.username)
    if not db_user:
        print("User not found")  # Debugging: user does not exist
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    print("Stored hash:", db_user["password"])
    
    print("Verification result:", verify_password(user.password, db_user["password"]))
    
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
