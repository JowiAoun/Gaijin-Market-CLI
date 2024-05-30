from pydantic import BaseModel

from gmcli.models.GaijinMarket import GaijinMarket
from gmcli.models.Receipt import Receipt
from gmcli.models.Item import Item

class User(BaseModel):
  token: str = ""
  id: int = -1
  balance: float = -1
  inventory: list[Item] = []
  receipts: list[Receipt] = []
  settings: dict = {}
  market: GaijinMarket = GaijinMarket(token=token)

  def get_balance(self) -> float:
    """
    Gets the balance of the user. If successful, returns a float.
    """

    return self.market.get_balance()

  def get_inventory(self) -> dict:
    """
    Gets the balance of the user. If successful, returns a float.
    """

    return self.market.get_inventory()

  def get_open_orders(self) -> list[tuple]:
    """
    Gets current open orders. Returns a list of tuples with data organized like so:
    (transact_id, order_id, pair_id, hash_name, type, price, amount, timestamp)
    """

    return self.market.get_open_orders()

  def create_order(self):
    """
    Creates an order for an item.
    """

  def cancel_order(self, receipt: Receipt) -> bool:
    """
    Cancels the user's open order using the item's receipt.
    """

    return self.market.cancel_order(receipt)

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
