Title: Using memcached to keep data at hand
Date:  2019-09-22 10:33
Category: Tutorial de Python
Tags: Debian,Python,Ubuntu,memcached,Fedora
lang: en
translation: true
Slug: memcached_2019
Authors: Ernesto Crespo
Summary: There are cases where data is taken from a database that can be somewhat slow and that data has to be fetched again; for that it is better to have a cache with the data in order to reduce the latency that database queries can cause us. To do this, memcached will be used in Python.

This article explains why memcached is used, how it is installed and how it is used from Python.

The following figure shows an application that gets its data from a (slow) database. Here the problem arises when the database is queried and, depending on the number of queries, the query may at some point come back empty. The other issue is that if you have to fetch the same data several times; in both cases memcached becomes necessary.

![without memcached](./images/20190922-memcache_sin.png)

The following figure shows the addition of memcached, used together with the database, to "cache" the database's data.

![with memcached](./images/20190922-memcached.png)


This article is based on an article about [memcached from realpython](https://realpython.com/python-memcache-efficient-caching/).

### Installing memcached

For Debian and Debian derivatives, apt is used to install memcached:
```bash
apt-get install memcached
```
For Redhat, Fedora, Centos:
```bash
yum install memcached
```

Install the library for Python; in this case pip is used:
```
pip install pymemcache  
```

Run memcached:
```
memcached
```
### The code

The example code for using pymemcache is shown below:

```python

#!/usr/bin/env python3

#Se importa el cliente de memcached
from pymemcache.client import base


#Se conecta al servidor memcached
client = base.Client(('localhost', 11211))

#Se almacena en memcached una variable y un valor
client.set('variable', 'valor')

#Se almacena otro valor
client.set("entero",1)

#Se almacena otro
client.set("booleano",True)
variable = str(client.get('variable'))
entero = int(client.get('entero'))
booleano = bool(client.get('booleano'))

#se ve el tipo de las variables
print(type(client.get('variable')))
print(type(client.get('entero')))
print(type(client.get('booleano')))


#Se muestra el resultado tomando los datos de memcached
print(f"variable: {type(variable)}, {variable}")
print(f"entero: {type(entero)}, {entero}")
print(f"booleano: {type(booleano)},{booleano}")

```

### Result

The output of the script (mem1.py) is shown below:

```
<class 'bytes'>
<class 'bytes'>
<class 'bytes'>
variable: <class 'str'>, b'valor'
entero: <class 'int'>, 1
booleano: <class 'bool'>,True
```

As the output shows, the variables stored in memcached are all of type bytes when their values are retrieved, so they have to be converted before they can be manipulated in the code.




####
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
