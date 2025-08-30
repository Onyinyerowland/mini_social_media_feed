import pytest
from fastapi.testclient import TestClient

# Import the main FastAPI app and the in-memory database objects
from app.main import app
from app.database import users_db, posts_db, post_id_counter

# Define a fixture to provide a test client for all tests
# This is more efficient than creating a new client for every test
@pytest.fixture(scope="session")
def client():
    """Provides a TestClient instance for the API."""
    with TestClient(app) as test_client:
        yield test_client

# This fixture automatically runs before every test to reset the database
# This ensures each test starts with a clean slate and is independent
@pytest.fixture(autouse=True)
def reset_db():
    """Resets the in-memory database before each test."""
    users_db.clear()
    posts_db.clear()
    global post_id_counter
    post_id_counter = 0

# Example of a test function using the client fixture
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Mini Social Media API!"}
