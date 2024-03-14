import sqlite3

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

  def close_connection(self):
    self.conn.close()
