from sqlmodel import Field , SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str

class Pokemon(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pokemon_name: str
    pokemon_type: str
    level: int
    region: str
    user_id: int = Field(foreign_key="user.id")

