# app/database.py
# app/database.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from the .env file
load_dotenv()

# Get the database URL from the environment variable.
DATABASE_URL = os.getenv("DATABASE_URL")


# Raise an error if the database URL is not set, so you can catch it early.
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# Create the SQLAlchemy engine. Ensure you are not passing connect_args here.
# The `connect_args` parameter is used for SQLite, not PostgreSQL.
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class to handle database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the base class for your models.
Base = declarative_base()

# A utility function to get a database session and close it automatically.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def posts_db():
    pass
