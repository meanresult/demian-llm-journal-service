# db의 설계도 - 모델 정의
# SQLAlchemy의 Base 클래스를 상속받아 모델을 정의

# app/db/base.py

from sqlalchemy.orm import declarative_base

Base = declarative_base()