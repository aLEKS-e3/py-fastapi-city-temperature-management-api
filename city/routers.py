from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city.models import City
from city import schemas, crud
from database import SessionLocal

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/cities/", response_model=list[schemas.CityList])
def get_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db)


def get_city_by_name(name: str, db: Session = Depends(get_db)):
    return db.query(City).filter(City.name == name).first()


@router.post("/cities/", response_model=schemas.CityDetail)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    if get_city_by_name(city.name, db):
        raise HTTPException(
            status_code=400,
            detail="City with that name already exists",
        )
    return crud.create_city(db, city)


@router.get("/cities/{city_id}/", response_model=schemas.CityDetail)
def get_city_detail(city_id: int, db: Session = Depends(get_db)):
    return crud.get_city_by_id(db, city_id)


@router.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city_by_id(db, city_id)
    crud.delete_city(city, db)

    return {"message": "City deleted successfully"}


@router.put("/cities/{city_id}/", response_model=schemas.CityDetail)
def update_city(
        city_id: int,
        city_to_update: schemas.CityCreate,
        db: Session = Depends(get_db)
):
    city = crud.get_city_by_id(db, city_id)
    updated_city = crud.update_city(db, city, city_to_update)

    return updated_city
