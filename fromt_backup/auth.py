from datetime import date, datetime, timedelta
from fastapi import responses
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.bookings.router import add_booking, get_bookings
from app.hotels.rooms.router import get_rooms_by_time
from app.hotels.router import get_hotel_by_id, get_hotels_by_location_and_time
from app.utils import format_number_thousand_separator, get_month_days
from app.exceptions import CannotAddDataToDatabase, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.router import login_user
from app.users.dao import UserDAO


router = APIRouter(
    # prefix="/",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")



# @router.get("/login", response_class=HTMLResponse)
# async def get_login_page(request: Request):
#     form = await request.form()
#     form_register_data = {
#             'email': form.get('email'),
#             'password': form.get('password'),
#         }
    
#     return templates.TemplateResponse("auth/login.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
@router.post("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    if request.method == "POST":
        form = await request.form()
        form_register_data = {
            'email': form.get('email'),
            'password': form.get('password'),
        }
        user = await authenticate_user(form_register_data.get('email'), form_register_data.get('password'))
        access_token = create_access_token({"sub": str(user.id)})
        response = RedirectResponse("/bookings", status_code=302)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="Lax",
            secure=True,
        )
        return response
        #return responses.RedirectResponse('/bookings', status_code=303)
        # print(access_token)
        # response = RedirectResponse('/login')
        # response.set_cookie("booking_access_token", access_token, httponly=True, samesite="none", secure=True)
        # token = request.cookies.get("booking_access_token")
        # print(token)
        # return responses.RedirectResponse('/bookings', status_code=303)
    if request.method == 'GET':
        return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
@router.post("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    if request.method == 'POST':
        form = await request.form()#await request.form()
        #print(form)
        form_register_data = {
            'email': form.get('email'),
            'password': form.get('password'),
        }
        #print(form_register_data)
        existing_user = await UserDAO.find_one_or_none(email=form_register_data.get('email'))
        if existing_user:
            raise UserAlreadyExistsException
        hashed_password = get_password_hash(form_register_data.get('password'))
        new_user = await UserDAO.add(email=form_register_data.get('email'), hashed_password=hashed_password)
        if not new_user:
            raise CannotAddDataToDatabase
        return responses.RedirectResponse('/login', status_code=303)
    if request.method == 'GET':
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
    request: Request,
    _=Depends(add_booking),
):
    return templates.TemplateResponse(
        "bookings/booking_successful.html", {"request": request}
    )


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
