from fastapi import APIRouter

from city.crud import get_all_cities
from dependencies import CommonSession
from temperature import crud, schemas


router = APIRouter()


@router.get("/temperatures", response_model=list[schemas.TemperatureList])
def get_temperatures(
        db: CommonSession,
        city_id: int | None = None
) -> list[schemas.TemperatureList]:
    return crud.get_all_temperature_records(city_id, db)


@router.post("/temperatures/update")
def update_temperatures(db: CommonSession) -> dict:
    cities = get_all_cities(db)

    for city in cities:
        crud.update_temperature_record(city, db)

    return {"message": "success"}
