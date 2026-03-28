

from fastapi import Query, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2, database
from ..database import get_db


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session=Depends(database.get_db), current_user: dict=Depends(oauth2.get_current_user)):
    
    query_post = db.query(models.Post).filter(models.Post.id == vote.post_id)
    find_post = query_post.first()
    if not find_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id {vote.post_id}")    

    query_vote = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    find_vote = query_vote.first()

    if vote.dir == 1:
        if find_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id}, has already liked post")
        
        new_vote = models.Vote(user_id = current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": f"User {current_user.id} like post {vote.post_id}"}
        
    if vote.dir == 0:
        if find_vote is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} not voted on this post")
        query_vote.delete(synchronize_session=False)
        db.commit()
        return {"message": f"User {current_user.id} unlike post {vote.post_id}"}


