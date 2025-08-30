import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, security
from ..database import get_db
from ..schemas.posts import PostCreate, PostBase as PostSchema

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Creates a new post with the authenticated user as the author.
    """
    # Create the SQLAlchemy model instance with the authenticated username
    db_post = models.Post(
        title=post.title,
        content=post.content,
        image_path=post.image_path,
        username=current_user.username,
        published=post.published
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/{post_id}", response_model=PostSchema)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single post by its ID.
    """
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return db_post

@router.get("/", response_model=list[PostSchema])
def get_all_posts(db: Session = Depends(get_db)):
    """
    Retrieves all posts from the database.
    """
    posts = db.query(models.Post).all()
    return posts

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Deletes a post by its ID.
    """
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Check if the user is the owner of the post
    if db_post.username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this post"
        )

    db.delete(db_post)
    db.commit()
    return None

@router.put("/{post_id}", response_model=PostSchema)
def update_post(
    post_id: int,
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Updates a post by its ID.
    """
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Check if the user is the owner of the post
    if db_post.username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this post"
        )

    # Update the post fields
    db_post.title = post.title
    db_post.content = post.content
    db_post.image_path = post.image_path
    db_post.published = post.published
    db.commit()
    db.refresh(db_post)
    return db_post
@router.get("/user/{username}", response_model=list[PostSchema])
def get_posts_by_user(username: str, db: Session = Depends(get_db)):
    """
    Retrieves all posts made by a specific user.
    """
    posts = db.query(models.Post).filter(models.Post.username == username).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found for this user"
        )
    return posts
