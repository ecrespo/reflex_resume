Title: Extracting data from a web page with pyquery and Python
Date: 2013-10-27 9:00
Category: Tutorial Python
Tags: Canaima,Debian,General,Linux,Python,Ubuntu,Webscraping
lang: en
translation: true

Continuing with the [webscraping articles](/blog/tags), it is now the turn of [pyquery](https://pypi.org/project/pyquery/).

The explanation of how to locate the information to be obtained was already given in this [article](/blog/webscrapingoextracciondedatosdepaginaswebconbeautifulsoup4ypython) article.

Pyquery is a library that lets you make jquery-style queries on xml documents. 

The idea is to obtain the sunrise and sunset information already explained in previous articles. 

The code is shown below:

```python
#!/usr/bin/env python

#importar pyquery

from pyquery import *

#Se Crea la instancia de la Clase PyQuery pasando el url de

#timeanddate.

html = PyQuery(url='http://www.timeanddate.com/worldclock/astronomy.html?n=58')

#Se busca el tag html de la tabla.

#Recibe todos los elementos de la tabla.

trs = html('table.spad tbody tr')

#Se muestra los elementos de la tabla.

print trs

#Se recorre los elementos de la tabla

for tr in trs:

    tds = tr.getchildren()

    print tds[1].text, tds[2].text

```

The result of running the script is shown below:
```
05:47 17:36

05:47 17:36

05:48 17:35

05:48 17:35

05:48 17:35

05:48 17:34

05:48 17:34

```

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)