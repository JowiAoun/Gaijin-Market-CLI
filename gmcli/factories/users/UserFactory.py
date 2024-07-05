import os
import json

from gmcli.models.users.UserMarketCache import UserMarketCache
from gmcli.models.gaijinMarket.GaijinMarketSettings import GaijinMarketSettings

from gmcli.models.users.User import User

class UserFactory:
  @staticmethod
  def create_from_id(user_id: int) -> User:
    """
    Creates a User object from a JSON file based on user ID.
    """
    filename: str = f"./gmcli/users/{user_id}.json"

    if not os.path.exists(filename):
      raise FileNotFoundError(f"User file not found for ID {user_id}")

    with open(filename, 'r') as f:
      data = json.load(f)

    # Convert dictionaries to models
    if 'cache' in data and isinstance(data['cache'], dict):
      data['cache'] = UserMarketCache.parse_obj(data['cache'])
    if 'market_settings' in data and isinstance(data['market_settings'], dict):
      data['market_settings'] = GaijinMarketSettings.parse_obj(data['market_settings'])

    return User(**data)
