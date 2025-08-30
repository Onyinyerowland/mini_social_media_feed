from typing import Dict, List, Optional
import uuid
from schemas import UserCreate, UserInDB


# This is a mock database. In a real application, you would use
# a database like PostgreSQL, MySQL, or MongoDB, and an ORM like SQLAlchemy.
# The `users_db` dictionary maps usernames to user objects.
users_db: Dict[str, UserInDB] = {}

def create_user(user_data: UserCreate) -> UserInDB:
    """
    Creates a new user and adds them to the mock database.
    In a real app, this would involve hashing the password and saving to a database.
    """
    # Generate a unique ID for the new user.
    user_id = str(uuid.uuid4())
    # In a real scenario, you'd hash the password here.
    hashed_password = user_data.password  # Placeholder for real password hashing.

    new_user = UserInDB(
        id=user_id,
        username=user_data.username,
        hashed_password=hashed_password
    )
    users_db[new_user.username] = new_user
    return new_user

def get_user_by_username(username: str) -> Optional[UserInDB]:
    """
    Retrieves a user from the mock database by their username.
    """
    return users_db.get(username)

def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    """
    Retrieves a user from the mock database by their ID.
    """
    # A simple search through the values of our mock database.
    for user in users_db.values():
        if user.id == user_id:
            return user
    return None

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """
    Authenticates a user by their username and password.
    In a real app, this would involve checking the hashed password.
    """
    user = get_user_by_username(username)
    if user and user.hashed_password == password:  # Placeholder for real password check.
        return user
    return None
def get_all_users() -> List[UserInDB]:
    """
    Retrieves all users from the mock database.
    """
    return list(users_db.values())
def delete_user(username: str) -> bool:
    """
    Deletes a user from the mock database by their username.
    Returns True if the user was deleted, False if the user was not found.
    """
    if username in users_db:
        del users_db[username]
        return True
    return False
def update_user(username: str, new_data: Dict[str, str]) -> Optional[UserInDB]:
    """
    Updates a user's information in the mock database.
    """
    user = get_user_by_username(username)
    if not user:
        return None
    if "password" in new_data:
        user.hashed_password = new_data["password"]  # Placeholder for real password hashing.
    # Add more fields as necessary.
    return user
def reset_users_db():
    """
    Resets the mock users database.
    """
    global users_db
    users_db = {}
