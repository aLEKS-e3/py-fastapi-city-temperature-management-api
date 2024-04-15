from fastapi import APIRouter, HTTPException

from city.models import City
from city import schemas, crud
from dependencies import CommonSession

router = APIRouter()


@router.get("/cities", response_model=list[schemas.CityList])
def get_cities(db: CommonSession):
    return crud.get_all_cities(db)


def get_city_by_name(name: str, db: CommonSession):
    return db.query(City).filter(City.name == name).first()


@router.post("/cities", response_model=schemas.CityDetail)
def create_city(city: schemas.CityCreate, db: CommonSession):
    if get_city_by_name(city.name, db):
        raise HTTPException(
            status_code=400,
            detail="City with that name already exists",
        )
    return crud.create_city(db, city)


@router.get("/cities/{city_id}", response_model=schemas.CityDetail)
def get_city_detail(city_id: int, db: CommonSession):
    return crud.get_city_by_id(db, city_id)


@router.delete("/cities/{city_id}")
def delete_city(city_id: int, db: CommonSession):
    city = crud.get_city_by_id(db, city_id)
    crud.delete_city(city, db)

    return {"message": "City deleted successfully"}


@router.put("/cities/{city_id}", response_model=schemas.CityDetail)
def update_city(
        city_id: int,
        city_to_update: schemas.CityCreate,
        db: CommonSession
):
    city = crud.get_city_by_id(db, city_id)
    updated_city = crud.update_city(db, city, city_to_update)

    return updated_city
