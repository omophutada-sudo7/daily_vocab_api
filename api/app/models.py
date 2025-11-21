from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Word(Base):
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), unique=True, nullable=False)
    definition = Column(Text)
    difficulty_level = Column(
        SQLEnum('Beginner', 'Intermediate', 'Advanced', name='difficulty'),
        default='Beginner'
    )
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    submissions = relationship("PracticeSubmission", back_populates="word_rel")

class PracticeSubmission(Base):
    __tablename__ = "practice_submissions" 
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1, nullable=False) 
    word_id = Column(Integer, ForeignKey('words.id'), nullable=False)
    submitted_sentence = Column(Text, nullable=False)
    score = Column(DECIMAL(3, 1))
    feedback = Column(Text)
    corrected_sentence = Column(Text)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)

    word_rel = relationship("Word", back_populates="submissions")