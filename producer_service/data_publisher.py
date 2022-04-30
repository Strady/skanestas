import dataclasses
import json
import typing
import redis
import ticker_data


class Producer(typing.Protocol):

    def get_prices(self) -> list[ticker_data.TickerData]:
        ...


class DataPublisher:

    def __init__(self, redis_host: str, channel_name: str, producer: Producer) -> None:
        self._channel_name = channel_name
        self._producer: Producer = producer
        self._redis_client = redis.Redis(host=redis_host)

    def publish_prices_data(self) -> None:
        """
        Published prices into specified channel
        """
        json_data = [dataclasses.asdict(price_data) for price_data in self._producer.get_prices()]
        self._redis_client.publish(channel=self._channel_name, message=json.dumps(json_data).encode())
