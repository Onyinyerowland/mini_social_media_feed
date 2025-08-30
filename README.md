**Mini Social Media API**

A simple backend API for a social media application. This API allows users to register, create posts with optional images, list all posts, view a specific user's posts, and like posts.

**Features**
User Management: Register new users.

Post Creation: Create posts with a title, content, and an optional image upload.

Content Feed: Retrieve a list of all posts.

User Posts: Filter and view all posts by a specific user.

Engagement: Like a post and see the like count.

Password Hashing: Passwords are securely hashed using bcrypt before being stored.

**Project Structure**
The project is organized into a modular structure to keep the code clean and maintainable.

├── app/
│ ├── __init__.py
│ ├── main.py
│ ├── middleware.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ │ ├──__init__.py
│ │ ├── users.py
│ │ ├── posts.py
│ │ └── likes.py
│ ├── routers/
│ │ ├── __init__.py
│ │ ├── users.py
│ │ ├── posts.py
│ │ └── likes.py

**Prerequisites**
To run this project, you need to have Python 3.8+ installed.

**Dependencies**
The project relies on a few key Python libraries. You can install them using pip:

pip install fastapi "uvicorn[standard]" "passlib[bcrypt]" python-multipart

fastapi: The web framework used to build the API.

uvicorn: An ASGI server to run the FastAPI application.

passlib[bcrypt]: Used for securely hashing user passwords.

python-multipart: Required to handle form data, including file uploads.

**Installation and Setup**

Clone the Repository (if applicable) or create the project folder structure.

Navigate to the project directory.

Install the dependencies listed in the "Prerequisites" section.

Create the files as outlined in the "Project Structure" section and copy the provided code into each file.

**Running the Application**
To start the API server, run the following command from the project's root directory:

uvicorn app.main:app --reload

uvicorn app.main:app: This command tells Uvicorn to run the app instance from the main.py file inside the app directory.

--reload: This flag enables hot-reloading, so the server will automatically restart whenever you make code changes.

Once the server is running, you can access it at http://127.0.0.1:8000.

**API Endpoints**
You can interact with the API using any tool like Postman, cURL, or directly through the interactive documentation provided by FastAPI.

**Interactive Documentation**
Navigate to http://127.0.0.1:8000/docs in your web browser to view the Swagger UI, which provides a clean interface to test all the API endpoints.
