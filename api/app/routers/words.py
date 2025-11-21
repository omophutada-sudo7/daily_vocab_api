from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func # ใช้สำหรับสุ่ม
from app.database import get_db
from app.models import Word
from app.schemas import WordResponse

router = APIRouter()

@router.get("/word", response_model=WordResponse)
def get_random_word(db: Session = Depends(get_db)):
    word = db.query(Word).order_by(func.random()).first()
    
    if not word:
        raise HTTPException(status_code=404, detail="No words found in database")
        
    return word