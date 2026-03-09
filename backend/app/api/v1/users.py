from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.auth import get_current_user

router = APIRouter(tags=["users"])

@router.get("/users/me")
def get_me(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["sub"]  # 토큰에서 나온 내 ID

    row = db.execute(
        text("""
            INSERT INTO users (user_id)
            VALUES (:user_id)
            ON CONFLICT (user_id) DO NOTHING
        """),
        {"user_id": user_id}
    )
    db.commit()

    row = db.execute(
        text("""
            SELECT user_id, display_name, timezone, created_at
            FROM users
            WHERE user_id = :user_id
        """),
        {"user_id": user_id}
    ).mappings().first()

    return row