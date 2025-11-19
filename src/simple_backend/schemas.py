from pydantic import BaseModel, Field, conint, confloat
from typing import Optional
from datetime import datetime


class SessionCreate(BaseModel):
    """
    Schema per la creazione di una nuova sessione
    """
    user_id: str = Field(..., min_length=1, max_length=64, description="ID dell'utente")
    exercise_type: str = Field(..., min_length=1, max_length=128, description="Tipo di esercizio")
    duration_seconds: conint(ge=1) = Field(..., description="Durata dell'esercizio in secondi, >=1")
    repetitions: Optional[conint(ge=0)] = Field(None, description="Numero di ripetizioni (opzionale)")
    quality_score: confloat(ge=0.0, le=100.0) = Field(..., description="Punteggio di qualità 0-100")


class SessionRead(BaseModel):
    """
    Schema per la lettura di una sessione
    """
    id: int
    user_id: str
    exercise_type: str
    duration_seconds: int
    repetitions: Optional[int]
    quality_score: float
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True  # necessario per from_orm in Pydantic v2
    }

class SessionFilter(BaseModel):
    """
    Parametri opzionali per filtrare le sessioni
    """
    user_id: Optional[str] = Field(None, description="ID dell'utente")
    exercise_type: Optional[str] = Field(None, description="Tipo di esercizio")
    start_date: Optional[datetime] = Field(None, description="Data di inizio")
    end_date: Optional[datetime] = Field(None, description="Data di fine")
class UserStats(BaseModel):
    """
    Schema per le statistiche di un utente
    """
    user_id: str
    total_sessions: int
    avg_duration_seconds: Optional[float] = None
    avg_quality_score: Optional[float] = None
