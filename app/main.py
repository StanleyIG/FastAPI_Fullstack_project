from fastapi import FastAPI, Depends
from fastapi.requests import Request
from pydantic import BaseModel
from typing import Annotated
from settings import HotelSearchArgs
from datetime import datetime
from app.bookings.router import router as router_bookings

app = FastAPI(
    title="Бронирование Отелей",
    version="0.1.0",
    root_path="/api",
)

#app.include_router(router_bookings)

class SBooking(BaseModel):
    room_id: int
    date_from: datetime
    date_to: datetime

class SBookingPublic(BaseModel):
    date_from: datetime
    date_to: datetime
    qwerty: int
# @app.get('/hotels/{id}')
# def get_hotels(search_args: HotelSearchArgs = Depends()):
#     return search_args


@app.post('/bookings')
def add_booking(booking: Annotated[SBooking, Depends()]) -> list[SBookingPublic]:
    d = {'id': 1, "date_from": "2024-04-27T00:00:00", "date_to": "2024-04-27T00:00:00", 'qwe': 123}
    return [d]                                                        

# list[SBooking] для валидации отдаваемых данных
# как более лаконичный способ вместо response_model = list[SBooking]
# в праметрах контроллера

