Title: Extracting data from web pages with Webscraping and Python
Date:  2013-10-25 9:00
Category: Tutorial Python
Tags: Canaima,Debian,General,Linux,Python,Ubuntu,Webscraping
lang: en
translation: true

Continuing with the data extraction from the timeanddate page, the sunrise and sunset information for Venezuela.
In this case the webscraping library will be used. To install it, use the `pip` command:
```
#pip install webscraping
```
The [previous (broken link)](/blog/webscrapingoextracciondedatosdepaginaswebconbeautifulsoup4ypython) article shows how to locate the information that is needed.

The code is shown below:

```python
#!/usr/bin/env python


#De webscraping se importa download y xpath


from webscraping import download, xpath


#Se define la instancia Download


D = download.Download()

#Se obtiene la informacion de la salida y ocultamiento del

#sol en Venezuela desde la pagina timeanddate.

html = D.get('http://www.timeanddate.com/worldclock/astronomy.html?n=58')


#Se busca la informacion en la tabla donde se muestra.


for row in xpath.search(html, '//table[@class="spad"]/tbody/tr'):


    #Se busca en la fila el tag /td


    cols = xpath.search(row, '/td')


    #Se muestra la informacion en pantalla


    print 'Amanecer: %s, Atardecer: %s' % (cols[1], cols[2])
```

The result of running the script is shown below:
```
Amanecer: 05:47, Atardecer: 17:36

Amanecer: 05:47, Atardecer: 17:36

Amanecer: 05:47, Atardecer: 17:36

Amanecer: 05:48, Atardecer: 17:35

Amanecer: 05:48, Atardecer: 17:35

Amanecer: 05:48, Atardecer: 17:35

Amanecer: 05:48, Atardecer: 17:34
```
##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)