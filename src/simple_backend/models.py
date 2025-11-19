from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from sqlalchemy import BigInteger, Identity

Base = declarative_base()


class SessionModel(Base):
    __tablename__ = "sessions"

    # AUTO-INCREMENT PostgreSQL
    id = Column(
        BigInteger,
        Identity(start=1, cycle=False),
        primary_key=True,
        index=True
    )

    user_id = Column(String(64), index=True, nullable=False)
    exercise_type = Column(String(128), index = True,nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    repetitions = Column(Integer, nullable=True)
    quality_score = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
