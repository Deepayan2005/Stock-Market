import json
import requests
from bs4 import BeautifulSoup
from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

@app.route('/find')
def findstocks():
    text = str(request.args.get('sector'))

    with ThreadPoolExecutor(max_workers=1000) as p:
        p.map(findstocks)
        r = requests.get(text)

        soup = BeautifulSoup(r.content, 'html5lib')
        dataList = []

        tableOne = soup.find("tbody")

        def decorateList(list):
            data = []
            for a in list:
                dict = {'link': a[0], 'name': a[1], 'last_price': a[2],
                        '1day_percent': a[3], 'market_cap_CR': a[4], '52W_L': a[5],
                        'volume': a[6]}
                data = data + [dict]
            return data

        for i in tableOne.find_all("tr", class_="border-b border-black5"):
            tempList = []
            link = "https://www.etmoney.com" + i.find('a')['href']
            tempList = tempList + [link]
            for a in (i.find_all("td")):
                data = BeautifulSoup(str(a), 'html5lib')
                tempList = tempList + [data.text]
            dataList = dataList + [tempList]
            tempList = []
        else:
            dataList = decorateList(dataList)
            for i in dataList:
                print(i)

        return json.dumps(dataList)



@app.route('/')
def give_details():
    with ThreadPoolExecutor(max_workers=1000) as p:
        p.map(give_details)
        URL = "https://www.etmoney.com/stocks/market-data/sectoral-indices/32"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')
        dataList = []

        for i in soup.find_all('tr', class_="border-b border-black5"):
            link = "https://www.etmoney.com" + i.find('a')['href']
            price = i.find_all("td")

            temp = []
            temp = temp + [link]

            for a in price:
                data = BeautifulSoup(str(a), 'html5lib')
                temp = temp + [data.text]

            dataList = dataList + [temp]
            temp = []

        def decorateList(list):
            data = []

            for a in list:
                dict = {'link': a[0], 'name': a[1], 'price': a[2], '1day%': a[3], '1week%': a[4], '1year%': a[5],
                        '3year%': a[6]}
                data = data + [dict]
            return data

        dataList = (decorateList(dataList))

        return json.dumps(dataList)
