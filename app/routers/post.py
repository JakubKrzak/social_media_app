from unittest import result

from fastapi import Query, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get('/',response_model=List[schemas.PostResponse])
@router.get('/',response_model=List[schemas.PostOut])
def get_posts(limit: int=10, skip: int=0, search: Optional[str] = "", db: Session = Depends(get_db), current_user: dict=Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    return [{"post": post, "votes": votes} for post, votes in results]
 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db), current_user: dict=Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_post_by_id(id: int, db: Session=Depends(get_db), current_user: dict=Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()


    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id}, not found")
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), current_user: dict=Depends(oauth2.get_current_user)):
    
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id}, not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You cant delete not yours post")
    
    db.delete(post)
    db.commit()

    return {"message": f"Post with id: {id} has been deleted"}

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, update_post: schemas.PostUpdate, db: Session=Depends(get_db), current_user: dict=Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id}, not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You cant edit not yours post")
    
    post_query.update(update_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()