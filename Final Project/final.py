# Coinmarketcap project
import sys
import requests, json
from pprint import pprint
from PySide6.QtWidgets import (QApplication, QLabel, QWidget, QPushButton, QLabel, QVBoxLayout, QDateEdit, QLineEdit)
from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
from PySide6.QtCore import Slot, QDate, Qt   
from PySide6.QtGui import QPixmap
from qt_material import apply_stylesheet
import itertools

app = Flask(__name__)
bootstrap = Bootstrap4(app)

@app.route('/')
def index():
    # my_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V'
    endpoint = 'https://api.coingecko.com/api/v3/coins/markets?'
    payload = {
        #'api_key': my_key,
        #'start_date': '2023-03-09',
        #'end_date': '2023-03-11'
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': '100'
    }

    rank_list = []
    name_list = []
    price_list = []
    logo_list = []
    symbol_list = []
    dayChange_list = []
    dayVolume_list = []
    marketcap_list = []

    try:
        r = requests.get(endpoint, params=payload)
        if r.ok:
            data = r.json()
            # pprint(data)
            for item in data:
                rank_list.append(item['market_cap_rank'])
                name_list.append(item['name'])
                symbol_list.append(item['symbol'])
                price_list.append(item['current_price'])
                logo_list.append(item['image'])
                dayChange_list.append(item['price_change_percentage_24h'])
                dayVolume_list.append(item['total_volume'])
                marketcap_list.append(item['market_cap'])

                # logo_list = data[int(1)]['image']
                # name_list = data[int(1)]['name']
                # symbol_list = data[int(1)]['symbol']
                # price_list = data[int(1)]['current_price']

                # pprint(f'Crypto Name: {name_list}')
                # pprint(len(name_list))
                # pprint(f'Ticker Symbol: {symbol_list}')
                # pprint(f'Price: {price_list}')
            # pprint(f'{logo_list}')
    except Exception as e:
        print(e)
    return render_template('index.html', data = zip(rank_list, name_list, price_list, logo_list, symbol_list, dayChange_list, dayVolume_list, marketcap_list))
    # return render_template('index.html', name_list=name_list, price_list=price_list, logo_list=logo_list, symbol_list=symbol_list)

@app.route('/detail')
def detail():
    endpoint = 'https://api.coingecko.com/api/v3/coins/bitcoin?'
    payload = {
        'tickers': 'false',
        'market_data': 'false',
        'community_data': 'false',
        'developer_data': 'false',
        'sparkline': 'false'

    }
    description_list = []
    try:
        r = requests.get(endpoint, params=payload)
        if r.ok:
            data = r.json()
            # pprint(data)
            for item in data['description']['en']:
                # pprint(item)
                description_list = (item[0])
            pprint(description_list)
    except Exception as e:
        print(e)
    return render_template('detail.html')

app.run(debug=True)
