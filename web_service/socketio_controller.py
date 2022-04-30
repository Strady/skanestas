import typing

from models import TickerData


class Emitter(typing.Protocol):

    def emit(self, event: str, *args, **kwargs) -> None:
        ...


class SocketIOController:

    def __init__(self, emitter: Emitter):
        self._emitter: Emitter = emitter

    def emit_data(self, tickers_data: list[TickerData], timestamp: int) -> None:
        """
        Emits data via using provided emitter
        """
        self._emitter.emit('prices', self._prepare_data(tickers_data=tickers_data, timestamp=timestamp))

    @staticmethod
    def _prepare_data(tickers_data: list[TickerData], timestamp: int) -> dict:
        """
        Formats data before emitting
        """
        return {ticker_data.name: [timestamp, ticker_data.price] for ticker_data in tickers_data}