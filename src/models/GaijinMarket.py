from http import client
import json
from datetime import datetime
import Receipt

class GaijinMarket:
  def __init__(self, token: str):
    self.token: str = token
    self.conn_wallet: client.HTTPSConnection = client.HTTPSConnection("wallet.gaijin.net")
    self.conn_market: client.HTTPSConnection = client.HTTPSConnection("market-proxy.gaijin.net")

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

    if not data['success']:
      print("ERROR: Could not make request for open orders.")
      return []

    for item in data['response']:
      try:
        open_orders.append((int(item['txId']), int(item['id']), int(item['pairId']), item['market'], item['type'],
                            round(int(item['localPrice']) / 10000, 2), int(item['amount']), item['time']))
      except:
        print(f"ERROR: Could not get item in open orders with ID: {item['id']}")

    return open_orders

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
