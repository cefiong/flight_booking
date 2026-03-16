from fastapi import APIRouter
from auth.auth import authenticate_user, login
from db.config import SessionDep
from models.user import UserPublic
from models.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) :
    return login(session=session, form_data=form_data)