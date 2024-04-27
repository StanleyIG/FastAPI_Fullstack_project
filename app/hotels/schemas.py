from typing import List

from pydantic import BaseModel, ConfigDict


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int

    # тоько для pydantic 2.0, тут явный атрибут который указывае что модель pydantic может 
    # обращаться к данным как к объектам python, т.е. через точку, в данном случае к объектам модели SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


class SHotelInfo(SHotel):
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)