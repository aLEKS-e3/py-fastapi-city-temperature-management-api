import os
import requests

from typing import List
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.orm import Session

from temperature import schemas
from city.models import City
from temperature.models import Temperature

load_dotenv()

API_KEY = os.environ.get("API_KEY")
URL = os.environ.get("URL")


def get_all_temperature_records(
        city_id: int | None,
        db: Session
) -> List[Temperature]:
    if city_id:
        return db.query(Temperature).filter_by(city_id=city_id).all()

    return db.query(Temperature).all()


def get_temperature_records_for_city(
        city_id: int,
        db: Session
) -> List[Temperature]:
    return db.query(Temperature).filter_by(city_id=city_id).all()


async def update_temperature_record(city: City, db: Session) -> None:
    response = requests.get(
        URL,
        params={
            "key": API_KEY,
            "q": city.name
        }
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to fetch temperature data for {city.name}"
        )

    weather = response.json()["current"]

    temperature_data = schemas.TemperatureCreate(
        city_id=city.id,
        temperature=weather["temp_c"],
        date_time=weather["last_updated"]
    )
    temperature = Temperature(**temperature_data.model_dump())

    db.add(temperature)
    db.commit()
