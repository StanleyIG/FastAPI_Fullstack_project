from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    # тоько для pydantic 2.0, тут явный атрибут который указывае что модель pydantic может 
    # обращаться к данным как к объектам python, т.е. через точку, в данном случае к объектам модели SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class SBookingInfo(SBooking):
    image_id: int
    name: str
    description: Optional[str]
    services: list[str]

    model_config = ConfigDict(from_attributes=True)


class SNewBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    