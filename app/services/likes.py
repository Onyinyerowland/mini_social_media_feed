# File: app/services/likes.py
"""
Service layer for managing likes on posts.
This module handles the core business logic for liking and unliking a post,
as well as retrieving like counts.
"""
from typing import Dict, List, Set

# Mock database for likes.
# This dictionary maps a post_id to a set of user_ids who have liked that post.
# Using a 'set' is efficient for adding and removing likes and for checking if a user has already liked a post.
likes_db: Dict[str, Set[str]] = {}

def like_post(post_id: str, user_id: str) -> bool:
    """
    Adds a like from a user to a specific post.

    Args:
        post_id (str): The unique ID of the post being liked.
        user_id (str): The unique ID of the user who is liking the post.

    Returns:
        bool: True if the like was successfully added, False if the user has already liked the post.
    """
    if post_id not in likes_db:
        # If the post hasn't been liked before, create a new entry for it.
        likes_db[post_id] = set()

    # Check if the user has already liked the post.
    if user_id in likes_db[post_id]:
        return False  # The user has already liked this post.

    likes_db[post_id].add(user_id)
    return True

def unlike_post(post_id: str, user_id: str) -> bool:
    """
    Removes a like from a user on a specific post.

    Args:
        post_id (str): The unique ID of the post being unliked.
        user_id (str): The unique ID of the user who is unliking the post.

    Returns:
        bool: True if the like was successfully removed, False if the like didn't exist.
    """
    # Check if the post has any likes and if the user has liked it.
    if post_id in likes_db and user_id in likes_db[post_id]:
        likes_db[post_id].remove(user_id)
        # Optional: Clean up the dictionary if the set of likes becomes empty.
        if not likes_db[post_id]:
            del likes_db[post_id]
        return True

    return False # The like didn't exist, so nothing was removed.

def get_post_likes_count(post_id: str) -> int:
    """
    Returns the total number of likes for a specific post.

    Args:
        post_id (str): The unique ID of the post.

    Returns:
        int: The number of likes for the post.
    """
    # Return the size of the set. If the post ID doesn't exist, the count is 0.
    return len(likes_db.get(post_id, set()))

def get_user_likes(user_id: str) -> List[str]:
    """
    Returns a list of post IDs that a specific user has liked.

    Args:
        user_id (str): The unique ID of the user.

    Returns:
        List[str]: A list of post IDs liked by the user.
    """
    liked_posts = []
    for post_id, likers in likes_db.items():
        if user_id in likers:
            liked_posts.append(post_id)
    return liked_posts
def has_user_liked_post(post_id: str, user_id: str) -> bool:
    """
    Checks if a specific user has liked a specific post.
    Args:
        post_id (str): The unique ID of the post.
        user_id (str): The unique ID of the user.
    Returns:
        bool: True if the user has liked the post, False otherwise.
    """
    return user_id in likes_db.get(post_id, set())
