from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

'''
CRUD operations:-
C - Create operations (Post request which sends data)
R - Read operations (Get request which does not send any data, just asks for data)
U - Update operations (Put/Patch request which modifies existing data)
D - Delete operations (Delete request which removes existing data)
'''

router = APIRouter(
  prefix="/posts", # makes it so that all the routes in this file are appended with /posts at the start
  tags=['posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute("""SELECT * FROM posts""")
  # posts = cursor.fetchall()

  # The following is a left outer join (left inner by default in sqlalchemy so we explicitly set it)
  posts = db.query(models.Post).all()
  return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost) 
# 201 status code represents the creation of a post
def create_posts(post : schemas.CreatePost, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
  #                (post.title, post.content, post.published))
  # new_post = cursor.fetchone()

  # conn.commit() # saves the changes to the database
  
  new_post = models.Post(**post.dict(), owner_id=current_user.id)
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  
  return new_post

@router.get("/{id}", response_model=schemas.PostOut) # id field is a path parameter
def get_post(id: int, db: Session = Depends(get_db)): # we can pass the path parameter as a simple function argument
  # cursor.execute("""SELECT * FROM posts WHERE id = (%s) """, (str(id)))
  # post = cursor.fetchone()

  post = db.query(models.Post).filter(models.Post.id == id).all()
  
  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"The post with the id: {id} doesn't exist")

  return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute("""DELETE FROM posts WHERE id = (%s) RETURNING *""", (str(id)))
  # deleted_post = cursor.fetchone()

  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()

  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} does not exist")
  
  if current_user.id != post.owner_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="not authorized to perform this operation")
  
  post_query.delete(synchronize_session=False)
  db.commit()

  # conn.commit()

  # We should not send any data back while performing a delete operation
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.ResponsePost)
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
  #               (post.title, post.content, post.published, str(id)))
  
  # updated_post = cursor.fetchone()

  # conn.commit()

  post_query = db.query(models.Post).filter(models.Post.id == id)
  old_post = post_query.first()

  if old_post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} does not exist")
  
  if current_user.id != old_post.owner_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                       detail="not authorized to perform this operation")
  
  post_query.update(post.dict(), synchronize_session=False)

  db.commit()

  return post_query.first()
