from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookingInfo, SNewBooking
from app.exceptions import RoomCannotBeBooked
# from app.tasks.tasks import send_booking_confirmation_email
# from app.users.dependencies import get_current_user
from app.users.models import Users
from app.database import async_session_maker

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
    return result


@router.get("/{days}")
async def get_booking(days: int):
    result = await BookingDAO.find_need_to_remind(days)
    #room = booking.room
    print(type(result))
    return result#{"room": room.to_dict()}


@router.post("/add", status_code=201)
async def add_booking(
    booking: SNewBooking,
):
    booking = await BookingDAO.add(
        1,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )
    if not booking:
        raise RoomCannotBeBooked
    return booking



