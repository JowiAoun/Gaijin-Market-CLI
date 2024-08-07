from pydantic import BaseModel, Field
from datetime import datetime
from gmcli.models.items.tags.TagCollection import TagCollection


class Item(BaseModel):
  """
  Class representing an item from the Gaijin market.
  """
  cvalue: int = None
  id: int = None  # Unique identifier for each Gaijin Market item
  name: str = None
  hash_name: str = None
  price_buy: float = None
  price_sell: float = None
  quantity_buy: int = None
  quantity_sell: int = None
  marketable: bool = None
  tags: TagCollection = Field(default_factory=lambda: TagCollection())
  timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp()))

  class Config:
    arbitrary_types_allowed = True

  @property
  def profit(self) -> float:
    return (0.85 * self.price_sell) - self.price_buy
  @property
  def roi(self) -> int:
    return int((self.profit / self.price_buy) * 100)

  def __str__(self):
    return f"Item with id {self.id} and asset_id {self.cvalue} and tags [{self.tags}]"
