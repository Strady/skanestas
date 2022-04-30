import random
from ticker_data import TickerData


class PricesProducer:

    def __init__(self, tickers_number) -> None:
        self._prices: list[TickerData] = [
            TickerData(name=f'ticker_{str(i).zfill(2)}') for i in range(tickers_number)
        ]

    def get_prices(self) -> list[TickerData]:
        """
        Updates and returns fake prices
        """
        self._update_prices()
        return self._prices

    def _update_prices(self) -> None:
        """
        Updates fake prices
        """
        for tp in self._prices:
            tp.price += -1 if random.random() < 0.5 else 1
