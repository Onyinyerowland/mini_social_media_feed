# The 'client' fixture is automatically provided by conftest.py
def test_read_root(client):
    """Test the root endpoint for a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Mini Social Media API!"}

def test_get_status(client):
    """Test the /status endpoint to ensure the API is running."""
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "API is running!"}
# Additional tests can be added here as needed
