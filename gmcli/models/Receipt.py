from pydantic import BaseModel

class Receipt(BaseModel):
  transact_id: int
  order_id: int
  pair_id: int
