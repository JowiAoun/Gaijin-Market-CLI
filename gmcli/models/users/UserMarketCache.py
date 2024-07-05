from pydantic import BaseModel

from typing import Optional
from datetime import datetime

from gmcli.models.items.transactions.Receipt import Receipt
from gmcli.models.items.Item import Item


class UserMarketCache(BaseModel):
  token: Optional[tuple[datetime, str]] = None
  balance: Optional[tuple[datetime, float]] = None
  inventory: Optional[tuple[datetime, list[Item]]] = None
  receipts: Optional[tuple[datetime, list[Receipt]]] = None

  def get_token(self) -> str | None:
    if self.token is None:
      return None
    return self.token[1]

  def get_token_time(self) -> datetime | None:
    if self.token is None:
      return None
    return self.token[0]

  def set_token(self, val: str):
    self.token = (datetime.now(), val)

  def get_balance(self) -> float | None:
    if self.balance is None:
      return None
    return self.balance[1]

  def get_balance_time(self) -> datetime | None:
    if self.balance is None:
      return None
    return self.balance[0]

  def set_balance(self, val: float):
    self.balance = (datetime.now(), val)

  def decrease_balance(self, val: float):
    self.set_balance(self.balance[1] - val)
