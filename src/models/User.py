import GaijinMarket
import Receipt
import Item

class User:
  def __init__(self, token: str):
    self.token: str = token
    self.balance: float = 0
    self.inventory: list[Item] = []
    self.receipts: list[Receipt] = []
    self.market: GaijinMarket = GaijinMarket.GaijinMarket(self.token)

  def get_balance(self) -> float:
    """
    Gets the balance of the user. If successful, returns a float.
    """

    return self.market.get_balance()

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
