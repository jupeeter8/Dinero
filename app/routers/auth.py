from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models
from app.oAuth2 import create_access_token, password_utils
from ..database import get_db

router = APIRouter(tags=["Login"])


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    client_login_query = db.query(models.Users).filter(
        models.Users.username == form_data.username
    )

    client_data: models.Users = client_login_query.first()

    if not client_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found with username {form_data.username}",
        )
    client_login_password = form_data.password
    client_hashed_password = client_data.password

    if not password_utils.verify_hash(client_login_password, client_hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password"
        )

    token = create_access_token(data={"user_ID": client_data.user_id})
    return {"access_token": token, "token_type": "bearer"}
