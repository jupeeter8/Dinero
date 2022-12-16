from pydantic import BaseModel, EmailStr


class CreateNewUser(BaseModel):
    username: str
    email: EmailStr
    password: str
