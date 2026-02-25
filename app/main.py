# main.py
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.Session import get_db

from app.api.v1.users import router as users_router
from app.api.v1.diary import router as diary_router


app = FastAPI()

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    return {"result": result.scalar()}

app.include_router(users_router)
app.include_router(diary_router)
