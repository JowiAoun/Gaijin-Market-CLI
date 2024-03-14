import sqlite3
from src.models.Item import Item

class Database:
  def __init__(self):
    self.conn = sqlite3.connect('gmcli.db')
    self.cursor = self.conn.cursor()

  def execute_query(self, query, params=None):
    if params:
      self.cursor.execute(query, params)
    else:
      self.cursor.execute(query)
    self.conn.commit()

  def fetch_data(self, query, params=None):
    if params:
      self.cursor.execute(query, params)
    else:
      self.cursor.execute(query)
    return self.cursor.fetchall()

  def select_hash_name(self, asset_id: int) -> str:
    self.cursor.execute("SELECT hash_name FROM items_static WHERE asset_id = ?", str(asset_id))
    return self.cursor.fetchone()[0]

  def insert_item_static(self, item: Item):
    self.cursor.execute(f"INSERT INTO items_static (asset_id, hash_name, name) VALUES (?, ?, ?)",
                        (item.asset_id, item.hash_name, item.name))
    self.conn.commit()

  def insert_item_variable(self, item: Item):
    self.cursor.execute(f"INSERT INTO items_variable (asset_id, price_buy, price_sell, quantity_buy, quantity_sell, profit, roi, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (item.asset_id, item.price_buy, item.price_sell, item.quantity_buy, item.quantity_sell, item.profit, item.roi, item.timestamp))
    self.conn.commit()

  def insert_item_static_many(self, items: list[Item]):
    data = [(item.asset_id, item.hash_name, item.name) for item in items]
    self.cursor.executemany(f"INSERT INTO items_static (asset_id, hash_name, name) VALUES (?, ?, ?)", data)
    self.conn.commit()

  def insert_item_variable_many(self, items: list[Item]):
    data = [(item.asset_id, item.price_buy, item.price_sell, item.quantity_buy, item.quantity_sell, item.profit, item.roi, item.timestamp) for item in items]
    self.cursor.executemany(f"INSERT INTO items_variable (asset_id, price_buy, price_sell, quantity_buy, quantity_sell, profit, roi, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
    self.conn.commit()

  def insert_item_inventory(self, item: Item):
    raise NotImplemented()

  def insert_item_inventory_many(self, items: list[Item]):
    raise NotImplemented()

  def close_connection(self):
    self.cursor.close()
    self.conn.close()
