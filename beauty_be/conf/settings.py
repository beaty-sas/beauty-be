from enum import Enum

from pydantic_settings import BaseSettings
from sqlalchemy.engine.url import URL


class LogLevel(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class Env(str, Enum):
    LOCAL = 'LOCAL'
    STAGING = 'STAGING'
    PRODUCTION = 'PRODUCTION'


class Settings(BaseSettings):
    DEBUG: bool = False
    ENV: Env = Env.LOCAL
    PORT: int = 4000
    LOG_LEVEL: LogLevel = LogLevel.INFO
    ALLOWED_ORIGINS: str = 'http://localhost http://localhost:5173 http://127.0.0.1:3000'

    DB_USER: str = 'postgres'
    DB_PASS: str = 'postgres'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_NAME: str = 'postgres'
    DB_DRIVER: str = 'postgresql+asyncpg'

    DEFAULT_DATE_FORMAT: str = '%Y-%m-%d'
    DEFAULT_BOOKING_TIME_STEP: int = 3600

    AUTH0_URL: str = 'https://reserve-exp.eu.auth0.com'

    S3_BUCKET_NAME: str = 'reserve-attachemtns'
    AWS_DEFAULT_REGION: str = 'eu-central-1'
    AWS_ACCESS_KEY_ID: str = ''
    AWS_SECRET_ACCESS_KEY: str = ''
    SQS_SMS_NOTIFICATION_QUEUE: str = ''

    @property
    def sqlalchemy_database_uri(self):
        return URL.create(
            drivername=self.DB_DRIVER,
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )


settings = Settings()
