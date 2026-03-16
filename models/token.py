from sqlmodel import Field, Session, SQLModel
from pydantic import EmailStr

class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: EmailStr | None = None
