from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
# from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
    
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="Postgres", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successfull.")
        break

    except Exception as error:
        print("Connecting to database failed.")
        print(f"Error: {error}")
        time.sleep(2)


# testing the sqlalchemy
@app.get("/sqlalchemy", response_model = List[schemas.Post_response])
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/sqlalchemy/posts", response_model=schemas.Post_response)
def create_posts_2(post: schemas.Post, db: Session = Depends(get_db)):
    # print(**post.model_dump())
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
async def get_posts():
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    print(posts)
    return posts

@app.get("/posts/{id}")
def get_post_by_id(id: int):
    cursor.execute("select * from posts where id = %s", (str(id)))
    test_post = cursor.fetchone()
    
    if test_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist.")

    return test_post

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post):
    cursor.execute("insert into posts (title, content, published) values (%s, %s, %s) returning *", 
                   (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    conn.commit()

    return new_post

@app.put("/posts/{id}")
def update_post(id: int, post: schemas.Post):
    cursor.execute("update posts set title = %s, content = %s, published = %s  where id = %s returning *",
                                            (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if (updated_post == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"id {id} does not exist")
    
    return updated_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("delete from posts where id = %s returning *",str(id))
    deleted_post = cursor.fetchone()
    conn.commit()

    if (deleted_post == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist.")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hashing the password so that actual password is not stored in the database
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

