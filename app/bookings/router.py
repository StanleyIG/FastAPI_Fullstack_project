from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookingInfo, SNewBooking
from app.exceptions import RoomCannotBeBooked
# from app.tasks.tasks import send_booking_confirmation_email
# from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


# @router.get("")
# async def get_bookings():
#     async with async_session_maker() as session:
#         query = select(Booking)
#         result = await session.execute(query)
#         return result

@router.get("")
async def get_bookings():
    result = await BookingDAO.find_all(user_id=1)
    return result[0]