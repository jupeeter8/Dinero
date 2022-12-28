from datetime import datetime
from typing import Optional
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


class SplitDetails(BaseModel):
    paid_by: int
    p_username: str
    paid_amount: int
    owed_by: int
    o_username: str
    owed_amount: int
    group_id: Optional[int]
    paid_for: str
    category: str
    split_method: dict


class GetAllFriendRequest(BaseModel):
    sender: int
    reciver: int
    status: bool
    sent_on: datetime

    class Config:
        orm_mode = True
