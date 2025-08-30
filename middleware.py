from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Depends


# Import get_db from the appropriate module
# Update the import path below to the correct location of get_db if different
from .app.database import get_db  # If db.py is in the same package/folder as this file


app = FastAPI(title="Mini Social Media Feed API", version="1.0.0")
# router(router)  # Removed because 'router' is not defined; add your routers here if needed
app.dependency_overrides[Depends(get_db)] = get_db


app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


# Ensure uploads directory exists
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


# Mount static file serving for uploaded images
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")
