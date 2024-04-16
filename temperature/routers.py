from fastapi import APIRouter

from city.crud import get_all_cities
from dependencies import CommonSession
from temperature import crud, schemas


router = APIRouter()


@router.get("/temperatures", response_model=list[schemas.TemperatureList])
async def get_temperatures(
        db: CommonSession,
        city_id: int | None = None
) -> list[schemas.TemperatureList]:
    if city_id:
        return await crud.get_temperature_records_for_city(
            db=db,
            city_id=city_id
        )

    return await crud.get_all_temperature_records(db)


@router.post("/temperatures/update")
async def update_temperatures(db: CommonSession) -> dict:
    cities = await get_all_cities(db)

    for city in cities:
        await crud.update_temperature_record(city, db)

    return {"message": "success"}
