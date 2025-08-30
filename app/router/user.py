import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from typing import Optional

# Import the models and database dependencies
from .. import models
from ..database import get_db

# Import the Pydantic schemas for request and response models
from ..schemas.user import UserCreate, User as UserSchema, Token

# Create a CryptContext instance for password hashing.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# A utility function to hash a password.
def get_password_hash(password):
    return pwd_context.hash(password)

# A utility function to verify a password.
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT settings
SECRET_KEY = "your-secret-key"  # Change this in a real app
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Create a new APIRouter instance.
router = APIRouter(prefix="/users", tags=["users"])

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticates a user by verifying their username and password.
    """
    # Find the user by their username.
    db_user = db.query(models.User).filter(models.User.username == form_data.username).first()

    # If no user is found, or the password doesn't match, raise an authentication error.
    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # If the credentials are valid, generate and return a JWT token.
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# This is the endpoint to create a user.
@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user in the database.
    """
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = get_password_hash(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        password_hash=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# This is the endpoint to get a user by their ID.
@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a user by their ID.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

# This is the endpoint to get all users.
@router.get("/", response_model=list[UserSchema])
def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieves all users from the database.
    """
    users = db.query(models.User).all()
    return users

# This is the endpoint to delete a user by their ID.
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletes a user by their ID.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(db_user)
    db.commit()
    return None

# This is the endpoint to update a user's information.
@router.put("/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    """
    Updates a user's information.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db_user.email = user.email
    db_user.password_hash = get_password_hash(user.password)  # Corrected to password_hash
    db_user.username = user.username
    db_user.full_name = user.full_name

    db.commit()
    db.refresh(db_user)
    return db_user
from ..security import get_current_active_user
@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    """
    Retrieves the currently authenticated user's information.
    """
    return current_user
