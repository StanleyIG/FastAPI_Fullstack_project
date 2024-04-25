from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import Column, Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database import Base
# from app.hotels.rooms.models import Rooms
# from app.users.models import Users
from app.hotels.models import Hotels # Импортировал модель Hotel т.к. она нужна для relationship связной модели Hotels

# if TYPE_CHECKING:
#     # Чтоб убрать ошибки IDE при предупреждении отсутствия импорта
#     from app.hotels.rooms.models import Rooms
#     from app.users.models import Users
    


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date] = mapped_column(Date)
    date_to: Mapped[date] = mapped_column(Date)
    price: Mapped[int]
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"))
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))

    room: Mapped["Rooms"] = relationship(back_populates="bookings")
    user: Mapped["Users"] = relationship(back_populates="bookings")
    

    def __str__(self):
        return f"Бронь #{self.id}"

 
# class Bookings(Base):
#     __tablename__ = "bookings"

#     id = Column(Integer, primary_key=True)
#     room_id = Column(ForeignKey("rooms.id"))
#     user_id = Column(ForeignKey("users.id"))
#     date_from = Column(Date, nullable=False)
#     date_to = Column(Date, nullable=False)
#     price = Column(Integer, nullable=False)
#     total_cost = Column(Integer, Computed("(date_to - date_from) * price"))
#     total_days = Column(Integer, Computed("date_to - date_from"))

#     user = relationship("Users", back_populates="bookings")
#     room = relationship("Rooms", back_populates="booking")

#     def __str__(self):
#         return f"Booking #{self.id}"
