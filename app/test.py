from database import async_session_maker, engine
from app.users.models import Users
from sqlalchemy import and_, func, or_, select
from datetime import date
import datetime
import asyncio
  


async def find_all(hotel_id):
    async with async_session_maker() as session:
        get_rooms = select(Users)
        rooms = await session.execute(get_rooms)
        result = rooms.mappings().all()
        return result[0]['Bookings'].id



async def main():
    rooms = await find_all(1)
    print(rooms)

if __name__ == "__main__":
    asyncio.run(main())
