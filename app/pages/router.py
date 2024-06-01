from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.bookings.router import add_booking, get_bookings
from app.exceptions import RoomCannotBeBooked
from app.hotels.rooms.router import get_rooms_by_time
from app.hotels.router import get_hotel_by_id, get_hotels_by_location_and_time
from app.utils import format_number_thousand_separator, get_month_days
from app.bookings.schemas import SBookingInfo, SNewBooking
from app.bookings.dao import BookingDAO
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")



@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.get("/hotels/{location}", response_class=HTMLResponse)
async def get_hotels_page(
    request: Request,
    location: str,
    date_to: date,
    date_from: date,
    hotels=Depends(get_hotels_by_location_and_time),
):
    dates = get_month_days()
    if date_from > date_to:
        date_to, date_from = date_from, date_to
    date_from = max(datetime.today().date(), date_from)
    date_to = min((datetime.today() + timedelta(days=180)).date(), date_to)
    return templates.TemplateResponse(
        "hotels_and_rooms/hotels.html",
        {
            "request": request,
            "hotels": hotels,
            "location": location,
            "date_to": date_to.strftime("%Y-%m-%d"),
            "date_from": date_from.strftime("%Y-%m-%d"),
            "dates": dates,
        },
    )


@router.get("/hotels", response_class=HTMLResponse)
async def get_hotels_page(
    request: Request,
):
    date_from = datetime.today().date()
    date_to = (datetime.today() + timedelta(days=180)).date()
    dates = get_month_days()
    return templates.TemplateResponse(
        "hotels_and_rooms/hotels.html",
        {
            "request": request,
            "hotels": [],
            "location": "",
            "date_to": date_to,
            "date_from": date_from,
            "dates": dates,
        },
    )


@router.get("/hotels/{hotel_id}/rooms", response_class=HTMLResponse)
async def get_rooms_page(
    request: Request,
    date_from: date,
    date_to: date,
    rooms=Depends(get_rooms_by_time),
    hotel=Depends(get_hotel_by_id),
):
    date_from_formatted = date_from.strftime("%d.%m.%Y")
    date_to_formatted = date_to.strftime("%d.%m.%Y")
    booking_length = (date_to - date_from).days
    return templates.TemplateResponse(
        "hotels_and_rooms/rooms.html",
        {
            "request": request,
            "hotel": hotel,
            "rooms": rooms,
            "date_from": date_from,
            "date_to": date_to,
            "booking_length": booking_length,
            "date_from_formatted": date_from_formatted,
            "date_to_formatted": date_to_formatted,
        },
    )


@router.post("/successful_booking", response_class=HTMLResponse)
async def get_successful_booking_page(
    request: Request, user: Users = Depends(get_current_user)):#, _=Depends(add_booking)):
    data = await request.form()
    booking = SNewBooking(**dict(data))
    booking = await BookingDAO.add(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )
    if not booking:
        raise RoomCannotBeBooked
    
    # импорт зависимостей для Celery, ссответвующий код...
    # редирект с кодом 303 чтоб редиректнул на другую страницу, а не только что загруженный ресурс, и соответвенно это будет GET запрос
    response = RedirectResponse('/pages/bookings', status_code=303)
    return response
    
    # return templates.TemplateResponse(
    #     "bookings/booking_successful.html", {"request": request}
    # )


@router.get("/bookings", response_class=HTMLResponse)
async def get_bookings_page(
    request: Request,
    bookings=Depends(get_bookings),
):
    return templates.TemplateResponse(
        "bookings/bookings.html",
        {
            "request": request,
            "bookings": bookings,
            "format_number_thousand_separator": format_number_thousand_separator,
        },
    )
