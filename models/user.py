from sqlmodel import Field, Session, SQLModel
from pydantic import EmailStr

class UserBase(SQLModel):
    name: str
    email: EmailStr = Field(index=True)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str

class UserPublic(UserBase):
    id: int

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None