from typing import Dict, List
import datetime
import uuid

# In a real application, these models would be imported from a 'schemas' directory.
# We'll define them here for this example.
class PostCreate:
    def __init__(self, content: str, user_id: str):
        self.content = content
        self.user_id = user_id

class PostInDB:
    def __init__(self, id: str, content: str, user_id: str, created_at: datetime.datetime):
        self.id = id
        self.content = content
        self.user_id = user_id
        self.created_at = created_at

# This is a mock database for posts. It stores a list of post objects.
posts_db: List[PostInDB] = []

def create_post(post_data: PostCreate) -> PostInDB:
    """
    Creates a new post and adds it to the mock database.
    """
    new_post = PostInDB(
        id=str(uuid.uuid4()),
        content=post_data.content,
        user_id=post_data.user_id,
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )
    posts_db.append(new_post)
    return new_post

def get_posts_for_user(user_id: str) -> List[PostInDB]:
    """
    Retrieves all posts created by a specific user from the mock database.
    """
    return [post for post in posts_db if post.user_id == user_id]

def get_all_posts() -> List[PostInDB]:
    """
    Retrieves all posts from the mock database, sorted by creation date.
    """
    # Sort posts by creation date, from newest to oldest.
    return sorted(posts_db, key=lambda post: post.created_at, reverse=True)
