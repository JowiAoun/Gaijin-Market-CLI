import math
from http import client
import json
from datetime import datetime
from .Receipt import Receipt

class GaijinMarket:
  def __init__(self, token: str):
    self.token: str = token
    self.conn_market: client.HTTPSConnection = client.HTTPSConnection("market-proxy.gaijin.net")
    self.conn_wallet: client.HTTPSConnection = client.HTTPSConnection("wallet.gaijin.net")

  def get_balance(self) -> float:
    headers = {'Authorization': f'BEARER {self.token}'}
    self.conn_wallet.request("GET", "/GetBalance", '', headers)
    res = self.conn_wallet.getresponse()
    data = json.loads(res.read())

    if data["status"] != "OK":
      print(f"ERROR: could not get balance.\nStatus: {data['status']}")
      return -1
    else:
      return float(data["balance"]) / 10000

  def get_open_orders(self) -> list[tuple]:
    payload = f"action=cln_get_user_open_orders&token={self.token}&appid=1165"
    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    self.conn_market.request("POST", "/web", payload, headers)
    res = self.conn_market.getresponse()
    data = json.loads(res.read())

    open_orders = []

    if not data['response']['success']:
      print("ERROR: Could not make request for open orders.")
      return []

    for item in data['response']:
      try:
        open_orders.append((int(item['txId']), int(item['id']), int(item['pairId']), item['market'], item['type'],
                            round(int(item['localPrice']) / 10000, 2), int(item['amount']), item['time']))
      except Exception as err:
        print(f"ERROR: Could not get item in open orders with ID: {item['id']}")
        print(err)

    return open_orders

  def get_inventory(self) -> dict:
    """
    Returns a dictionary in key-value form,
    where the 'item_id' is the static ID of the item,
    and 'class_id' is the ID given to the item while in the inventory.
    The 'class_id' changes after transactions are done with it.
    """

    payload = f"action=GetContextContents&token={self.token}&appid=1067&contextid=1"
    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    self.conn_market.request("POST", "/assetAPI", payload, headers)
    _res = self.conn_market.getresponse()
    res = json.loads(_res.read())

    data = {}
    for item in res["result"]["assets"]:
      class_value = item["class"][0]["value"]
      if class_value in data:
        data[class_value].append(int(item["id"]))
      else:
        data[class_value] = int(item["id"])

    if not res["result"]["success"]:
      print(f"ERROR: could not get inventory IDs.\nStatus: {data['result']['success']}")
      return {}

    return data

  def get_item_variable(self, hash_name: str) -> tuple:
    """
    Gets variable data for a single item by its hash name.
    Returns a tuple with data organized like so:
    (price_buy_list, price_sell_list, quantity_buy, quantity_sell, profit, roi, timestamp).
    """

    payload = f"action=cln_books_brief&token={self.token}&appid=1067&market_name={hash_name}"
    headers = {'accept': 'application/json, text/javascript, */*; q=0.01',
               'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    self.conn_market.request("POST", "/web", payload, headers)
    res = self.conn_market.getresponse()
    data = json.loads(res.read())

    if not data['response']['success']:
      print(f"ERROR: Could not get item variable data for hash name: {hash_name}")
      return ()

    try:
      price_buy_list = data['response']['BUY']
      price_sell_list = data['response']['SELL']
      quantity_buy = data['response']['depth']['BUY']
      quantity_sell = data['response']['depth']['SELL']
      profit = round((0.85 * price_sell_list[0][0] / 10000) - price_buy_list[0][0] / 10000, 2)
      roi = int((profit / price_buy_list[0][0] / 10000) * 100)
      timestamp = int(datetime.now().timestamp())
      return price_buy_list, price_sell_list, quantity_buy, quantity_sell, profit, roi, timestamp

    except:
      print(f"ERROR: Could not get item variable data for hash name: {hash_name}")
      return ()

  def get_items_static(self, count: int) -> list[tuple]:
    """
    Returns a list of tuples containing static data in the order:
    (asset_id, name, hash_name).
    """

    data = []
    num_requests = math.ceil(count / 100)
    skip = 0

    for _ in range(num_requests):
      curr_count = min(100, count)

      payload = f"action=cln_market_search&token={self.token}&appid=1165&skip={skip}&count={curr_count}&text=&language=en_US&options=any_sell_orders&appid_filter=1067"
      headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8"}
      self.conn_market.request("GET", "/web", payload, headers)
      res = self.conn_market.getresponse()
      data = json.loads(res.read())

      if data['response']['error'] == "LIMIT_IS_EXCEEDED":
        break
      elif not data['response']['success']:
        continue

      for j in range(count):
        try:
          asset_id = int(data['response']['assets'][j]["asset_class"][0]["value"])
          name = data['response']['assets'][j]['name']
          hash_name = data['response']['assets'][j]['hash_name']
          data.append((asset_id, name, hash_name))

        except Exception as err:
          print(f"ERROR: could not get market id: {asset_id} at loop index UNKNOWN")
          print(err)
          continue

      skip = curr_count
      count -= curr_count

    return data

  def get_items_variable(self, count: int) -> list[tuple]:
    """
    Gets variable data for a single item by its hash name.
    Returns a tuple with data organized like so:
    (price_buy_list, price_sell_list, quantity_buy, quantity_sell, profit, roi, timestamp).
    """

    data = []
    skip = 0
    num_requests = math.ceil(count / 100)
    timestamp = int(datetime.now().timestamp())

    for _ in range(num_requests):
      curr_count = min(100, count)

      payload = f"action=cln_market_search&token={self.token}&appid=1165&skip={skip}&count={curr_count}&text=&language=en_US&options=any_sell_orders&appid_filter=1067"
      headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8"}
      self.conn_market.request("GET", "/web", payload, headers)
      res = self.conn_market.getresponse()
      data = json.loads(res.read())

      if data['response']['error'] == "LIMIT_IS_EXCEEDED":
        break
      elif not data['response']['success']:
        continue

      for j in range(count):
        try:
          asset_id = int(data['response']['assets'][j]["asset_class"][0]["value"])
          price_buy = data['response']['assets'][j]['buy_price'] / 100000000
          price_sell = data['response']['assets'][j]['price'] / 100000000
          quantity_buy = data['response']['assets'][j]['depth']
          quantity_sell = data['response']['assets'][j]['buy_depth']
          profit = round((0.85 * price_sell) - price_buy, 2)
          roi = int((profit / price_buy) * 100)
          data.append((asset_id, price_buy, price_sell, quantity_buy, quantity_sell, profit, roi, timestamp))

        except Exception as err:
          print(f"ERROR: could not get market id: {asset_id} at loop index UNKNOWN")
          print(err)
          continue

      skip += curr_count
      count -= curr_count

    return data

  def cancel_order(self, receipt: Receipt) -> bool:
    timestamp = datetime.now().timestamp()
    payload = f"action=cancel_order&token={self.token}&appid=1165&transactid={receipt.transact_id}&reqstamp={timestamp}&pairId={receipt.pair_id}&orderId={receipt.order_id}"
    headers = {'accept': 'application/json, text/javascript, */*; q=0.01', 'accept-language': 'en-CA,en;q=0.8',
               'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    self.conn_market.request("POST", "/market", payload, headers)
    res = self.conn_market.getresponse()
    data = json.loads(res.read())

    if not data["response"]["success"]:
      return False
    else:
      return True

  def close_connection(self):
    self.token = None
    self.conn_wallet.close()
    self.conn_market.close()
