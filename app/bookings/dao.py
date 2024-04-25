from datetime import date, timedelta

from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker, async_session_maker_nullpool
from app.exceptions import RoomFullyBooked
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    # async def find_all(cls, user_id: int):
    #     async with async_session_maker() as session:
    #         query = (
    #             select(Bookings.__table__.columns).where(Bookings.user_id == user_id)
    #         )

    #         result = await session.execute(query)
    #         return result.mappings().all()
    async def find_all(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(Bookings.__table__.columns)
                .where(Bookings.user_id == user_id)
                .join(Bookings.room)
            )
            
            result = await session.execute(query)
            return result.mappings().all()

    

