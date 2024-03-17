from datetime import datetime

class Item:
  """
  Class representing an item from the Gaijin market.
  """

  def __init__(self, asset_id, name, hash_name, price_buy=None, price_sell=None,
               quantity_buy=None, quantity_sell=None, tags=None) -> None:
    self.asset_id: int = asset_id
    self.name: str = name
    self.hash_name: str = hash_name
    self.price_buy: float = price_buy
    self.price_sell: float = price_sell
    self.quantity_buy: int = quantity_buy
    self.quantity_sell: int = quantity_sell
    self.tags: dict = tags
    self.profit: float = (0.85 * price_sell) - price_buy
    self.roi: int = (self.profit / price_buy) * 100
    self.timestamp: int = int(datetime.now().timestamp())
