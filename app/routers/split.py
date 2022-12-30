from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.schema import SplitDetails
from app.service.usersService import validate_user
from .. import models
from ..database import get_db
from ..oAuth2 import get_current_user

router = APIRouter(tags=["Balance and settle"])

# TODO Added Created by column in Split table
@router.post("/record/split")
async def split(
    split_detail: SplitDetails,
    current_user_ID: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # data = split_detail.dict()

    # Check if user is not requesting to add split data for someone else
    if (
        not split_detail.paid_by == current_user_ID
        and not split_detail.owed_by == current_user_ID
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User Can only add balance for themselves",
        )

    # Check if the user is trying to add split with themselve
    if split_detail.paid_by == split_detail.owed_by:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User can not owe themselve"
        )

    # Validate both user_id
    validate_user(split_detail.paid_by, db)
    validate_user(split_detail.owed_by, db)

    return None
