from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.auth import get_current_user
from app.schemas.diary import DiaryEntryCreate, DiaryEntryResponse
from app.services import diary as diary_service

router = APIRouter(prefix="/diary-entries", tags=["diary"])


@router.post("", response_model=DiaryEntryResponse, status_code=201)
def create_diary(
    body: DiaryEntryCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["sub"]
    entry = diary_service.create_diary_entry(db, user_id, body.content)
    background_tasks.add_task(diary_service.process_llm_pipeline, entry.diary_id, body.content)
    return entry


@router.get("", response_model=list[DiaryEntryResponse])
def list_diaries(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["sub"]
    return diary_service.get_diary_entries(db, user_id, skip, limit)


@router.get("/{diary_id}", response_model=DiaryEntryResponse)
def get_diary(
    diary_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["sub"]
    entry = diary_service.get_diary_entry(db, user_id, diary_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    return entry
