from app.db.Session import engine
from app.db.base import Base
import app.models  # 이 import가 핵심 (모델 등록)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()