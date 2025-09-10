from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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


@app.get("/")
async def root():
    return {"message": "Hello World ss"}

@app.post("/posts")
def create_posts(post: Post):
 
    print("===test post", post)
    print("===test non pydantic",   post.model_dump())
    return {"message": "sucessfully created posts"}