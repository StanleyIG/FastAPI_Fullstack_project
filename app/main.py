from contextlib import asynccontextmanager
import time

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.images.router import router as router_images
from app.importer.router import router as router_import
from app.logger import logger
from app.pages.router import router as router_pages
from app.users.router import router_auth, router_users

app = FastAPI(
    title="Бронирование Отелей",
    version="0.1.0",
    root_path="/api",
)



# подключение роутеров
app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)

app.include_router(router_images)
app.include_router(router_import)


# Подключение CORS, чтобы запросы к API могли приходить из браузера 
origins = [
    # порт 3000 для React.js например
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    "подключение Redis"

    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

    
app.include_router(router_pages)

# Подключение статики
app.mount("/static", StaticFiles(directory="app/static"), "static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response


if __name__ == "__main__":
    import uvicorn

    import os.path
    import sys
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    uvicorn.run(
        app="app.main:app",
        reload=True,
    )