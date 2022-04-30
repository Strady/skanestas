import pydantic


class TickerData(pydantic.BaseModel):
    """
    Financial instrument current data container
    """
    name: str
    price: int
