Title:  Discovering Twitter Trending Topics with twython and python
Date: 2013-09-22 9:00
Category: Tutorial Python
Tags: Canaima,Debian,General,Linux,Python,Twitter,Ubuntu
lang: en
translation: true

Continuing with the articles about [python libraries for twitter](/blog/twitter), an article recently showed how to [see the Trending Topics using the python-twitter library](/blog/descubriendotrendingtopicsdetwitterconpythontwitter) , and now it will be shown how to display the topics using the twython library.

The script will show the connection to twitter, then display the identifiers of the cities that have Trending Topics in Venezuela, and finally display the Trending Topics of Venezuela right now.

To learn how to obtain the application or access token value, it is recommended to review the [previous article](/blog/probandolalibreriatwythonparatwitter).

The code is shown below:
```python
#!/usr/bin/env python

# -*- coding: utf-8 -*-

#Se define el token de la aplicacion

CONSUMER_KEY = 'xxxxx'

CONSUMER_SECRET = 'xxxxx'

#Se define el acceso al usuario

ACCESS_KEY = 'xxxxx'

ACCESS_SECRET = 'xxxxx'

#Se importa twython y de time a  sleep

from twython import Twython

from time import sleep

#Se define los argumentos del cliente, la ip y puerto del proxy, el tiempo de intento de la conexion y el nombre de la

#aplicacion cliente

client_args = {'headers': {'User-Agent': 'cmdtweetpy'},'proxies': {'http': '127.0.0.1:xxx'},'timeout': 300}

#Conectar a twitter y enviar un tweet,

#Si no se logra la conexion se devuelve un mensaje.

try:

    api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET,client_args = client_args)

    print(u"Autenticación con exito")

except twython.exceptions.TwythonAuthError:

    print(u"Error de autenticación")

print ""

trending = api.get_available_trends()

print u"Identificación de woeid de Venezuela"

print "-------------------------------------"

c = 0   

pos = 0

woeid = 0

#Se despliega los woeid de las ciudades de Venezuela y de Venezuela en si


for i in trending:


    if i[u'countryCode'] == u'VE':


        print i[u'name'],i[u'woeid']


        #Se toma el woeid de Venezuela


        woeid = i[u'woeid']


        pos = c


    c += 1


print ""


#Se despliega los topics de Venezuela.


print "Lista de Trending Topics en Venezuela"


print "-------------------------------------"


for i in api.get_place_trends(id=woeid):


    for k in i[u'trends']:


        print k[u'name']
```

The result of running the script is shown below:

```python
Identificación de woeid de Venezuela


-------------------------------------


Caracas 395269


Maracaibo 395270


Maracay 395271


Valencia 395272


Barcelona 395273


Ciudad Guayana 395275


Turmero 395277


Barquisimeto 468382


Maturín 468384


Venezuela 23424982





Lista de Trending Topics en Venezuela


-------------------------------------


#10CosasQueOdio


#AlfombraRojaE


#EmmysPorWarner


#ChavezElGranArquitecto


#ObamaNervioso


Angela Merkel


Titanic


Kenia


GNB


Sofia Vergara
```

As you can see, the topics of each city or country can be obtained once you have the `woeid`.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)