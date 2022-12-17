from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models


class UserValidator:
    def __init__(self, user_ID: int) -> None:
        self.tovalidate_user_ID: int = user_ID

    def validate_user(self, db: Session) -> bool:
        validation_query = db.query(models.Users).filter(
            models.Users.user_id == self.tovalidate_user_ID
        )
        validation_data = validation_query.first()

        if not validation_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with user_ID: {self.tovalidate_user_ID} does not exist",
            )
        return True
