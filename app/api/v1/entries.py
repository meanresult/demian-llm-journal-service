from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.Session import get_db
from app.core.auth import get_current_user

router = APIRouter(tags=["entries"])

@router.post("/entries/post")
def send_diary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user("sub"))
)