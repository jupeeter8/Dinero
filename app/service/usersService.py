from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models


def validate_user(tovalidate_user_ID: int, db: Session) -> bool:
    validation_query = db.query(models.Users).filter(
        models.Users.user_id == tovalidate_user_ID
    )
    validation_data = validation_query.first()

    if not validation_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with user_ID: {tovalidate_user_ID} does not exist",
        )
    return True
