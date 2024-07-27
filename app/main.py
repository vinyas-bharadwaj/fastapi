from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .routers import posts, users, auth, votes
from .config import settings

'''
get - sends a get request to the server and the server sends a response
post - similar to get request but in addition data is also sent along with the post request 
'''



# the following code is not needed since we are using alembic to migrate our data
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Origins array essentially indicates all the domains that can access our API end points
# "*" essentially means that every domain can access our API
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
  return {"message": "welcome to my website"}


@app.get("/sqlalchemy")
def test(db: Session = Depends(get_db)):
  posts = db.query(models.Post).all()
  return posts




