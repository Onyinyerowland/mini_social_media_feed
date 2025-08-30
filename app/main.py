# app/main.py

import uvicorn
from fastapi import FastAPI

# Import routers and models
from app import models
from app.router import user, posts, likes

# Import database session
from app.database import engine

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI(
    title="Mini Social Media Feed",
    description="A simple social media feed API with user authentication, posts, and likes.",
    version="1.0.0",
)

# Include routers to add endpoints to the application
app.include_router(user.router)
app.include_router(posts.router)
app.include_router(likes.router)

# A simple "health check" endpoint
@app.get("/")
def read_root():
    """
    Root endpoint for the social media feed.
    """
    return {"message": "Welcome to the mini social media feed API!"}
   
