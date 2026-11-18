from fastapi.responses import FileResponse
from fastapi import FastAPI
from sqlmodel import Session , select
import hashlib

from database import create_db_and_tables, engine
from models import User, Pokemon

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"message": "Pokemon Collection"}

@app.post("/register")
def register(user: User):

    with Session(engine) as session:

        existing_user = session.exec(
            select(User).where(User.username == user.username)
        ).first()

        if existing_user:
            return {"message": "Username already exist"}

        hashed_password = hashlib.sha256(
            user.password.encode()
        ).hexdigest()

        user.password = hashed_password

        session.add(user)
        session.commit()

        return {"message": "Registration successful"}

@app.post("/login")
def login(user: User):
    with Session(engine) as session:

        existing_user = session.exec(
            select(User).where(User.username == user.username)
        ).first()

        if not existing_user:
            return {"message": "Username not found"}

        hashed_password = hashlib.sha256(
            user.password.encode()
        ).hexdigest()

        if existing_user.password == hashed_password:
            return {"message": "Login successful"}
        else:
            return {"message": "Incorrect password"}

@app.get("/register-page")
def register_page():
    return FileResponse("register.html")

@app.get("/login-page")
def login_page():
    return FileResponse("login.html")