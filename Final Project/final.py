# Coinmarketcap project
from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
from pprint import pprint
import requests
import matplotlib.pyplot as plt
app = Flask(__name__)
bootstrap = Bootstrap4(app)

@app.route('/')
def index():
    endpoint = 'https://api.coingecko.com/api/v3/coins/markets?'
    payload = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': '20'
    }

    id_list = []
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
            pprint(data)
            for item in data:
                id_list.append(item['id'])
                rank_list.append(item['market_cap_rank'])
                name_list.append(item['name'])
                symbol_list.append(item['symbol'])
                price_list.append(item['current_price'])
                logo_list.append(item['image'])
                dayChange_list.append(item['price_change_percentage_24h'])
                dayVolume_list.append(item['total_volume'])
                marketcap_list.append(item['market_cap'])

            symbol_list = [symbol.upper() for symbol in symbol_list]
            marketcap_list = [format(num, ',') for num in marketcap_list]
            price_list = [format(round(num, 2), ',.2f') for num in price_list]
            dayVolume_list = [format(num, ',') for num in dayVolume_list]
            dayChange_list = [format(round(num, 2), ',.2f') for num in dayChange_list]
    except Exception as e:
        print(e)

    return render_template('index.html', data = zip(id_list, rank_list, name_list, price_list, logo_list, symbol_list, dayChange_list, dayVolume_list, marketcap_list))

@app.route('/detail/<id>')
def detail(id):
    endpoint = f'https://api.coingecko.com/api/v3/coins/{id}?'
    payload = {
        'tickers': 'false',
        'market_data': 'false',
        'community_data': 'false',
        'developer_data': 'false',
        'sparkline': 'false'
    }

    try:
        r = requests.get(endpoint, params=payload)
        if r.ok:
            data = r.json()
            pprint(data)
            description = data['description']['en']
            description = description.replace('<a ', '<a target="_blank" ')
    except Exception as e:
        print(e)

    return render_template('detail.html', id=id, description=description)

@app.route('/chart/<id>')
def chart(id):
    endpoint = f'https://api.coingecko.com/api/v3/coins/{id}/market_chart?'
    payload = {
        'vs_currency': 'usd',
        'days': '1,14,30,max',
        'interval': 'daily'
    }

    try:
        r = requests.get(endpoint, params=payload)
        if r.ok:
            data = r.json()

            prices = data['prices']
            timestamps = [price[0] for price in prices]
            values = [price[1] for price in prices]

            plt.plot(timestamps, values)
            plt.xlabel('Timestamp')
            plt.ylabel('Price (USD)')
            plt.title('Price Chart')

            plt.show()

    except Exception as e:
        print(e)
app.run(debug=True)