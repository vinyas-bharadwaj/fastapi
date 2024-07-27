from fastapi import APIRouter, status, Depends, HTTPException
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/vote",
  tags=['vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
        current_user: int = Depends(oauth2.get_current_user)):
  
  post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {vote.post_id} does not exist")
  
  vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
  found_vote = vote_query.first()

  # if the user wants to like the post
  if vote.dir == 1:
    # The post has already been liked by this user so he cannot like it again
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                          detail=f"user {current_user.id} has already voted on post with id {vote.post_id}")
    
    # The post has previously not been liked by this user
    new_vote = models.Vote(post_id=vote.post_id, user_id=current_user .id)
    db.add(new_vote)
    db.commit()

    return {"message": "successfully added vote"}
  
  # if the user wants to remove his like since he clicked by accident or changed his mind
  else:
    # This post has not previously been liked by this user and hence he cannot unlike it
    if found_vote is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
    
    # This post has been previously liked by this user and so he has the ability to unlike it
    vote_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "successfully deleted post"}
    

