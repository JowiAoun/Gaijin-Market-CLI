from pydantic import BaseModel, Field

import os
import json

from gmcli.models.Receipt import Receipt
from gmcli.models.GaijinMarketSettings import GaijinMarketSettings
from gmcli.models.UserMarketCache import UserMarketCache
from gmcli.models.GaijinMarket import GaijinMarket


class User(BaseModel):
  id: int = None
  cache: UserMarketCache = Field(default_factory=lambda: UserMarketCache())
  market: GaijinMarket = Field(default_factory=lambda: GaijinMarket())
  market_settings: GaijinMarketSettings = Field(default_factory=lambda: GaijinMarketSettings())

  def __init__(self, **data):
      super().__init__(**data)
      self.load_from_file_if_exists()

  def get_balance(self) -> float:
    """
    Gets the balance of the user. If successful, returns a float.
    If unsuccessful, returns -1.
    """

    new_balance = self.market.get_balance(self.cache.get_token())

    if new_balance == -1:
      return new_balance

    self.cache.set_balance(new_balance)
    self.save()
    return new_balance

  def get_inventory(self) -> dict:
    """
    Gets the balance of the user. If successful, returns a float.
    """

    return self.market.get_inventory_ids(self.cache.get_token())

  def dev_test(self):
    """
    Development testing command
    """
    return self.market.get_item_static(self.cache.get_token(), 100124)

  def get_open_orders(self) -> list[tuple]:
    """
    Gets current open orders. Returns a list of tuples with data organized like so:
    (transact_id, order_id, pair_id, hash_name, type, price, amount, timestamp)
    """

    return self.market.get_open_orders(self.cache.get_token())

  def create_order(self):
    """
    Creates an order for an item.
    """

  def cancel_order(self, receipt: Receipt) -> bool:
    """
    Cancels the user's open order using the item's receipt.
    """

    return self.market.cancel_order(self.cache.get_token(), receipt)

  def cancel_orders(self, receipts: list[Receipt]) -> bool:
    """
    Cancels the selected user's open order using the items receipts.
    """

    for receipt in receipts:
      if not self.cancel_order(receipt):
        return False

    return True

  def cancel_orders_all(self):
    for receipt in self.receipts:
      if not self.cancel_order(receipt):
        return False

    return True

  def set_token(self, token: str):
    self.cache.set_token(token)
    self.save()

  def set_market_settings(self, market_settings: GaijinMarketSettings):
    self.market_settings = market_settings
    self.save()

  def save(self):
    """
    Saves the user's attributes to a JSON file.
    """
    with open(f"./gmcli/users/{self.id}.json", 'w') as f:
      f.write(self.json(exclude={"market"}))

  def load_from_file_if_exists(self):
    """
    Loads the user's attributes from a JSON file if it exists.
    Returns true if file exists, else false
    """
    filename: str = f"./gmcli/users/{self.id}.json"

    if (self.id is not None) and (os.path.exists(filename)):
      with open(filename, 'r') as f:
        data = json.load(f)

      # Convert dictionaries to models
      if 'cache' in data and isinstance(data['cache'], dict):
        data['cache'] = UserMarketCache.parse_obj(data['cache'])
      if 'market_settings' in data and isinstance(data['market_settings'], dict):
        data['market_settings'] = GaijinMarketSettings.parse_obj(data['market_settings'])

      self.__dict__.update(data)
