from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException

from city.schemas import CityCreate
from city.models import City


def get_all_cities(db: Session) -> List[City]:
    return db.query(City).all()


def create_city(db: Session, city: CityCreate) -> City:
    db_city = City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_city_by_id(db: Session, city_id: int) -> City:
    if city := db.query(City).filter_by(id=city_id).first():
        return city

    raise HTTPException(
        status_code=404,
        detail="City not found",
    )


def delete_city(city: City, db: Session) -> None:
    db.delete(city)
    db.commit()


def update_city(
        db: Session,
        existing_city: City,
        city_to_update: CityCreate
) -> City:
    for key, value in city_to_update.dict().items():
        setattr(existing_city, key, value)

    db.add(existing_city)
    db.commit()
    db.refresh(existing_city)

    return existing_city
