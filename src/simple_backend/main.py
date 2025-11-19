from fastapi import FastAPI, Depends, HTTPException, status, Response, Query
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from datetime import datetime
import crud, schemas
from database import SessionLocal, engine
import models

# Creazione tabelle (solo se non si usa Alembic)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Esempio sistema Teleriabilitazione",
    version="1.0.0",
)

# API Key auth
header_scheme = APIKeyHeader(name="x-key")


# ----------------------------
# Dependencies
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_key(key: str = Depends(header_scheme)):
    if key != "secret": #Provvisorio
        raise HTTPException(status_code=401, detail="Unauthorized")
    return key


# ----------------------------
# POST /sessions
# ----------------------------
@app.post(
    "/sessions",
    response_model=schemas.SessionRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(validate_key)]
)
def create_session(
    session_in: schemas.SessionCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    try:
        obj = crud.create_session(db, session_in)

        # Imposto header Location con l’ID della risorsa creata
        response.headers["Location"] = f"/sessions/{obj.id}"

        # Restituisco direttamente l’oggetto Pydantic
        return schemas.SessionRead.from_orm(obj)

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get(
    "/sessions",
    response_model=List[schemas.SessionRead],
    dependencies=[Depends(validate_key)]
)
def get_sessions(
    db: Session = Depends(get_db),
    user_id: Optional[str] = Query(None),
    exercise_type: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
):
    filters = schemas.SessionFilter(
        user_id=user_id,
        exercise_type=exercise_type,
        start_date=start_date,
        end_date=end_date
    )
    try:
        sessions = crud.get_sessions(db, filters)
        return [schemas.SessionRead.from_orm(s) for s in sessions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# ----------------------------
# GET /users/{user_id}/stats
# ----------------------------
@app.get(
    "/users/{user_id}/stats",
    response_model=schemas.UserStats,
    dependencies=[Depends(validate_key)]
)
def get_user_stats(
    user_id: str,
    db: Session = Depends(get_db)
):
    try:
        stats = crud.get_user_stats(db, user_id)
        return schemas.UserStats(**stats)

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
