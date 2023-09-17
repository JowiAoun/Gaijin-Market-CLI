# --- Imports
import http # used to make API requests
import pandas as pd  # used to turn arrays into csv and sorting
import json  # used to load settings from settings.json


# --- Access settings
stgs = json.load(open('settings_search.json', 'w'))


# --- Functions
def market_search():
    count = 100
    skip = 0

    items = {'Item': [], 'Buy': [], 'Sell': [], 'Profit': [], 'ROI': [], 'ID': [], 'Link': []}

    #! get from requests.py, make sure to connect only once
    conn = http.client.HTTPSConnection("market-proxy.gaijin.net")

    for i in range(stgs['requests']):
        #! make new item class here
        payload = f"action=cln_market_search&token={stgs['token']}&appid=1165&skip={skip}&count=100&text=&language=en_US&options=any_sell_orders&appid_filter=1067"
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

            if ('key' in name) or (price_buy > stgs['buy_max']) or (price_buy == 0) or (price_sell == 0):
                continue

            profit = (0.85 * price_sell) - price_buy
            roi = (profit / price_buy) * 100

            if (profit < stgs['profit_min']) or (roi < stgs['roi_min']):
                continue

            items['Item'].append(name)
            items['Buy'].append(float(f"{price_buy:.2f}"))
            items['Sell'].append(float(f"{price_sell:.2f}"))
            items['Profit'].append(float(f"{profit:.2f}"))
            items['ROI'].append(str(int(roi)) + "%")
            items['ID'].append(hash)
            items['Link'].append("https://trade.gaijin.net/?n=" + str(hash) + "&viewitem=&a=1067")

        skip += 100

    df = pd.DataFrame(data=items)
    df_ = df.sort_values('Profit', ascending=False)  # !get from search_settings

    df_.to_csv("warthunder-prices-data.csv", index=False, encoding='cp1252', errors='ignore')
