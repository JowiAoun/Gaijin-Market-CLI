from src.view import View
from src.models.User import User
from dotenv import load_dotenv
import os
import json

class Controller:
  def __init__(self):
    load_dotenv()
    self.view = View()

  def launch(self):
    token = os.environ.get("GM_TOKEN")
    settings = json.load(open('settings.json', 'r'))
    user = User(token, settings)

    print("Balance: $" + str(user.get_balance()))
