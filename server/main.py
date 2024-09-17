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
