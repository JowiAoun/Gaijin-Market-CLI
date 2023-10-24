# --- Imports
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


# --- Requests
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
    
    return ids_mapping

def get_inventory():
    #? When making a request, should I instead update an SQL database
    #? instead of making more and more requests to get current inventory?
    pass

def market_search():
    conn = client.HTTPSConnection("market-proxy.gaijin.net") # setup connection
    count = 100
    skip = 0
    
    #! temporary, store directly into a database instead
    items = {'Item': [], 'Buy': [], 'Sell': [], 'Profit': [], 'ROI': [], 'ID': [], 'Link': []}

    for i in range(STGS['requests']):
        #! make new item class here
        payload = f"action=cln_market_search&token={STGS['token']}&appid=1165&skip={skip}&count=100&text=&language=en_US&options=any_sell_orders&appid_filter=1067"
        headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8"}
        conn.request("GET", "/web", payload, headers)
        res = conn.getresponse()

        data = json.loads(res.read())

        for j in range(count):
            try:
                name = data['response']['assets'][j]['name']
                hash_name = data['response']['assets'][j]['hash_name']
                price_buy = data['response']['assets'][j]['buy_price'] / 100000000
                price_sell = data['response']['assets'][j]['price'] / 100000000
            except:
                continue

            if ('key' in name) or (price_buy > STGS['buy_max']) or (price_buy == 0) or (price_sell == 0):
                continue

            profit = (0.85 * price_sell) - price_buy
            roi = (profit / price_buy) * 100

            if (profit < STGS['profit_min']) or (roi < STGS['roi_min']):
                continue

            items['Item'].append(name)
            items['Buy'].append(float(f"{price_buy:.2f}"))
            items['Sell'].append(float(f"{price_sell:.2f}"))
            items['Profit'].append(float(f"{profit:.2f}"))
            items['ROI'].append(str(int(roi)) + "%")
            items['ID'].append(hash)
            items['Link'].append("https://trade.gaijin.net/?n=" + str(hash) + "&viewitem=&a=1067")

        skip += 100

    conn.close()


# --- Helpers
