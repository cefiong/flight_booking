from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi import Query, HTTPException
from sqlmodel import select
from auth.auth import get_current_active_user, get_password_hash
from db.config import SessionDep
from models.user import UserCreate, UserPublic, UserUpdate, User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/users/", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    db_user = User.model_validate(user)
    # hash the password
    # 🔐 hash password before saving
    db_user.password = get_password_hash(user.password)

    print(db_user)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/users/", response_model=list[UserPublic])
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    user = session.exec(select(User).offset(offset).limit(limit)).all()
    return user

@router.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate, session: SessionDep, current_user: Annotated[User, Depends(get_current_active_user)],):
    user_db = session.get(User, user_id)

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this account")

    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db



@router.delete("/users/{user_id}")
def delete_user(user_id: int, session: SessionDep, current_user: Annotated[User, Depends(get_current_active_user)],):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this account")
    session.delete(user)
    session.commit()
    return {"ok": True}

@router.get("/me/", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
