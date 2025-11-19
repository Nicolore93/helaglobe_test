from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import models, schemas



def create_session(db: Session, session_in: schemas.SessionCreate) -> models.SessionModel:
    """
    Crea una nuova sessione nel database.
    """
    db_obj = models.SessionModel(
        user_id=session_in.user_id,
        exercise_type=session_in.exercise_type,
        duration_seconds=session_in.duration_seconds,
        repetitions=session_in.repetitions,
        quality_score=session_in.quality_score,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_sessions(db: Session, filters: schemas.SessionFilter) -> List[models.SessionModel]:
    """
    Restituisce le sessioni filtrate opzionalmente per utente, tipo esercizio e periodo.
    """
    query = db.query(models.SessionModel)

    if filters.user_id:
        query = query.filter(models.SessionModel.user_id == filters.user_id)
    if filters.exercise_type:
        query = query.filter(models.SessionModel.exercise_type == filters.exercise_type)
    if filters.start_date:
        query = query.filter(models.SessionModel.created_at >= filters.start_date)
    if filters.end_date:
        query = query.filter(models.SessionModel.created_at <= filters.end_date)

    return query.order_by(models.SessionModel.created_at.desc()).all()

def get_user_stats(db: Session, user_id: str) -> dict:
    """
    Restituisce statistiche per un dato utente:
    - totale sessioni
    - media durata
    - media punteggio qualità
    """
    query = db.query(
        func.count(models.SessionModel.id),
        func.avg(models.SessionModel.duration_seconds),
        func.avg(models.SessionModel.quality_score)
    ).filter(models.SessionModel.user_id == user_id)

    count, avg_duration, avg_quality = query.one()

    return {
        "user_id": user_id,
        "total_sessions": int(count or 0),
        "avg_duration_seconds": float(avg_duration) if avg_duration is not None else None,
        "avg_quality_score": float(avg_quality) if avg_quality is not None else None,
    }
