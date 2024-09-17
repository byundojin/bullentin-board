from fastapi import FastAPI, Body, Response
from pydantic import BaseModel
import sqlite3

app = FastAPI()

db_connection = sqlite3.connect(".db")

post_sql = """
CREATE TABLE posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title text,
    content text,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def make_table():
    cursor = db_connection.cursor()
    cursor.execute(post_sql)
    db_connection.commit()

try:
    make_table()
except sqlite3.OperationalError as e:
    assert(e.args[0] == 'table posts already exists')

def create_post(title, content):
    post_create_sql = \
"""
insert into posts(title, content) values (?, ?);
"""

    cursor = db_connection.cursor()
    cursor.execute(post_create_sql, (title, content))
    db_connection.commit()

class PostBody(BaseModel):
    title:str
    content:str

@app.post("/post")
async def post_post(post_body:PostBody = Body()):
    create_post(
        title=post_body.title,
        content=post_body.content
    )

    return Response(status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)