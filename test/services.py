# File: tests/test_services.py

"""
Unit tests for the service layer.
This module contains tests for the business logic in the
'app/services' directory, ensuring functions work as expected
in isolation from the API endpoints.
"""

import pytest
import uuid
import datetime

# Import the service modules and their mock databases to test them directly.
# We need to import the modules themselves to access the mock databases.
from ..app.services import user_service
from ..app.services import post_service
from ..app.services import likes

# --- Fixtures ---
# Fixtures are functions that provide a consistent setup for your tests.
# The 'autouse=True' ensures that these fixtures run automatically before
# each test to reset the mock databases, ensuring tests are independent.

@pytest.fixture(autouse=True)
def reset_user_db():
    """Resets the mock user database before each test."""
    user_service.users_db.clear()

@pytest.fixture(autouse=True)
def reset_post_db():
    """Resets the mock post database before each test."""
    post_service.posts_db.clear()

@pytest.fixture(autouse=True)
def reset_likes_db():
    """Resets the mock likes database before each test."""
    likes.likes_db.clear()

# --- User Service Tests ---

def test_create_user():
    """Tests the create_user function."""
    user_data = user_service.UserCreate(username="testuser", password="password123")
    new_user = user_service.create_user(user_data)

    # Assert that the function returns a valid user object.
    assert isinstance(new_user, user_service.UserInDB)
    assert new_user.username == "testuser"
    assert new_user.hashed_password == "password123" # In a real app, this would be a hashed value.
    assert isinstance(new_user.id, str)

    # Assert that the new user exists in the mock database.
    assert new_user.username in user_service.users_db
    assert user_service.users_db[new_user.username].id == new_user.id

def test_get_user_by_username():
    """Tests retrieving a user by their username."""
    # First, create a user to ensure it's in the database.
    user_data = user_service.UserCreate(username="testuser", password="password123")
    created_user = user_service.create_user(user_data)

    # Retrieve the user and assert it matches the one we created.
    found_user = user_service.get_user_by_username("testuser")
    assert found_user is not None
    assert found_user.username == "testuser"
    assert found_user.id == created_user.id

def test_get_user_by_username_not_found():
    """Tests retrieving a non-existent user."""
    found_user = user_service.get_user_by_username("nonexistentuser")
    assert found_user is None

# --- Post Service Tests ---

def test_create_post():
    """Tests the create_post function."""
    # We need a user ID to associate with the post.
    user_id = str(uuid.uuid4())
    post_data = post_service.PostCreate(content="This is my first post!", user_id=user_id)
    new_post = post_service.create_post(post_data)

    # Assert that the function returns a valid post object.
    assert isinstance(new_post, post_service.PostInDB)
    assert new_post.content == "This is my first post!"
    assert new_post.user_id == user_id
    assert isinstance(new_post.id, str)
    assert isinstance(new_post.created_at, datetime.datetime)

    # Assert the new post exists in the mock database.
    assert new_post in post_service.posts_db

def test_get_posts_for_user():
    """Tests retrieving posts for a specific user."""
    user_id_1 = str(uuid.uuid4())
    user_id_2 = str(uuid.uuid4())

    # Create posts for different users.
    post_service.create_post(post_service.PostCreate(content="Post 1 by User 1", user_id=user_id_1))
    post_service.create_post(post_service.PostCreate(content="Post 2 by User 1", user_id=user_id_1))
    post_service.create_post(post_service.PostCreate(content="Post 1 by User 2", user_id=user_id_2))

    # Retrieve posts for User 1 and assert the count is correct.
    user_1_posts = post_service.get_posts_for_user(user_id_1)
    assert len(user_1_posts) == 2
    assert all(post.user_id == user_id_1 for post in user_1_posts)

def test_get_all_posts():
    """Tests retrieving all posts, sorted by creation date."""
    user_id = str(uuid.uuid4())

    # Create posts with slightly different creation times.
    post_1 = post_service.create_post(post_service.PostCreate(content="First post", user_id=user_id))
    post_2 = post_service.create_post(post_service.PostCreate(content="Second post", user_id=user_id))

    all_posts = post_service.get_all_posts()

    # Assert that the most recent post is at the beginning of the list.
    assert all_posts[0].content == "Second post"
    assert all_posts[1].content == "First post"
    assert len(all_posts) == 2

# --- Likes Service Tests ---

def test_like_post():
    """Tests adding a new like to a post."""
    post_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    # Assert that the like is successfully added.
    success = likes.like_post(post_id, user_id)
    assert success is True
    assert likes.get_post_likes_count(post_id) == 1
    assert user_id in likes.likes_db[post_id]

def test_like_post_already_liked():
    """Tests that a user cannot like a post more than once."""
    post_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    # First, like the post.
    likes.like_post(post_id, user_id)

    # Try to like it again and assert it returns False.
    success = likes.like_post(post_id, user_id)
    assert success is False
    assert likes.get_post_likes_count(post_id) == 1

def test_unlike_post():
    """Tests removing a like from a post."""
    post_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    # First, like the post so we can unlike it.
    likes.like_post(post_id, user_id)
    assert likes.get_post_likes_count(post_id) == 1

    # Now, unlike the post.
    success = likes.unlike_post(post_id, user_id)
    assert success is True
    assert likes.get_post_likes_count(post_id) == 0

def test_unlike_post_not_liked():
    """Tests unliking a post that the user has not liked."""
    post_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    # Try to unlike a post without liking it first.
    success = likes.unlike_post(post_id, user_id)
    assert success is False
    assert likes.get_post_likes_count(post_id) == 0

def test_get_user_likes():
    """Tests getting a list of posts a user has liked."""
    user_id = str(uuid.uuid4())
    post_id_1 = str(uuid.uuid4())
    post_id_2 = str(uuid.uuid4())

    # Like two posts with the same user.
    likes.like_post(post_id_1, user_id)
    likes.like_post(post_id_2, user_id)

    # Get the list of liked posts and assert it contains both IDs.
    user_liked_posts = likes.get_user_likes(user_id)
    assert len(user_liked_posts) == 2
    assert post_id_1 in user_liked_posts
    assert post_id_2 in user_liked_posts
    assert likes.get_post_likes_count(post_id_1) == 1
    assert likes.get_post_likes_count(post_id_2) == 1
    assert user_id in likes.likes_db[post_id_1]
    assert user_id in likes.likes_db[post_id_2]
    return [post_id for post_id, user_ids in likes.likes_db.items() if user_id in user_ids]

def test_get_post_likes_count_no_likes():
    """Tests getting the like count for a post with no likes."""
    post_id = str(uuid.uuid4())
    assert likes.get_post_likes_count(post_id) == 0

def test_has_user_liked_post():
    """Tests checking if a user has liked a specific post."""
    post_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    # Initially, the user has not liked the post.
    assert likes.has_user_liked_post(post_id, user_id) is False

    # Like the post.
    likes.like_post(post_id, user_id)

    # Now, the user should have liked the post.
    assert likes.has_user_liked_post(post_id, user_id) is True

    # Unlike the post.
    likes.unlike_post(post_id, user_id)

    # Finally, the user should not have liked the post anymore.
    assert likes.has_user_liked_post(post_id, user_id) is False
