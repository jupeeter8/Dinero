from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware

from app import models
from .routers import users
from .database import engine

app = FastAPI()
app.include_router(users.router)

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
