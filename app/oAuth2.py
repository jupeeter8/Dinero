from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app import models

from app.database import get_db
from .config import env_var
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordUtils:
    def verify_hash(self, password, hashed_password):
        return pwd_context.verify(password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)


password_utils = PasswordUtils()


def create_access_token(data: dict):
    to_encode = data.copy()

    expire_time = datetime.utcnow() + timedelta(
        minutes=env_var.access_token_expire_minutes
    )
    to_encode.update({"exp": expire_time})

    encoded_jwt = jwt.encode(to_encode, env_var.secret_key, algorithm=env_var.algorithm)
    return encoded_jwt


def verify_token_data(token: str):
    try:
        payload = jwt.decode(token, env_var.secret_key, algorithms=[env_var.algorithm])
        user_ID = payload["user_ID"]

        if not user_ID:
            return None
        return user_ID

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user_ID = verify_token_data(token)

    current_user_data = (
        db.query(models.Users).filter(models.Users.user_id == user_ID).first()
    )

    if not current_user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with user_ID {user_ID} does not exist",
        )
    return user_ID
