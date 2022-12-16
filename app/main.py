from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware
from app import models

from app.database import Base, engine

app = FastAPI()

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
