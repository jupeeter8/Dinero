from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.schema import SplitDetails
from .. import models
from ..database import get_db
from ..oAuth2 import get_current_user

router = APIRouter(tags=["Balance and settle"])


@router.post("/record/split")
async def split(
    split_detail: SplitDetails,
    current_user_ID: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return split_detail
