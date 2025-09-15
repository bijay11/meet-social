from typing import Optional
from fastapi import status, FastAPI, HTTPException, Response, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title:str
    content: str
    published: bool = True

# Connecting to Database
while True:
    try:
        conn = psycopg2.connect(host='localhost', port=5433, database='meetsocial', user='postgres', password='learndb', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    
    except Exception as error:
        print("Connecting to the database failed.")
        print("Error:", error)
        time.sleep(2)

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "session"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts; """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *; """, 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    # Save the result to DB
    conn.commit()

    return {"data": new_post}
    
@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s; """, (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return {"post": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id =%s RETURNING * ; """,(str(id),))
    post = cursor.fetchone()

    conn.commit()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id),)))
    post = cursor.fetchone()

    conn.commit()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    return {"data": post}