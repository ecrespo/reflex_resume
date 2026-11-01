Title: Getting weather information for a city with Python  
Date: 2014-01-19 9:00  
Category: Tutorial Python  
Tags: Canaima,Debian,Python,Ubuntu,PyOWM  
lang: en
translation: true  



There is a library called [PyOWM](https://github.com/csparpa/pyowm), which is a wrapper for the OpenWeatherMap API. 
The documentation for using the library is at the following [link](https://github.com/csparpa/pyowm/wiki/Usage-examples).

To use the library you need to create an account on OpenWeatherMap and look up the APPID in the user's profile. The procedure is explained at this [link](https://openweathermap.org/appid).

To install the library, run `pip`:
```
#pip install pyowm
```

Below is the code of a script that shows how to use the library:
 
```python
#!/usr/bin/env python


# -*- coding: utf-8 -*-


import pyowm

#Llave del uso del API


apikey = "abcdefghijklimnopqrstuvxyz"


#Se crea la instancia OWM pasando la llave para el uso del API.


owm = pyowm.OWM(apikey)


#Se obtiene la llave de uso del API


print owm.get_API_key()


#Se define la ciudad por nombre o se pasa la coordenada.


obs = owm.weather_at('Valencia,ve')


#obs = owm.weather_at_coords(-0.107331,51.503614)


print "tiempo: ", obs.get_reception_time()


print "tiempo: ", obs.get_reception_time(timeformat='iso')


#Se Instancia los datos de la estacion meterologica.


w = obs.get_weather()


print "Fecha y hora ",w.get_reference_time(timeformat='iso')


print "Nubes:", w.get_clouds()


print  "lluvias:", w.get_rain()


print "Nieve: ", w.get_snow()


print "viento", w.get_wind()


print "humedad:",w.get_humidity()


print "presion:", w.get_pressure()


print "Temperatura:",w.get_temperature()


print "Temperatura:",w.get_temperature(unit='celsius')


print "Estatus", w.get_status()


print "Hora de salida del sol",w.get_sunrise_time("iso")


print "Hora de ocultarse el sol",w.get_sunset_time('iso')


l = obs.get_location()


print "nombre:", l.get_name()


print "Longitud: %s, Latitud: %s"   %(l.get_lon(),l.get_lat())

print "Identificador", l.get_ID()
```

Running the application gives the following:

```python
ernesto@heimdal:~/bin/python$ ./clima.py 

abcdefghijklimnopqrstuvxyz

tiempo:  1390165372

tiempo:  2014-01-19 21:02:52+00

Fecha y hora  2014-01-19 20:00:00+00

Nubes: 20

lluvias: {}

Nieve:  {}

viento {u'speed': 2.1, u'deg': 110}

humedad: 41

presion: {'press': 1012, 'sea_level': None}

Temperatura: {'temp_kf': None, 'temp_min': 308.15, 'temp': 308.15, 'temp_max': 308.15}

Temperatura: {'temp_kf': None, 'temp_max': 35.0, 'temp': 35.0, 'temp_min': 35.0}

Estatus clouds

Hora de salida del sol 2014-01-19 10:54:19+00

Hora de ocultarse el sol 2014-01-19 22:31:34+00

nombre: Valencia

Longitud: -68.01, Latitud: 10.16



Identificador 3625549  

```


Note that the sunrise and sunset times are relative to the Greenwich 
meridian (you need to adjust them to the corresponding time zone).


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)