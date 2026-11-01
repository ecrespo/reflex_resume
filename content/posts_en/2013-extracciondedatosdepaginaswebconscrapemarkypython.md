Title: Extracting data from web pages with Scrapemark and Python
Date: 2013-10-26 10:00
Category: Tutorial Python
Tags: Canaima,Debian,General,Linux,Python,Ubuntu,webscraping, Scrapermark
lang: en
translation: true

Continuing with the articles on [webscraping](/blog/tags), now it is the turn of `scrapermark`.

The example page is still timeanddate.com. `Scrapermark` uses regular expressions internally, which makes its searches fast, and it uses a language similar to HTML.

To get scrapermark you can download either the egg or the source from the following [link](https://arshaw.com/scrapemark/download/).

For the `egg`, run:
```python
#easy_install scrapemark-0.9-py2.7.egg
```
For the source, extract the .tar.gz file:
```
#tar -xvf scrapemark-0.9.tar.gz
```
Then change to the directory and run the installation with `setup.py`:
```python
#cd scrapemark-0.9/
#python setup.py install
```

The following [link](https://arshaw.com/scrapemark/) shows an example of how it is used; for more examples you can visit this [link](https://arshaw.com/scrapemark/docs/examples/).

This [article](/blog/webscrapingoextracciondedatosdepaginaswebconbeautifulsoup4ypython) explains how to find the information you need to extract from the [aforementioned](https://www.timeanddate.com/worldclock/astronomy.html?n=58) page.

The idea is to extract the sunrise and sunset times for Venezuela.
The code is shown below:

```python
#!/usr/bin/env python


#Se importa sys para pasar como argumento al programa


#el url del sitio timeanddate


import sys


#Se importa pprint para mostrar la informacion en la


#consola


from pprint import pprint


#se importa scrape


from scrapemark import scrape





#se ejecuta scrape pasando el tag  html de la tabla


#donde se encuentra la fila de la informacion de la salida


#y ocultamiento del sol.


#se le pasa como argumento en la linea de comandos


#el url de timeanddate.


resultado = scrape("""


    <table class="spad">


     <tbody>


      {*


       <tr>


          <td>{{[].day}}</td>


          <td>{{[].sunrise}}</td>


          <td>{{[].sunset}}</td>


      {# ... #}


     </tr>


     *}


 </tbody>


    </table>


""",url=sys.argv[1] )





#Se muestra el resultado en pantalla


pprint (resultado)
```
The result of running the script is the following:
```python
ernesto@grievous:~$ python ej5.py http://www.timeanddate.com/worldclock/astronomy.html?n=58

fetching http://www.timeanddate.com/worldclock/astronomy.html?n=58 ...

DONE fetching.

[{'day': u'24 Oct 2013', 'sunrise': u'05:47', 'sunset': u'17:36'},

 {'day': u'25 Oct 2013', 'sunrise': u'05:47', 'sunset': u'17:36'},

 {'day': u'26 Oct 2013', 'sunrise': u'05:48', 'sunset': u'17:35'},

 {'day': u'27 Oct 2013', 'sunrise': u'05:48', 'sunset': u'17:35'},

 {'day': u'28 Oct 2013', 'sunrise': u'05:48', 'sunset': u'17:35'},

 {'day': u'29 Oct 2013', 'sunrise': u'05:48', 'sunset': u'17:34'},

 {'day': u'30 Oct 2013', 'sunrise': u'05:48', 'sunset': u'17:34'}]
```

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)