from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import root_validator
import sys
from os.path import abspath, dirname

sys.path.insert(0, dirname(dirname(abspath(__file__))))

class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Рабочий, но весьма уродливый способ забирать данные с класса и снова возвращать их методу с помощью штатного декоратора
    # @root_validator
    # def get_database_url(cls, v):
    #     v["DATABASE_URL"] = f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
    #     return v

    # Гораздо более лаконичный способ с свойством @property

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def TEST_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    SENTRY_DSN: str

    SECRET_KEY: str
    ALGORITHM: str

    # Со 2 версии Pydantic вместо class Config теперь атрибут model_config
    # class Config:
    #     env_file = ".env"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

