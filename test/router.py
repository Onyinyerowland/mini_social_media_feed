import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import users_db

def test_register_user_success(client):
    """Test successful user registration."""
    user_data = {"username": "testuser", "password": "password123"}
    response = client.post("/users/", json=user_data)

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert "password" not in response.json()
    assert "testuser" in users_db

def test_register_existing_user_fails(client):
    """Test that registering an existing user returns a 400 error."""
    # First, register a user
    client.post("/users/", json={"username": "user1", "password": "password123"})

    # Then try to register the same user again
    response = client.post("/users/", json={"username": "user1", "password": "new_password"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_login_user_success(client):
    """Test successful user login."""
    # First, register a user
    client.post("/users/", json={"username": "loginuser", "password": "password123"})

    # Then attempt to log in
    response = client.post("/users/login", json={"username": "loginuser", "password": "password123"})

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"

def test_login_user_invalid_credentials(client):
    """Test login with invalid credentials."""
    # First, register a user
    client.post("/users/", json={"username": "invaliduser", "password": "password123"})

    # Then attempt to log in with wrong password
    response = client.post("/users/login", json={"username": "invaliduser", "password": "wrongpassword"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_login_nonexistent_user(client):
    """Test login with a username that does not exist."""
    response = client.post("/users/login", json={"username": "nonexistent", "password": "password123"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"

def test_register_user_missing_fields(client):
    """Test user registration with missing fields."""
    response = client.post("/users/", json={"username": "incompleteuser"})

    assert response.status_code == 422  # Unprocessable Entity due to validation error
    assert "detail" in response.json()

def test_register_user_empty_username(client):
    """Test user registration with an empty username."""
    response = client.post("/users/", json={"username": "", "password": "password123"})

    assert response.status_code == 422  # Unprocessable Entity due to validation error
    assert "detail" in response.json()

def test_register_user_empty_password(client):
    """Test user registration with an empty password."""
    response = client.post("/users/", json={"username": "userwithnopassword", "password": ""})

    assert response.status_code == 422  # Unprocessable Entity due to validation error
    assert "detail" in response.json()


def test_login_user_empty_username(client):
    """Test login with an empty username."""
    response = client.post("/users/login", json={"username": "", "password": "password123"})

    assert response.status_code == 422  # Unprocessable Entity due to validation error
    assert "detail" in response.json()

def test_login_user_empty_password(client):
    """Test login with an empty password."""
    response = client.post("/users/login", json={"username": "someuser", "password": ""})
    assert response.status_code == 422  # Unprocessable Entity due to validation error
    assert "detail" in response.json()


def test_register_user_special_characters(client):
    """Test user registration with special characters in username."""
    user_data = {"username":
                    "user!@#$%^&*()", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "user!@#$%^&*()"
    assert "password" not in response.json()
    assert "user!@#$%^&*()" in users_db

def test_register_user_long_username(client):
    """Test user registration with a very long username."""
    long_username = "u" * 300  # 300 characters long
    user_data = {"username": long_username, "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == long_username
    assert "password" not in response.json()
    assert long_username in users_db

def test_register_user_long_password(client):
    """Test user registration with a very long password."""
    long_password = "p" * 300  # 300 characters long
    user_data = {"username": "longpassworduser", "password": long_password}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "longpassworduser"
    assert "password" not in response.json()
    assert "longpassworduser" in users_db



    assert response.json()["username"] == "user'; DROP TABLE users;--"
    assert "password" not in response.json()
    assert "user'; DROP TABLE users;--" in users_db
def test_login_user_sql_injection(client):
    """Test login with SQL injection attempt in username."""
    # First, register a user
    client.post("/users/", json={"username": "sqluser", "password": "password123"})

    # Then attempt to log in with SQL injection in username
    response = client.post("/users/login", json={"username": "sqluser'; DROP TABLE users;--", "password": "password123"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"
def test_register_user_unicode_username(client):
    """Test user registration with Unicode characters in username."""
    user_data = {"username":
                    "用户", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "用户"
    assert "password" not in response.json()
    assert "用户" in users_db
def test_login_user_unicode_username(client):
    """Test login with Unicode characters in username."""
    # First, register a user
    client.post("/users/", json={"username": "用户", "password": "password123"})

    # Then attempt to log in
    response = client.post("/users/login", json={"username": "用户", "password": "password123"})

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
def test_register_user_numeric_username(client):
    """Test user registration with numeric username."""
    user_data = {"username": "123456", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "123456"
    assert "password" not in response.json()
    assert "123456" in users_db
def test_login_user_numeric_username(client):
    """Test login with numeric username."""
    # First, register a user
    client.post("/users/", json={"username": "123456", "password": "password123"})
    # Then attempt to log in
    response = client.post("/users/login", json={"username": "123456", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"





def test_like_post_success(client):
    """Test the POST /posts/{post_id}/like endpoint."""
    client.post("/users/", json={"username": "liker", "password": "123"})
    post_response = client.post("/posts/", data={"username": "liker", "title": "Like This", "content": "Please"})
    post_id = post_response.json()["post_id"]

    response = client.post(f"/posts/{post_id}/like")

    assert response.status_code == 200
    assert response.json()["message"] == f"Post {post_id} liked successfully"
    assert response.json()["likes"] == 1

def test_like_post_not_found(client):
    """Test that liking a non-existent post returns a 404 error."""
    response = client.post("/posts/999/like")

    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"




    def test_create_post_with_image(client):
        """Test the POST /posts/ endpoint with an image file upload."""
        client.post("/users/", json={"username": "poster", "password": "password123"})

        files = {"image": ("test.jpg", b"fake-image-data", "image/jpeg")}
        data = {
            "username": "poster",
            "title": "My First Post",
            "content": "This is a test post with a picture."
        }
        response = client.post("/posts/", data=data, files=files)

        assert response.status_code == 200
        post_data = response.json()
        assert post_data["username"] == "poster"
        assert "image_url" in post_data
        assert post_data["likes"] == 0

def test_create_post_without_image(client):
    """Test creating a post without an image."""
    client.post("/users/", json={"username": "poster_no_img", "password": "password123"})

    data = {
        "username": "poster_no_img",
        "title": "Post Without Image",
        "content": "Just some text."
    }
    response = client.post("/posts/", data=data)

    assert response.status_code == 200
    post_data = response.json()
    assert post_data["title"] == "Post Without Image"
    assert post_data["image_url"] is None

def test_list_all_posts(client):
    """Test the GET /posts/ endpoint."""
    client.post("/users/", json={"username": "alice", "password": "123"})
    client.post("/posts/", data={"username": "alice", "title": "Post A", "content": "Content A"})
    client.post("/users/", json={"username": "bob", "password": "456"})
    client.post("/posts/", data={"username": "bob", "title": "Post B", "content": "Content B"})

    response = client.get("/posts/")

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 2

def test_list_user_posts(client):
    """Test the GET /users/{username}/posts endpoint."""
    client.post("/users/", json={"username": "charlie", "password": "123"})
    client.post("/posts/", data={"username": "charlie", "title": "Charlie Post 1", "content": "First"})
    client.post("/posts/", data={"username": "charlie", "title": "Charlie Post 2", "content": "Second"})
    client.post("/users/", json={"username": "david", "password": "456"})
    client.post("/posts/", data={"username": "david", "title": "David Post 1", "content": "Third"})

    response = client.get("/users/charlie/posts")

    assert response.status_code == 200
    charlie_posts = response.json()
    assert len(charlie_posts) == 2
    assert all(post["username"] == "charlie" for post in charlie_posts)

def test_create_post_missing_fields(client):
    """Test creating a post with missing required fields."""
    client.post("/users/", json={"username": "incompleteposter", "password": "password123"})

    # Missing title
    data = {
        "username": "incompleteposter",
        "content": "This post has no title."
    }
    response = client.post("/posts/", data=data)
    assert response.status_code == 422  # Unprocessable Entity due to validation error

    # Missing content
    data = {
        "username": "incompleteposter",
        "title": "Title Only Post"
    }
    response = client.post("/posts/", data=data)
    assert response.status_code == 422  # Unprocessable Entity due to validation error

    # Missing username
    data = {
        "title": "No Username Post",
        "content": "This post has no username."
    }
    response = client.post("/posts/", data=data)
    assert response.status_code == 422  # Unprocessable Entity due to validation error
def test_create_post_invalid_user(client):
    """Test creating a post with a username that does not exist."""
    data = {
        "username": "nonexistentuser",
        "title": "Invalid User Post",
        "content": "This post should fail."
    }
    response = client.post("/posts/", data=data)
    assert response.status_code == 400  # Bad Request due to invalid username
    assert response.json()["detail"] == "User does not exist"

def test_create_post_empty_title(client):
    """Test creating a post with an empty title."""
    client.post("/users/", json={"username": "emptytitleuser", "password": "password123"})

    data = {
        "username": "emptytitleuser",
        "title": "",
        "content": "This post has an empty title."
    }
    response = client.post("/posts/", data=data)
    assert response.status_code == 422  # Unprocessable Entity due to validation error
    assert "detail" in response.json()

def test_create_post_empty_content(client):
    """Test creating a post with empty content."""
    client.post("/users/", json={"username": "emptycontentuser", "password": "password123"})

    data = {
        "username": "emptycontentuser",
        "title": "Title with Empty Content",
        "content": ""
    }
    response = client.post("/posts/", data=data)
    assert response.status_code == 422  # Unprocessable Entity due to validation error
    assert "detail" in response.json()

def test_create_post_invalid_image_type(client):
    """Test creating a post with an invalid image file type."""
    client.post("/users/", json={"username": "invalidimageuser", "password": "password123"})

    files = {"image": ("test.txt", b"not-an-image", "text/plain")}
    data = {
        "username": "invalidimageuser",
        "title": "Post with Invalid Image",
        "content": "This post has an invalid image file."
    }
    response = client.post("/posts/", data=data, files=files)

    assert response.status_code == 400  # Bad Request due to invalid image type
    assert response.json()["detail"] == "Invalid image type. Only JPEG and PNG are allowed."

def test_create_post_large_image(client):
    """Test creating a post with a large image file."""
    client.post("/users/", json={"username": "largeimageuser", "password": "password123"})

    # Simulate a large image file (e.g., 6MB)
    large_image_data = b"x" * (6 * 1024 * 1024)  # 6MB of dummy data
    files = {"image": ("large.jpg", large_image_data, "image/jpeg")}
    data = {
        "username": "largeimageuser",
        "title": "Post with Large Image",
        "content": "This post has a large image file."
    }
    response = client.post("/posts/", data=data, files=files)

    assert response.status_code == 400  # Bad Request due to image size limit
    assert response.json()["detail"] == "Image size exceeds the maximum limit of 5MB."

def test_create_post_special_characters_in_title(client):
    """Test creating a post with special characters in the title."""
    client.post("/users/", json={"username": "specialcharuser", "password": "password123"})

    data = {
        "username": "specialcharuser",
        "title": "Special!@#$%^&*()_+{}|:\"<>?`~[];',./",
        "content": "This post has special characters in the title."
    }
    response = client.post("/posts/", data=data)

    assert response.status_code == 200
    post_data = response.json()
    assert post_data["title"] == "Special!@#$%^&*()_+{}|:\"<>?`~[];',./"
    assert post_data["username"] == "specialcharuser"
    assert post_data["likes"] == 0

def test_create_post_long_title(client):
    """Test creating a post with a very long title."""
    client.post("/users/", json={"username": "longtitleuser", "password": "password123"})

    long_title = "L" * 300  # 300 characters long
    data = {
        "username": "longtitleuser",
        "title": long_title,
        "content": "This post has a very long title."
    }
    response = client.post("/posts/", data=data)

    assert response.status_code == 200
    post_data = response.json()
    assert post_data["title"] == long_title
    assert post_data["username"] == "longtitleuser"
    assert post_data["likes"] == 0

def test_create_post_long_content(client):
    """Test creating a post with very long content."""
    client.post("/users/", json={"username": "longcontentuser", "password": "password123"})

    long_content = "C" * 5000  # 5000 characters long
    data = {
        "username": "longcontentuser",
        "title": "Post with Long Content",
        "content": long_content
    }
    response = client.post("/posts/", data=data)

    assert response.status_code == 200
    post_data = response.json()
    assert post_data["content"] == long_content
    assert post_data["username"] == "longcontentuser"
    assert post_data["likes"] == 0

def test_create_post_special_characters_in_content(client):
    """Test creating a post with special characters in the content."""
    client.post("/users/", json={"username": "specialcharcontentuser", "password": "password123"})

    data= {
        "username": "specialcharcontentuser",
        "title": "Normal Title",
        "content": "Content with special characters !@#$%^&*()_+{}|:\"<>?`~[];',./"
    }
    response = client.post("/posts/", data=data)
    assert response.status_code == 200
    post_data = response.json()
    assert post_data["content"] == "Content with special characters !@#$%^&*()_+{}|:\"<>?`~[];',./"
    assert post_data["username"] == "specialcharcontentuser"
    assert post_data["likes"] == 0

def test_create_post_no_data(client):
    """Test creating a post with no data at all."""
    response = client.post("/posts/", data={})
    assert response.status_code == 422  # Unprocessable Entity due to validation error
    assert "detail" in response.json()

def test_create_post_extra_fields(client):
    """Test creating a post with extra unexpected fields."""
    client.post("/users/", json={"username": "extrafieldsuser", "password": "password123"})

    data = {
        "username": "extrafieldsuser",
        "title": "Post with Extra Fields",
        "content": "This post has extra fields.",
        "unexpected_field": "unexpected_value"
    }
    response = client.post("/posts/", data=data)
    assert response.status_code == 200
    post_data = response.json()
    assert post_data["title"] == "Post with Extra Fields"
    assert post_data["username"] == "extrafieldsuser"
    assert post_data["likes"] == 0
    assert "unexpected_field" not in post_data  # Ensure extra field is ignored
def test_create_post_special_characters_in_username(client):
    """Test creating a post with special characters in the username."""
    client.post("/users/", json={"username": "user!@#$", "password": "password123"})

    data = {
        "username": "user!@#$",
        "title": "Post by Special Char User",
        "content": "This post is created by a user with special characters in their username."
    }
    response = client.post("/posts/", data=data)

    assert response.status_code == 200
    post_data = response.json()
    assert post_data["username"] == "user!@#$"
    assert post_data["title"] == "Post by Special Char User"
    assert post_data["likes"] == 0
