# Course     : CST 205
# Title      : Cryptocurrency Information
# Authors    : Juan Ansaldo, Ricardo Alire, Amancio Ramirez, Cory Greer
# Date       : 17 May 2023
# Abstract   : This program creates a flask application that uses the
#              coingecko api to display cryptocurrency information.
# Work contr : Juan worked on all templates, final.py, css, and javascript.
#              Ricardo worked on all templates and final.py.
#              Amancio worked on chart template and final.py.
#              Cory worked on info template, partials, nav bar, and final.py.
# Github link: https://github.com/juanansaldo/team7558

from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
from pprint import pprint
import requests
import humanize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# formats values using commas
def format_number(number):
    return humanize.intword(number, format='%.1f')

app = Flask(__name__)
bootstrap = Bootstrap4(app)

# root route
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

# details route with specific coin info
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

            fig = go.Figure(data=go.Scatter(x=timestamps, y=values))
            fig.update_layout(
            xaxis_title='Timestamp',
            yaxis_title='Price (USD)',
            title='Price Chart'
            )
            fig.show()
            # plt.plot(timestamps, values)
            # plt.xlabel('Timestamp')
            # plt.ylabel('Price (USD)')
            # plt.title('Price Chart')

            # plt.show()

    except Exception as e:
        print(e)
    return render_template('chart.html', id=id ,timestamps=timestamps, values=values)

# route with information about cryptocurrencies
@app.route('/information')
def information():
    return render_template('information.html')

app.run(debug=True)