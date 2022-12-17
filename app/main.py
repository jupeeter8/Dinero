from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware

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
