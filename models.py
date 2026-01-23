from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    discord_id = Column(String, unique=True)
    username = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class StudyLog(Base):
    __tablename__ = "study_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String)  # grammar / vocab / reading
    content = Column(String)
    is_correct = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)
