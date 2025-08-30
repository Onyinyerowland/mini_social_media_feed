import pytest
from pydantic import ValidationError
from app.schemas import UserCreate, UserResponse

def test_user_create_valid_data():
    """
    Test that the UserCreate schema correctly validates valid input data.
    """
    valid_user_data = {
        "username": "johndoe",
        "password": "strongpassword123"
    }

    # Try to create a UserCreate instance with valid data.
    # If this succeeds, it means the schema works as expected.
    user = UserCreate(**valid_user_data)

    # Assert that the attributes are correctly assigned
    assert user.username == "johndoe"
    assert user.password == "strongpassword123"

def test_user_create_missing_fields_fails():
    """
    Test that the UserCreate schema raises a ValidationError for missing fields.
    """
    invalid_user_data = {
        "username": "janedoe"
        # 'password' is missing
    }

    # Use a pytest context manager to check if ValidationError is raised
    with pytest.raises(ValidationError):
        UserCreate(**invalid_user_data)

def test_user_create_extra_fields_ignored():
    """
    Test that the UserCreate schema ignores extra fields by default.
    Pydantic's default behavior is to ignore extra data, so this test ensures that
    the schema behaves as expected.
    """
    extra_data = {
        "username": "extratest",
        "password": "securepassword",
        "email": "test@example.com" # This is an extra field
    }

    # The schema should validate successfully without an error
    user = UserCreate(**extra_data)

    # Assert that the extra field is not part of the model instance
    assert user.username == "extratest"
    assert not hasattr(user, 'email')

def test_user_response_valid_data():
    """
    Test that the UserResponse schema correctly validates valid input data.
    """
    valid_response_data = {
        "username": "userresponse"
    }

    # Try to create a UserResponse instance with valid data
    user_response = UserResponse(**valid_response_data)

    assert user_response.username == "userresponse"

def test_user_response_password_not_included():
    """
    Test that the UserResponse schema does not include a password field,
    even if it's provided, as it is designed for a secure response.
    """
    # This data is what might be passed accidentally
    invalid_response_data = {
        "username": "testuser",
        "password": "leakedpassword"
    }

    # The schema should validate successfully, but the password should be ignored
    user_response = UserResponse(**invalid_response_data)
