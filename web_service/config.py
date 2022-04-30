from pydantic import BaseSettings


class ServiceConfig(BaseSettings):

    channel_name: str
    redis_host: str = '127.0.0.1'
    influxdb_host: str = '127.0.0.1'
    influxdb_db: str
    influxdb_admin_user: str
    influxdb_admin_password: str
