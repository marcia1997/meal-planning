from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from database import users_collection

# Secret key for signing JWT tokens
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

# OAuth2 scheme for extracting token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Password encryption configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

# Function to get the current user from the token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """ Extract user from JWT token """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = users_collection.find_one({"username": username})
    if user is None:
        raise credentials_exception

    return user

# User registration
@router.post("/register")
async def register(user: User):
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    user_dict = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password)
    }
    users_collection.insert_one(user_dict)
    return {"message": "User registered successfully"}

# User login and JWT token generation
@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
