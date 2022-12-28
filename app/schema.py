from datetime import datetime
from pydantic import BaseModel, EmailStr


class CreateNewUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDataResponse(BaseModel):
    username: str
    email: EmailStr
    user_id: int
    joined_on: datetime

    class Config:
        orm_mode = True


class InviteFriend(BaseModel):
    user_a: int
    user_b: int
    relation: str


class GetAllFriendRequest(BaseModel):
    sender: int
    reciver: int
    status: bool
    sent_on: datetime

    class Config:
        orm_mode = True
