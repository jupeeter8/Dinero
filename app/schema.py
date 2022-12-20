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
    paid_amount: int
    owed_by: int
    owed_amount: int
    group_id: Optional[int] = -1
    reason: str
    category: str
    split_method: dict
