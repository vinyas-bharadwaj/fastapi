from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
  
  # note that 'user_credentials.username' essentially represents email in our case 
  user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail="Invalid credentials")
  
  if not utils.verify(user_credentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Invalid credentials")
  
  # Create a token
  # Return the token

  access_token = oauth2.create_access_token(data = {"user_id": user.id})

  return {"access_token": access_token, "token_type": "bearer"}