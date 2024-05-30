from pydantic import BaseModel, Field
from datetime import datetime

class Item(BaseModel):
  """
  Class representing an item from the Gaijin market.
  """
  asset_id: int
  name: str
  hash_name: str
  price_buy: float
  price_sell: float
  quantity_buy: int
  quantity_sell: int
  tags: dict
  timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp()))

  @property
  def profit(self) -> float:
    return (0.85 * self.price_sell) - self.price_buy
  @property
  def roi(self) -> int:
    return int((self.profit / self.price_buy) * 100)
