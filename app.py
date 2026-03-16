from fastapi import FastAPI
from routers import chat, user, auth
from db.config import create_db_and_tables

app = FastAPI()
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(chat.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Flight Assistant API"}