from fastapi import FastAPI

from city.routers import router as city_router

app = FastAPI()

app.include_router(city_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
