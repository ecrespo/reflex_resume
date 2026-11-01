Title: InfluxDB database on Debian Stretch
Date: 2017-06-24 12:00
Category: Tutorial de Linux
Tags: Linux,Debian,Ubuntu,InfluxDB
lang: en
translation: true

InfluxDB is an opensource time series database for handling events, monitoring, metrics, the Internet of Things and real-time analytics. It is developed by [InfluxData](https://www.influxdata.com/) in the Go language. You can find more information on [wikipedia](https://en.wikipedia.org/wiki/InfluxDB).

To install it on Debian you simply use `apt-get`:
```
# apt-cache search influxdb 
golang-github-influxdb-enterprise-client-dev - Golang client for speaking to the InfluxDB Enterprise application
golang-github-influxdb-usage-client-dev - library for speaking to the InfluxDB Anonymous Usage Reporting API
golang-gopkg-alexcesaro-statsd.v1-dev - simple and efficient Golang StatsD client
golang-github-influxdb-influxdb-dev - Scalable datastore for metrics, events, and real-time analytics. Dev package
influxdb - Scalable datastore for metrics, events, and real-time analytics
influxdb-client - command line interface for InfluxDB
influxdb-dev - Transitional package for golang-github-influxdb-influxdb-dev
ruby-influxdb - library for InfluxDB
```

To install:
```
# apt-get install influxdb influxdb-client
```
To test that it is running:
```
# influx
Visit https://enterprise.influxdata.com to register for updates, InfluxDB server management, and monitoring.
Connected to http://localhost:8086 version 1.0.2
InfluxDB shell version: 1.0.2
> 
```


To create a database called `mydb`:
```
> create database mydb
```
List the databases:
```
> show databases
name: databases
---------------
name
_internal
mydb

```

Insert data and query it in the `mydb` database:
```
> use mydb
Using database mydb
> INSERT cpu,host=ServerA,region=us_west value=0.64
> SELECT host, region, value FROM cpu
name: cpu
---------
time                   host         region value
1498340879346347895 ServerA us_west 0.64
```
As you can see, the primary key of the data is always the time. 

Now a small test with Python.

To install the library in Python:
```python
# pip3 install influxdb
```


We have the following script:

```python


#!/usr/bin/env python3





#Se importa influxdb


from influxdb import InfluxDBClient





#Se define un json con los datos a insertar


json_body = [


    {


        "measurement": "cpu_load_short",


        "tags": {


            "host": "server01",


            "region": "us-west"


        },


        "time": "2009-11-10T23:00:00Z",


        "fields": {


            "value": 0.64


        }


    },


    {


        "measurement": "cpu_load_short",


        "tags": {


            "host": "server02",


            "region": "us-west"


        },


        "time": "2009-12-10T23:00:00Z",


        "fields": {


            "value": 0.65


        }


    }


]


#Se conecta a la base de datos


client = InfluxDBClient('localhost', 8086, 'root', 'root', 'mydb')


#Se crea la base de datos mydb


client.create_database('mydb')





#Se inserta los datos


client.write_points(json_body)


#Se consulta y se muestra en pantalla


result = client.query('select value from cpu_load_short;')


print("Result: {0}".format(result))

```

When the script is run, it returns the following:
```python
./prueba-influxdb.py 
Result: ResultSet({'('cpu_load_short', None)': [{'value': 0.64, 'time': '2009-11-10T23:00:00Z'}, {'value': 0.65, 'time': '2009-12-10T23:00:00Z'}]})
```

Or from the `influxdb` client:
```
> use mydb
Using database mydb
> select value from cpu_load_short;
name: cpu_load_short
--------------------
time   value
1257894000000000000 0.64
1260486000000000000 0.65
```

As shown, the key that drives the queries is the time.

For more information, see the following links:

- Grafana, influxdb and python.  
- influxdb-python and its documentation.   
- influxdata documentation.  
- Influxdata platform  



##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)

