# --- Imports
from classes import Item # class to preserve a market item
from http import client # used to make API requests
from dotenv import load_dotenv # used in loading .env file
import mysql.connector # connector for MySQL database
import json  # used to load settings from settings.json
import os # used in setting environment variables


# --- Setup
load_dotenv() # load environment variables
with open('./src/queries.sql', 'r') as file: # read SQL querries
    sql_content = file.read()
queries = [query.split('\n', 1)[1].strip() for query in sql_content.split('-- #') if query.strip()]


# --- Constants
STGS = json.load(open('./settings.json', 'r')) # set settings from .json file
GM_TOKEN = os.environ.get("GM_TOKEN") # get token from .env (SECRET)
DB_USER_NAME = os.environ.get("DB_USER_NAME")
DB_USER_PASSWORD = os.environ.get("DB_USER_PASSWORD")
DB_NAME = "gmcli"
DB = mysql.connector.connect(
    host="localhost",
    user=DB_USER_NAME,
    passwd=DB_USER_PASSWORD,
    database=DB_NAME
)
DB_CURSOR = DB.cursor()


# --- Functions
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

    # Check if status is good
    if (data["status"] != "OK"):
        print(f"Error: could not get balance.\nStatus: {data['status']}")
        exit()

    conn.close()

    return float(data["balance"])/10000

def get_inventory_ids() -> dict:
    """
    Returns a dictionary in key-value form itemid-classid,
    where the 'itemid' is the static ID of the item,
    and 'classid' is the ID given to the item while in the inventory.
    The 'classid' changes after transactions are done with it.
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
        ids_mapping[item["class"][0]["value"]] = item["id"]

    # Check is status is good
    if (data["result"]["success"] != True):
        print(f"Error: could not get inventory IDs.\nStatus: {data['result']['success']}")
        exit()

    conn.close()
    
    return ids_mapping

def get_inventory():
    """
    Development steps:
    1. get_inventory_ids()
    2. Make requests to each item to get item info.
       - There may be an efficient 1 API call to do all that.
    """
    pass

def db_populate_items_static(table_name):
    """
    Populates the database's table provided to the function with static data from the Gaijin Market.
    This should be used lightly as it creates 18 big requests. The data is static, and therefore does
    not need frequent updating.
    """

    conn = client.HTTPSConnection("market-proxy.gaijin.net") # setup connection
    count = 100
    skip = 0
    
    for i in range(STGS['requests']):
        # Get data
        payload = f"action=cln_market_search&token={GM_TOKEN}&appid=1165&skip={skip}&count={count}&text=&language=en_US&options=any_sell_orders&appid_filter=1067"
        headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8"}
        conn.request("GET", "/web", payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read())

        # Iterate over each item in the request
        for j in range(count):
            try:
                asset_id = data['response']['assets'][j]["asset_class"][0]["value"]
                name = data['response']['assets'][j]['name']
                hash_name = data['response']['assets'][j]['hash_name']
                DB_CURSOR.execute(queries[0], (table_name, asset_id, name, hash_name))
            except:
                print(f"Error: could not insert market item static data to DB: {asset_id, name, hash_name} at loop index {i*100 + j}")
                continue

        skip += 100

    DB.commit()
    conn.close()


#? Next steps:
#? DONE - 1. Put static information into new database table (asset_id, name, hash_name)
#? 2. Link that table to another table containing variable data
#?    (price_buy, price_sell, quantity_buy, quantity_sell, profit, roi, timestamp)
#? 3. Add a tags table, link to asset_id from items_static
#?    (could be populated in db_populate_items_static simultanously)