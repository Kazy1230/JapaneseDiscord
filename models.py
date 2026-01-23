from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class UserStat(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True)
    discord_id = Column(String, unique=True, nullable=False)

    # 累積学習時間（分）
    total_minutes = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
