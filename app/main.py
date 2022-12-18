from typing import List
from fastapi import Depends, FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models

from app.database import get_db
from app.schema import UserDataResponse

from .routers import users, auth, friends


app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(friends.router)

origins = [""]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=responses.RedirectResponse)
async def main():
    return "/docs"


@app.get("/getAllUsers", response_model=List[UserDataResponse])
async def get_all_user(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()

    return users
