from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from .. import models, schemas
from ..oauth2 import get_current_user


router = APIRouter(
    tags=["posts"]
)


# ==========================
# Get all posts
# ==========================

@router.get(
    "/posts",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.PostOut]
)
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):

    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts



# ==========================
# Create Post
# ==========================

@router.post(
    "/createposts",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostOut
)
def create_post(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    new_post = models.Post(
        owner_id=current_user.id,
        **post.model_dump()
    )


    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return new_post



# ==========================
# Get latest post
# ==========================

@router.get(
    "/posts/latest",
    response_model=schemas.PostOut
)
def get_latest_post(
    db: Session = Depends(get_db)
):

    post = (
        db.query(models.Post)
        .order_by(models.Post.id.desc())
        .first()
    )


    if post is None:
        raise HTTPException(
            status_code=404,
            detail="No posts found"
        )


    return post



# ==========================
# Get Post By ID
# ==========================

@router.get(
    "/posts/{id}",
    response_model=schemas.PostOut
)
def get_post_by_id(
    id: int,
    db: Session = Depends(get_db)
):

    post = (
        db.query(models.Post)
        .filter(models.Post.id == id)
        .first()
    )


    if post is None:
        raise HTTPException(
            status_code=404,
            detail=f"Post {id} not found"
        )


    return post



# ==========================
# Delete Post
# ==========================

@router.delete(
    "/posts/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
    id:int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    post = (
        db.query(models.Post)
        .filter(models.Post.id == id)
        .first()
    )


    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )



    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )


    db.delete(post)
    db.commit()


    return



# ==========================
# Update Post
# ==========================

@router.put(
    "/posts/{id}",
    response_model=schemas.PostOut
)
def update_post(
    id:int,
    updated_post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    post = (
        db.query(models.Post)
        .filter(models.Post.id == id)
        .first()
    )


    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )


    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )



    post.title = updated_post.title
    post.content = updated_post.content
    post.published = updated_post.published


    db.commit()
    db.refresh(post)


    return post