# Coinmarketcap project
from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
from pprint import pprint
import requests
import humanize

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

    return render_template('index.html', data=zip(id_list, rank_list, name_list, price_list, logo_list, symbol_list, dayChange_list, dayVolume_list, marketcap_list))

@app.route('/detail/<id>')
def detail(id):
    def format_number(number):
        return humanize.intword(number, format='%.1f')

    endpoint = f'https://api.coingecko.com/api/v3/coins/{id}?'
    payload = {
        'tickers': 'false',
        'market_data': 'true',
        'community_data': 'false',
        'developer_data': 'false',
        'sparkline': 'false'
    }

    try:
        r = requests.get(endpoint, params=payload)

        if r.ok:
            data = r.json()
            pprint(data)

            price = data['market_data']['current_price']['usd']
            dayChange = data['market_data']['price_change_percentage_24h']
            dayVolume = data['market_data']['total_volume']['usd']
            marketcap = data['market_data']['market_cap']['usd']

            price = "${:,.2f}".format(price)
            marketcap = format_number(marketcap)
            dayVolume = format_number(dayVolume)



    except Exception as e:
        print(e)

    return render_template('detail.html', price=price, dayVolume=dayVolume, marketcap=marketcap, data=data)

app.run(debug=True)