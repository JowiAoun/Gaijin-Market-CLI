from pydantic import BaseModel

from typing import Optional, Any
from enum import Enum

class SettingsKey(Enum):
  REQUESTS_ITEMS = "requests_items"
  BUY_MAX = "buy_max"
  BUY_MIN = "buy_min"
  ROI_MAX = "roi_max"
  ROI_MIN = "roi_min"
  BANNED = "banned"


class GaijinMarketSettings(BaseModel):
  requests_items: Optional[int] = None  # Number of items returned from 1 request
  buy_max: Optional[float] = None  # Maximum item buy value
  buy_min: Optional[float] = None  # Minimum item buy value
  roi_max: Optional[float] = None  # Maximum item ROI
  roi_min: Optional[float] = None  # Minimum item ROI
  banned: Optional[list[str]] = None  # Banned items list

  def get(self, key: SettingsKey) -> Any:
    """
    Returns the value of the specified attribute by key.
    If the key does not exist, raises an AttributeError.
    """
    if hasattr(self, key.value):
      return getattr(self, key.value)
    else:
      raise AttributeError(f"'GaijinMarketSettings' object has no attribute '{key.value}'")


  def set(self, key: SettingsKey, value: Any) -> Any:
    """
    Sets the value of the specified attribute by key.
    If the key does not exist, raises an AttributeError.
    """
    if hasattr(self, key.value):
      setattr(self, key.value, value)
    else:
      raise AttributeError(f"'GaijinMarketSettings' object has no attribute '{key.value}'")
