# 유저 모델 정의하는 파일 

from sqlalchemy import Column, BigInteger, Text, DateTime, ForeignKey, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from datetime import datetime

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    # Supabase auth.users.id를 그대로 넣을 거라 기본값 생성 X
    user_id = Column(UUID(as_uuid=True), primary_key=True)

    display_name = Column(Text, nullable=True)
    timezone = Column(Text, nullable=False, server_default="Asia/Seoul")

    morning_alarm_time = Column(Time, nullable=True)  # (원하면 TIME으로 바꿔도 됨)
    evening_alarm_time = Column(Time, nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())