from fastapi import FastAPI, Response, status, HTTPException, Depends
# from fastapi.params import Body
# from pydantic import BaseModel
# import psycopg2
# from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
# from sqlalchemy.orm import Session
# from typing import List
# from .utils import hash
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
    
# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="Postgres", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successfull.")
#         break

#     except Exception as error:
#         print("Connecting to database failed.")
#         print(f"Error: {error}")
#         time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
