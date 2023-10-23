# --- Imports
from http import client # used to make API requests
import json  # used to load settings from settings.json
import os # used in setting environment variables
from dotenv import load_dotenv # used in loading .env file


# --- Setup
load_dotenv() # load environment variables


# --- Constants
TOKEN = os.environ.get("TOKEN") # get token from .env (SECRET)
STGS = json.load(open('./settings.json', 'r')) # set settings from .json file


# --- Functions
def get_balance() -> float:
    """
    Gets the balance of the user.
    If successful, returns a float.
    """
    
    # Get data
    conn = client.HTTPSConnection("wallet.gaijin.net")
    headers = {'Authorization': f'BEARER {TOKEN}'}
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
    payload = f"action=GetContextContents&token={TOKEN}&appid=1067&contextid=1"
    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    conn.request("POST", "/assetAPI", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read())

    # Create mapping for itemid-classid
    idsMapping = {}
    for item in data["result"]["assets"]:
        idsMapping[item["class"][0]["value"]] = item["id"]

    # Check is status is good
    if (data["result"]["success"] != True):
        print(f"Error: could not get inventory IDs.\nStatus: {data['result']['success']}")
        exit()
    
    return idsMapping

def get_inventory():
    #TODO: This is the next step.
    #? When i'm making a request, should I instead update an SQL database
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