from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import hashlib

app = FastAPI()


DB_FILE = "users.db"
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)

with engine.connect() as connection:
    connection.execute(text(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(30) NOT NULL,
            email TEXT,
            password TEXT
        );
        """
    ))
class User(BaseModel):
    name: str
    email: str
    password: str

def hash_passkey(password):
    return hashlib.sha256(password.encode()).hexdigest()
   
@app.post("/signup")
def signup(user: User):
    with engine.connect() as connection:
        connection.execute(
            text("""
                INSERT INTO users (name, email, password)
                VALUES (:name, :email, :password)
            """),
            {"name": user.name, "email": user.email, "password": hash_passkey(user.password)}
        )
        connection.commit()
    return {"message": "User registered successfully!"}
