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
    async def find_all(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
            select(Bookings.room)
            .select_from(Bookings)
            .join(Rooms, on=Bookings.room_id == Rooms.id)
        )

            result = await session.execute(query)
            res = result.mappings().all()
            return res
    
    @classmethod
    async def find_need_to_remind(cls, days: int):
        async with async_session_maker_nullpool() as session:
            query = (
                select(Bookings.room)
                # .options(joinedload(Bookings.user))
                .filter(date.today() == Bookings.date_from - timedelta(days=days))
            )
            result = await session.execute(query)
            return result.scalars().all()


    # async def find_all(cls, user_id: int):
    #     async with async_session_maker() as session:
    #         query = (
    #             select(Bookings)
    #             .where(Bookings.user_id == user_id)
    #             .join(Bookings.room)
    #         )
            
    #         result = await session.execute(query)
    #         return result.mappings().all()

    

