Title: Getting the bitcoin price from coinmarketcap with Python  
Date: 2018-03-11 09:00  
Category: Tutorial Python  
Tags: Numpy,Python,Coinmarketcap,Request,Blockchain,Bitcoin
lang: en
translation: true  


This article shows two ways to get the real-time Bitcoin price from the [coinmarketcap](https://coinmarketcap.com/) site; the first is using the request library, and the second is using a python library to access the Coinmarketcap API.

Coinmarketcap is a site that shows the market capitalization of the various existing cryptocurrencies in real time; a screenshot of the site is shown below:

![](./images/obtenercotizaciondebitcoindecoinmarketcapconpython-1.png)


This article is based on the Real Python article "[Python Project for Beginners: Bitcoin Price Notifications](https://realpython.com/blog/python/python-bitcoin-ifttt/)" and on the documentation of the [coinmarketcap](https://pypi.python.org/pypi/coinmarketcap/2.0) library.

To use the coinmarketcap library, first install it via pip3:
```python
pip3 install coinmarketcap
```
The exercise of accessing the coinmarketcap API from request and from the library that accesses the API is shown below:

In [1]:
```python
#Se importa la librería request
import requests
```
In [2]:
```python
#Se guarda el url del api para bitcoin
bitcoin_api_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
#Se guarda la consulta al url de bitcoin
respuesta = requests.get(bitcoin_api_url)
#Se obtiene el json de la respuesta
resp_json = respuesta.json()
```
In [3]:
```python
#cual es el tipo de dato de resp_json
type(resp_json)
```
Out[3]:
```python
list
```
In [4]:
```python
#El tipo de datos de resp_json es una lista, se muestra el primer elemento de la lista
resp_json[0]
```
Out[4]:
```python
{'24h_volume_usd': '6324610000.0',
 'available_supply': '16913212.0',
 'id': 'bitcoin',
 'last_updated': '1520799265',
 'market_cap_usd': '162063750441',
 'max_supply': '21000000.0',
 'name': 'Bitcoin',
 'percent_change_1h': '-0.64',
 'percent_change_24h': '5.74',
 'percent_change_7d': '-15.57',
 'price_btc': '1.0',
 'price_usd': '9582.08',
 'rank': '1',
 'symbol': 'BTC',
 'total_supply': '16913212.0'}
```
In [5]:
```python
#Se tiene un json con los datos de la cotización actual de Bitcoin BTC.
```
In [6]:
```python
#Ahora se usa la libreria coinmarketcap y la clase Market.
from coinmarketcap import Market
```
In [7]:
```python
#Se crea la instancia de la clase
coinmarketcap = Market()
```
In [8]:
```python
#Se obtiene la cotizacion de bitcoin
coinmarketcap.ticker("bitcoin")
Out[8]:
[{'24h_volume_usd': '6323720000.0',
  'available_supply': '16913337.0',
  'cached': False,
  'id': 'bitcoin',
  'last_updated': '1520799866',
  'market_cap_usd': '161323467507',
  'max_supply': '21000000.0',
  'name': 'Bitcoin',
  'percent_change_1h': '-1.11',
  'percent_change_24h': '5.47',
  'percent_change_7d': '-16.0',
  'price_btc': '1.0',
  'price_usd': '9538.24',
  'rank': '1',
  'symbol': 'BTC',
  'total_supply': '16913337.0'}]
```

There are two ways to get the information from the coinmarketcap site: one is using request and the other is the library that accesses the API directly. It is up to you to decide which is the best option to use.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)