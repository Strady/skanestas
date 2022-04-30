import dataclasses


@dataclasses.dataclass
class TickerData:
    """
    Container for current
    financial instrument state
    """
    name: str
    price: int = 0
