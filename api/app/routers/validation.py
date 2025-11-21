from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import ValidateSentenceRequest, ValidateSentenceResponse
from app.models import PracticeSubmission, Word
from app.database import get_db
from app.utils import mock_ai_validation
from sqlalchemy import exc

router = APIRouter()

@router.post(
    "/validate-sentence",
    response_model=ValidateSentenceResponse,
    status_code=status.HTTP_201_CREATED
)
def validate_sentence(
    request_data: ValidateSentenceRequest,
    db: Session = Depends(get_db)
):
    word_id = request_data.word_id
    submitted_sentence = request_data.sentence
    
    word_entry = db.query(Word).filter(Word.id == word_id).first()

    if not word_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Word with id {word_id} not found"
        )

    validation_result = mock_ai_validation(
        sentence=submitted_sentence,
        target_word=word_entry.word,
        difficulty=word_entry.difficulty_level
    )
    
    score = validation_result["score"]
    level = validation_result["level"]
    suggestion = validation_result["suggestion"]
    corrected_sentence = validation_result["corrected_sentence"]
    
    try:
        new_submission = PracticeSubmission(
            user_id=1,  
            word_id=word_id,
            submitted_sentence=submitted_sentence,
            score=score,
            feedback=suggestion,
            corrected_sentence=corrected_sentence
        )
        
        db.add(new_submission)
        db.commit()
        db.refresh(new_submission)
        
    except exc.SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {e}") 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not save practice submission to database."
        )

    return ValidateSentenceResponse(
        score=score,
        level=level,
        suggestion=suggestion,
        corrected_sentence=corrected_sentence
    )