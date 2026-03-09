import logging
from sqlalchemy.orm import Session
from app.models.diary import DiaryEntry
from app.services.llm import structure_diary, generate_reflection

logger = logging.getLogger(__name__)


def create_diary_entry(db: Session, user_id: str, content: str) -> DiaryEntry:
    entry = DiaryEntry(user_id=user_id, content=content)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def process_llm_pipeline(diary_id: int, content: str) -> None:
    """BackgroundTasks로 실행. 일기 저장 후 LLM 처리하여 DB 업데이트."""
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        structured = structure_diary(content)
        reflection = generate_reflection(content, structured)

        entry = db.query(DiaryEntry).filter(DiaryEntry.diary_id == diary_id).first()
        if not entry:
            logger.error("diary_id=%d not found for LLM pipeline", diary_id)
            return

        entry.structured_data = structured
        entry.reflection = reflection
        db.commit()
        logger.info("LLM pipeline complete for diary_id=%d", diary_id)
    except Exception as e:
        logger.error("LLM pipeline failed for diary_id=%d: %s", diary_id, e)
        db.rollback()
    finally:
        db.close()


def get_diary_entries(db: Session, user_id: str, skip: int = 0, limit: int = 20) -> list[DiaryEntry]:
    return (
        db.query(DiaryEntry)
        .filter(DiaryEntry.user_id == user_id)
        .order_by(DiaryEntry.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_diary_entry(db: Session, user_id: str, diary_id: int) -> DiaryEntry | None:
    return (
        db.query(DiaryEntry)
        .filter(DiaryEntry.diary_id == diary_id, DiaryEntry.user_id == user_id)
        .first()
    )
