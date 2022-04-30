import datetime
import threading
import typing

import pydantic
import redis

from models import TickerData


class Action(typing.Protocol):

    def __call__(self, tickers_data: list[TickerData], timestamp: int) -> None:
        ...


class RedisListener(threading.Thread):

    def __init__(self,
                 redis_host: str,
                 redis_channel: str,
                 actions: typing.Iterable[Action] = ()
                 ) -> None:
        super(RedisListener, self).__init__()
        redis_client = redis.Redis(host=redis_host)
        self.pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
        self.pubsub.subscribe(redis_channel)
        self._actions = actions

    def run(self) -> None:
        """
        Runs main subscriber loop. Executes actions when gets a message
        """
        for message in self.pubsub.listen():
            timestamp = int(datetime.datetime.now().timestamp())
            tickers_data: list[TickerData] = pydantic.parse_raw_as(list[TickerData], message['data'])
            for action in self._actions:
                action(tickers_data=tickers_data, timestamp=timestamp)




