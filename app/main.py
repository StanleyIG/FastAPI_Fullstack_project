from fastapi import FastAPI, Depends
from fastapi.requests import Request
from pydantic import BaseModel
from typing import Annotated
from config import HotelSearchArgs
from datetime import datetime

app = FastAPI()


class SBooking(BaseModel):
    room_id: int
    date_from: datetime
    date_to: datetime

@app.get('/hotels/{id}')
def get_hotels(search_args: HotelSearchArgs = Depends()):
    return search_args

@app.post('/bookings')
def add_booking(booking: Annotated[SBooking, Depends()]) -> list[SBooking]:
    # booking = {'room_id':1, 'date_from': datetime.now(), 'date_to': datetime(2024, 4, 27)}
    return {'room_id':1, 'date_from': datetime.now(), 'date_to': datetime(2024, 4, 27), 'hotel': 'SpaResort *5'}#[booking] # ошибка
