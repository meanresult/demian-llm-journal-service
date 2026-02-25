from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.Session import get_db  # 네 파일명이 Session.py라서 이렇게 되어있을 가능성 큼

router = APIRouter(prefix="/diary-entries", tags=["diary"])

@router.get("")
def list_diaries(user_id: int, db: Session = Depends(get_db)):
    return {"ok": True, "user_id": user_id}

@router.post("")
def create_diary(db: Session = Depends(get_db)):
    return {"ok": True}