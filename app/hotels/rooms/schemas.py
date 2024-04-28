from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    services: List[str]
    price: int
    quantity: int
    image_id: int

    # тоько для pydantic 2.0, тут явный атрибут который указывае что модель pydantic может 
    # обращаться к данным как к объектам python, т.е. через точку, в данном случае к объектам модели SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


class SRoomInfo(SRoom):
    total_cost: int
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)