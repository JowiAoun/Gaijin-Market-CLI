# --- Imports
from classes import Item  # class to preserve a market item
from http import client  # used to make API requests
from dotenv import load_dotenv  # used in loading .env file
import sqlite3
from datetime import datetime  # used to define the timestamp of requested GM items
import json  # used to load settings from settings.json
import os  # used in setting environment variables

# --- Setup
load_dotenv()  # load environment variables
with open('../db/queries.sql', 'r') as file:  # read SQL querries
  sql_content = file.read()
queries = [query.split('\n', 1)[1].strip() for query in sql_content.split('-- #') if query.strip()]

# --- Constants
STGS = json.load(open('../settings.json', 'r'))  # set settings from .json file
GM_TOKEN = os.environ.get("GM_TOKEN")  # get token from .env (SECRET)
conn = sqlite3.connect('../db/gmcli.db')
cursor = conn.cursor()


# --- General functions
def get_balance() -> float:
  """
    Gets the balance of the user.
    If successful, returns a float.
    """

  # Get data
  conn = client.HTTPSConnection("wallet.gaijin.net")
  headers = {'Authorization': f'BEARER {GM_TOKEN}'}
  conn.request("GET", "/GetBalance", '', headers)
  res = conn.getresponse()
  data = json.loads(res.read())
  conn.close()

  # Check if status is good
  if (data["status"] != "OK"):
    print(f"ERROR: could not get balance.\nStatus: {data['status']}")
    return -1
  else:
    return float(data["balance"]) / 10000


def get_open_orders() -> list[tuple]:
  """
    Gets current open orders. Returns a list of tuples with data organized like so:
    (transact_id, order_id, pair_id, hash_name, type, price, amount, timestamp).
    """

  conn = client.HTTPSConnection("market-proxy.gaijin.net")
  payload = f"action=cln_get_user_open_orders&token={GM_TOKEN}&appid=1165"
  headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
  conn.request("POST", "/web", payload, headers)
  res = conn.getresponse()
  data = json.loads(res.read())
  conn.close()

  open_orders = []

  if (data['success'] != True):
    print("ERROR: Could not make request for open orders.")
    return []

  for item in data['response']:
    try:
      open_orders.append((int(item['txId']), int(item['id']), int(item['pairId']), item['market'], item['type'],
                          round(int(item['localPrice']) / 10000, 2), int(item['amount']), item['time']))
    except:
      print(f"ERROR: Could not get item in open orders with ID: {item['id']}")

  return open_orders


