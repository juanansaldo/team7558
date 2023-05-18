from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
from pprint import pprint
import requests
import humanize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def format_number(number):
    return humanize.intword(number, format='%.1f')

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
            circSupply = data['market_data']['circulating_supply']
            totalSupply = data['market_data']['total_supply']
            weekChange = data['market_data']['price_change_percentage_7d']
            yearChange = data['market_data']['price_change_percentage_1y']
            low = data['market_data']['low_24h']['usd']
            high = data['market_data']['high_24h']['usd']

            price = "${:,.2f}".format(price)
            dayChange = round(dayChange, 2)
            dayVolume = format_number(dayVolume)
            marketcap = format_number(marketcap)
            circSupply = round(circSupply)
            totalSupply = round(totalSupply)
            circSupply = format(circSupply, ',')
            totalSupply = format(totalSupply, ',')
            weekChange = round(weekChange, 2)
            yearChange = round(yearChange, 2)
            low = "${:,.2f}".format(low)
            high = "${:,.2f}".format(high)

    except Exception as e:
        print(e)

    return render_template('detail.html', low=low, high=high, weekChange=weekChange, yearChange=yearChange, circSupply=circSupply, totalSupply=totalSupply, price=price, dayChange=dayChange, dayVolume=dayVolume, marketcap=marketcap, data=data)

@app.route('/chart/<id>')
def chart(id):
    endpoint = f'https://api.coingecko.com/api/v3/coins/{id}'
    payload = {
        'vs_currency': 'usd',
        'market_data': 'true',
        'days': '30',
        'interval': 'daily',
        'tickers': 'false',
        'community_data': 'false',
        'developer_data': 'false',
        'sparkline': 'false'
    }

    name = id.upper()
    timestamps = []
    prices = []
    data = {}

    try:
        r = requests.get(endpoint, params=payload)
        if r.ok:
            data = r.json()

            price = data['market_data']['current_price']['usd']
            dayChange = data['market_data']['price_change_percentage_24h']
            dayVolume = data['market_data']['total_volume']['usd']
            marketcap = data['market_data']['market_cap']['usd']
            circSupply = data['market_data']['circulating_supply']
            totalSupply = data['market_data']['total_supply']
            weekChange = data['market_data']['price_change_percentage_7d']
            yearChange = data['market_data']['price_change_percentage_1y']
            low = data['market_data']['low_24h']['usd']
            high = data['market_data']['high_24h']['usd']

            price = "${:,.2f}".format(price)
            dayChange = round(dayChange, 2)
            dayVolume = format_number(dayVolume)
            marketcap = format_number(marketcap)
            circSupply = round(circSupply)
            totalSupply = round(totalSupply)
            circSupply = format(circSupply, ',')
            totalSupply = format(totalSupply, ',')
            weekChange = round(weekChange, 2)
            yearChange = round(yearChange, 2)
            low = "${:,.2f}".format(low)
            high = "${:,.2f}".format(high)

            timestamps, prices = zip(*data['prices'])
            timestamps = [ts / 60000 for ts in timestamps]

            plotName = id.capitalize()

            plt.clf()
            plt.plot(timestamps, prices)
            plt.title(plotName + "'s Current Price Change Per Minute")
            plt.tick_params(axis='x', labelbottom=False)
            plt.xlabel('Time (minutes)')
            plt.ylabel('Value ($)')
            plt.savefig(f'static/images/{id}_chart.png')

    except Exception as e:
        print(e)

    return render_template('chart.html', id=id, name=name, imestamps=timestamps, values=prices, low=low, high=high, weekChange=weekChange, yearChange=yearChange, circSupply=circSupply, totalSupply=totalSupply, price=price, dayChange=dayChange, dayVolume=dayVolume, marketcap=marketcap, data=data)

@app.route('/information')
def information():
    return render_template('information.html')

app.run(debug=True)