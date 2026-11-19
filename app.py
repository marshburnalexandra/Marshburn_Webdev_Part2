from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from sqlmodel import Session, select
import hashlib

from database import create_db_and_tables, engine
from models import User, Pokemon

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "login.html")

@app.get("/collection")
def collection_page():
    return FileResponse(BASE_DIR / "index.html")

@app.post("/register")
def register(user: User):

    with Session(engine) as session:

        username = user.username.strip()
        existing_user = session.exec(select(User).where(User.username == username)).first()

        if existing_user:
            return {"success": False, "message": "That username is already taken."}

        hashed_password = hashlib.sha256(
            user.password.encode()
        ).hexdigest()

        user.username = username
        user.password = hashed_password

        session.add(user)
        session.commit()

        return {"success": True, "message": "Account created. You can log in now."}

@app.post("/login")
def login(user: User):
    with Session(engine) as session:

        existing_user = session.exec(select(User).where(User.username == user.username.strip())).first()

        if not existing_user:
            return {"success": False, "message": "Username or password is incorrect."}

        hashed_password = hashlib.sha256(
            user.password.encode()
        ).hexdigest()

        if existing_user.password == hashed_password:
            return {
                "success": True,
                "message": "Login successful",
                "user_id": existing_user.id,
                "username": existing_user.username,
            }
        else:
            return {"success": False, "message": "Username or password is incorrect."}

@app.get("/register-page")
def register_page():
    return FileResponse(BASE_DIR / "register.html")

@app.get("/login-page")
def login_page():
    return FileResponse(BASE_DIR / "login.html")

@app.get("/pokemon/{user_id}")
def get_pokemon(user_id: int):
    with Session(engine) as session:
        pokemon = session.exec(select(Pokemon).where(Pokemon.user_id == user_id)).all()
        return pokemon

@app.post("/pokemon")
def add_pokemon(pokemon: Pokemon):
    with Session(engine) as session:
        if not session.get(User, pokemon.user_id):
            return {"success": False, "message": "Please log in before adding Pokémon."}

        session.add(pokemon)
        session.commit()
        session.refresh(pokemon)
        return {"success": True, "message": "Pokémon added!", "pokemon": pokemon}