def cancel_order(transact_id: int, order_id: int, pair_id: int) -> bool:
  """
    Cancels an open order using the item's order ids.
    """

  timestamp = datetime.now().timestamp()

  conn = client.HTTPSConnection("market-proxy.gaijin.net")
  payload = f"action=cancel_order&token={GM_TOKEN}&appid=1165&transactid={transact_id}&reqstamp={timestamp}&pairId={pair_id}&orderId={order_id}"
  headers = {'accept': 'application/json, text/javascript, */*; q=0.01', 'accept-language': 'en-CA,en;q=0.8',
             'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
  conn.request("POST", "/market", payload, headers)
  res = conn.getresponse()
  data = json.loads(res.read())
  conn.close()

  if data["response"]["success"] != True:
    return False
  else:
    return True


def cancel_orders() -> bool:
  """
    Cancels all orders using each item's order ids.
    """

  pass


def create_order() -> bool:
  """
    Creates an order for an item.
    """

  pass


def get_item_variable_data(hash_name: str) -> tuple:
  """
    Gets variable data for a single item by its hash name.
    Returns a tuple with data organized like so:
    (price_buy_list, price_sell_list, quantity_buy, quantity_sell, profit, roi, timestamp).
    """

  conn = client.HTTPSConnection("market-proxy.gaijin.net")
  payload = f"action=cln_books_brief&token={GM_TOKEN}&appid=1067&market_name={hash_name}"
  headers = {'accept': 'application/json, text/javascript, */*; q=0.01',
             'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
  conn.request("POST", "/web", payload, headers)
  res = conn.getresponse()
  data = json.loads(res.read())
  conn.close()

  if (data['response']['success'] != True):
    print("ERROR: Could not make request for item variable data.")
    return ()

  try:
    price_buy_list = data['response']['BUY']
    price_sell_list = data['response']['SELL']
    quantity_buy = data['response']['depth']['BUY']
    quantity_sell = data['response']['depth']['SELL']
    profit = round((0.85 * price_sell_list[0][0] / 10000) - price_buy_list[0][0] / 10000, 2)
    roi = int((profit / price_buy_list[0][0] / 10000) * 100)
    timestamp = int(datetime.now().timestamp())
    return (price_buy_list, price_sell_list, quantity_buy, quantity_sell, profit, roi, timestamp)

  except:
    print(f"ERROR: Could not get item variable data for hash name: {hash_name}")
    return ()


def get_items_static_data() -> list[tuple]:
  """
    Returns a list of tuples containing static data in the order:
    (asset_id, name, hash_name).
    """

  conn = client.HTTPSConnection("market-proxy.gaijin.net")  # setup connection
  count = 100
  skip = 0

  for i in range(STGS['requests']):
    # Get data
    payload = f"action=cln_market_search&token={GM_TOKEN}&appid=1165&skip={skip}&count={count}&text=&language=en_US&options=any_sell_orders&appid_filter=1067"
    headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8"}
    conn.request("GET", "/web", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read())

    # Iterate over each item in the request and add to list
    ids_mapping = []
    for j in range(count):
      try:
        asset_id = int(data['response']['assets'][j]["asset_class"][0]["value"])
        name = data['response']['assets'][j]['name']
        hash_name = data['response']['assets'][j]['hash_name']
        ids_mapping.append((asset_id, name, hash_name))

      except:
        print(f"ERROR: could not get market id: {asset_id, name, hash_name} at loop index {i * 100 + j}")
        continue

    skip += 100

  conn.close()
  return ids_mapping


def get_items_variable_data() -> list[tuple]:
  """
    Returns a list of tuples containing variable data in the order:
    (asset_id, price_buy, price_sell, quantity_buy, quantity_sell, profit, roi, timestamp).
    """

  conn = client.HTTPSConnection("market-proxy.gaijin.net")  # setup connection
  count = 100
  skip = 0

  for i in range(STGS['requests']):
    # Get data
    payload = f"action=cln_market_search&token={GM_TOKEN}&appid=1165&skip={skip}&count={count}&text=&language=en_US&options=any_sell_orders&appid_filter=1067"
    headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8"}
    conn.request("GET", "/web", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read())

    # Get timestamp once
    timestamp = int(datetime.now().timestamp())

    # Iterate over each item in the request and add to list
    variable_data = []
    for j in range(count):
      try:
        asset_id = int(data['response']['assets'][j]["asset_class"][0]["value"])
        price_buy = data['response']['assets'][j]['buy_price'] / 100000000
        price_sell = data['response']['assets'][j]['price'] / 100000000
        quantity_buy = data['response']['assets'][j]['depth']
        quantity_sell = data['response']['assets'][j]['buy_depth']
        profit = round((0.85 * price_sell) - price_buy, 2)
        roi = int((profit / price_buy) * 100)
        variable_data.append((asset_id, price_buy, price_sell, quantity_buy, quantity_sell, profit, roi, timestamp))

      except:
        print(f"ERROR: could not get market id: {asset_id} at loop index {i * 100 + j}")
        continue

    skip += 100

  conn.close()
  return variable_data


def get_items_inventory_data() -> dict:
  """
    Returns a dictionary in key-value form,
    where the 'item_id' is the static ID of the item,
    and 'class_id' is the ID given to the item while in the inventory.
    The 'class_id' changes after transactions are done with it.
    """

  # Get data
  conn = client.HTTPSConnection("market-proxy.gaijin.net")
  payload = f"action=GetContextContents&token={GM_TOKEN}&appid=1067&contextid=1"
  headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
  conn.request("POST", "/assetAPI", payload, headers)
  res = conn.getresponse()
  data = json.loads(res.read())

  # Create mapping for itemid-classid
  ids_mapping = {}
  for item in data["result"]["assets"]:
    class_value = item["class"][0]["value"]
    if class_value in ids_mapping:
      ids_mapping[class_value].append(int(item["id"]))
    else:
      ids_mapping[class_value] = int([item["id"]])

  # Check is status is good
  if (data["result"]["success"] != True):
    print(f"ERROR: could not get inventory IDs.\nStatus: {data['result']['success']}")
    exit()

  conn.close()
  return ids_mapping


# --- Database functions
def db_get_hash_by_id(asset_id: int):
  """
    Returns the item's hash_name by its argument asset_id from the database.
    """
  cursor.execute(queries[3].format(asset_id))
  return cursor.fetchone()[0]


def db_populate_items_static():
  static_data = get_items_static_data()

  for i in static_data:
    cursor.execute(queries[0].format(i[0], i[1], i[2]))

  conn.commit()


def db_populate_items_variable():
  variable_data = get_items_variable_data()

  for i in variable_data:
    cursor.execute(queries[1].format(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))

  conn.commit()


def db_populate_items_inventory():
  ids_mapping = get_items_inventory_data()

  for i in ids_mapping:
    cursor.execute(queries[2].format(i, json.dumps(ids_mapping[i]), len(ids_mapping[i])))

  conn.commit()

# ? Next steps:
# ? DONE - 1. Put static information into new database table (asset_id, name, hash_name)
# ? DONE - 2. Link that table to another table containing variable data
# ?    (price_buy, price_sell, quantity_buy, quantity_sell, profit, roi, timestamp)
# ? 3. Add a tags table, link to asset_id from items_static
# ?    (should be populated along with db_populate_items_static simultanously)
# ? 4. Learn how to write formal python unit tests, and create one which does:
# ?    Opens an order for an item and cancels the order for the item (add delays and in-between checks)