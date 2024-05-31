import os
import json

from pydantic import BaseModel, Field

from gmcli.models.Receipt import Receipt
from gmcli.models.Item import Item
from gmcli.models.GaijinMarket import GaijinMarket


class User(BaseModel):
  id: int = -1
  token: str = ""
  balance: float = -1
  inventory: list[Item] = []
  receipts: list[Receipt] = []
  settings: dict = {}
  market: GaijinMarket = Field(default_factory=lambda: GaijinMarket())

  class Config:
    arbitrary_types_allowed = True

  def __init__(self, **data):
      super().__init__(**data)
      self.load_from_file_if_exists()

  def get_balance(self) -> float:
    """
    Gets the balance of the user. If successful, returns a float.
    """

    bal = self.market.get_balance(self.token)
    self.balance = bal
    self.save()
    return bal

  def get_inventory(self) -> dict:
    """
    Gets the balance of the user. If successful, returns a float.
    """

    return self.market.get_inventory(self.token)

  def get_open_orders(self) -> list[tuple]:
    """
    Gets current open orders. Returns a list of tuples with data organized like so:
    (transact_id, order_id, pair_id, hash_name, type, price, amount, timestamp)
    """

    return self.market.get_open_orders(self.token)

  def create_order(self):
    """
    Creates an order for an item.
    """

  def cancel_order(self, receipt: Receipt) -> bool:
    """
    Cancels the user's open order using the item's receipt.
    """

    return self.market.cancel_order(self.token, receipt)

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
    self.token = token
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
    """
    filename: str = f"./gmcli/users/{self.id}.json"
    if (self.id != -1) and (os.path.exists(filename)):
      with open(filename, 'r') as f:
        data = json.load(f)
      for key, value in data.items():
        setattr(self, key, value)
