from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database import Base


if TYPE_CHECKING:
    # Чтоб убрать ошибки IDE при предупреждении отсутствия импорта
    from bookings.models import Bookings


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]

    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")

    def __str__(self):
        return f"Пользователь {self.email}"


# class Users(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False)
#     hashed_password = Column(String, nullable=False)

#     bookings = relationship("Bookings", back_populates="user")

#     def __str__(self):
#         return f"Пользователь {self.email}"
