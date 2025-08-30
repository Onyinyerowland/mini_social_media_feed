from fastapi import APIRouter, HTTPException,status, Depends
from app.database import posts_db
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..schemas import likes as likes_schema
from ..security import get_current_user

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(
    like: likes_schema.LikeCreate,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user),
):
    # Check if the post exists
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if the user has already liked the post
    existing_like = db.query(models.Like).filter(
        models.Like.post_id == like.post_id,
        models.Like.username == current_user_username,
    ).first()

    if existing_like:
        raise HTTPException(status_code=409, detail="User has already liked this post")

    # Create the like
    new_like = models.Like(
        post_id=like.post_id,
        username=current_user_username,
    )
    db.add(new_like)
    db.commit()
    return {"message": "Post liked successfully"}

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post(
    like: likes_schema.LikeCreate,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user),
):
    # Find the like
    like_to_delete = db.query(models.Like).filter(
        models.Like.post_id == like.post_id,
        models.Like.username == current_user_username,
    ).first()

    if not like_to_delete:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(like_to_delete)
    db.commit()
    return


@router.get("/posts/{post_id}/likes")
def get_post_likes(post_id: int):
    for post in posts_db:
        if post.post_id == post_id:
            return {"post_id": post_id, "likes": post.likes}

    raise HTTPException(status_code=404, detail="Post not found")
@router.get("/users/{user_id}/likes")
def get_user_likes(user_id: str):
    liked_posts = [post for post in posts_db if post.owner_id == int(user_id) and post.likes > 0]
    return {"user_id": user_id, "liked_posts": liked_posts}
@router.get("/likes/")
def get_all_likes():
    all_likes = {post.post_id: post.likes for post in posts_db}
    return {"all_likes": all_likes}
@router.delete("/posts/{post_id}/likes", status_code=204)
def reset_post_likes(post_id: int):
    for post in posts_db:
        if post.post_id == post_id:
            post.likes = 0
            return

    raise HTTPException(status_code=404, detail="Post not found")
@router.delete("/users/{user_id}/likes", status_code=204)
def reset_user_likes(user_id: str):
    user_found = False
    for post in posts_db:
        if post.owner_id == int(user_id):
            post.likes = 0
            user_found = True

    if not user_found:
        raise HTTPException(status_code=404, detail="User not found")
    return
@router.delete("/likes/", status_code=204)
def reset_all_likes():
    for post in posts_db:
        post.likes = 0
    return
@router.get("/posts/{post_id}/is_liked_by/{user_id}")
def is_post_liked_by_user(post_id: int, user_id: str):
    for post in posts_db:
        if post.post_id == post_id:
            is_liked = post.owner_id == int(user_id) and post.likes > 0
            return {"post_id": post_id, "user_id": user_id, "is_liked": is_liked}

    raise HTTPException(status_code=404, detail="Post not found")
@router.get("/posts/{post_id}/like_status/{user_id}")
def get_post_like_status(post_id: int, user_id: str):
    for post in posts_db:
        if post.post_id == post_id:
            is_liked = post.owner_id == int(user_id) and post.likes > 0
            return {"post_id": post_id, "user_id": user_id, "is_liked": is_liked}

    raise HTTPException(status_code=404, detail="Post not found")
@router.get("/users/{user_id}/liked_posts")
def get_liked_posts_by_user(user_id: str):
    liked_posts = [post for post in posts_db if post.owner_id == int(user_id) and post.likes > 0]
    return {"user_id": user_id, "liked_posts": liked_posts}
@router.get("/posts/{post_id}/like_count")
def get_post_likes_count(post_id: int):
    for post in posts_db:
        if post.post_id == post_id:
            return {"post_id": post_id, "likes_count": post.likes}

    raise HTTPException(status_code=404, detail="Post not found")
@router.get("/users/{user_id}/total_likes")
def get_user_total_likes(user_id: str):
    total_likes = sum(post.likes for post in posts_db if post.owner_id == int(user_id))
    return {"user_id": user_id, "total_likes": total_likes}
@router.get("/likes/summary")
def get_likes_summary():
    summary = {post.post_id: post.likes for post in posts_db}
    return {"likes_summary": summary}
@router.get("/posts/most_liked")
def get_most_liked_posts():
    if not posts_db:
        return {"most_liked_posts": []}

    max_likes = max(post.likes for post in posts_db)
    most_liked_posts = [post for post in posts_db if post.likes == max_likes]

    return {"most_liked_posts": most_liked_posts}

@router.get("/posts/least_liked")
def get_least_liked_posts():
    if not posts_db:
        return {"least_liked_posts": []}

    min_likes = min(post.likes for post in posts_db)
    least_liked_posts = [post for post in posts_db if post.likes == min_likes]

    return {"least_liked_posts": least_liked_posts}
@router.get("/posts/average_likes")
def get_average_likes():
    if not posts_db:
        return {"average_likes": 0}

    total_likes = sum(post.likes for post in posts_db)
    average_likes = total_likes / len(posts_db)

    return {"average_likes": average_likes}
