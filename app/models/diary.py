# app/models/diary.py
# 일기 모델 정의하는 파일 - 일기 항목의 구조와 데이터베이스 테이블 매핑

from sqlalchemy import Column, BigInteger, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.db.base import Base

class DiaryEntry(Base):
    __tablename__ = "diary_entries"
    diary_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)