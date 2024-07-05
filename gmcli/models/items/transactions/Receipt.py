from pydantic import BaseModel

class Receipt(BaseModel):
  # Do we need itemId?
  transact_id: int
  order_id: int
  pair_id: int
