from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

from database import SessionLocal


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


CommonSession = Annotated[Session, Depends(get_db)]
