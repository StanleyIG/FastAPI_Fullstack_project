from typing import Optional, TYPE_CHECKING
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from sqlalchemy import JSON, Column, Integer, String

if TYPE_CHECKING:
    # Чтоб убрать ошибки IDE при предупреждении отсутствия импорта
    from hotels.models import Hotels
    from bookings.models import Bookings


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    services: Mapped[list[str]] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]

    hotel: Mapped["Hotels"] = relationship(back_populates="room")
    bookings: Mapped[list["Bookings"]] = relationship(back_populates="room")

    def __str__(self):
        return f"Номер {self.name}"


# class Rooms(Base):
#     __tablename__ = "rooms"

#     id = Column(Integer, primary_key=True)
#     hotel_id = Column(ForeignKey("hotels.id"), )
#     name = Column(String, )
#     description = Column(String, nullable=True)
#     price = Column(Integer, )
#     services = Column(JSON, nullable=True)
#     quantity = Column(Integer, )
#     image_id = Column(Integer)

#     hotel = relationship("Hotels", back_populates="rooms")
#     booking = relationship("Bookings", back_populates="room")

#     def __str__(self):
#         return f"Номер {self.name}"
