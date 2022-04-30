from pydantic import BaseSettings


class ServiceConfig(BaseSettings):

    channel_name: str
    tickers_number: int = 100
    redis_host: str = '127.0.0.1'
