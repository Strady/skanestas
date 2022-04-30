import datetime

from influxdb import InfluxDBClient

from models import TickerData


class InfluxDBController:

    def __init__(self, host: str, database: str, username: str, password: str):
        self._client = InfluxDBClient(
            host=host,
            port=8086,
            username=username,
            password=password,
            database=database
        )

    def get_tickers_list(self) -> list[str]:
        """
        Gets instruments names list from storage
        """
        return [point['name'] for point in self._client.query('SHOW MEASUREMENTS').get_points()]

    def get_ticker_data(self, ticker_name) -> list[dict]:
        """
        Requests stored prices from storage for specified instrument
        """
        return list(self._client.query(f'SELECT * FROM {ticker_name}').get_points())

    def write_tickers_data(self, tickers_data: list[TickerData], timestamp: int) -> None:
        """
        Writes prices data into storage
        """
        point_time = datetime.datetime.fromtimestamp(timestamp).isoformat()
        points = [
            self._create_point(point_data=ticker_data, point_time=point_time)
            for ticker_data in tickers_data
        ]
        self._client.write_points(points=points)

    @staticmethod
    def _create_point(point_data: TickerData, point_time: str) -> dict:
        """
        Formats data to write into storage
        """
        return {
            "measurement": point_data.name,
            "time": point_time,
            "fields": {
                "price": point_data.price
            }
        }
