Title: Webscraping with Python Mechanize and BeautifulSoup4
Date: 2013-10-29 9:00
Category: Tutorial Python
Tags: Canaima,Debian,Linux,Python,Ubuntu,Webscraping,Mechanize,Beautiful Soup
lang: en
translation: true

Now [Python Mechanize](/blog/emulandolanavegacionenpythonconmechanize-1) will be used together with [BeautifulSoup4](/blog/unaintroduccionabeautifulsoup4enpython) to extract the sunrise and sunset information for Venezuela, with a brief change to show how dynamic the extraction of data from a web page can be.

In this case the information is extracted from the same site, [timeanddate](https://www.timeanddate.com/astronomy/venezuela/caracas); the difference is that instead of only passing the Venezuela code (58), the month and the year are passed too.

The code shows the sunrise and sunset information for the whole months of October and November.

The code is shown below:

```python
#!/usr/bin/env python

#Se importa mechanize y cookielib

import mechanize

import cookielib

#Se importa beautifulSoup

from BeautifulSoup import BeautifulSoup

def DefinirUrl(mes,agno):


    #Se pasa el url del sitio timeanddate con la informacion


    #de la salida y ocultamiento del sol en Venezuela.


    return "http://www.timeanddate.com/worldclock/astronomy.htmln=58&month=%s&year=%s&obj=sun&afl=-11&day=1" %(mes,agno)

def CapturarInformacion(mes,agno):


    #Se crea una instancia de Browser


    br = mechanize.Browser()


    #Se crea una instancia para la Cookie


    cj = cookielib.LWPCookieJar()


    #Se asocia la instancia del cookie con el navegador.


    br.set_cookiejar(cj)


    #Se deshabilita el manejo de robots.txt


    br.set_handle_robots(False)


    #Se define el tiempo de refrescamiento


    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)


    #Se pasa el url del sitio timeanddate con la informacion


    url = DefinirUrl(mes,agno)


    #de la salida y ocultamiento del sol en Venezuela.


    #Se define las cabeceras del navegador, en este caso se le esta diciendo


    # que el navegador es un firefox desde Linux Debian


    br.addheaders = [('User-agent',


         'Mozilla/5.0 (X11; U; Linux i686; es-VE; rv:1.9.0.1)Gecko/2008071615 Debian/6.0 Firefox/9')]


    #Se abre el url


    r = br.open(url)


    #Se lee el htmml de la pagina


    html = br.response().read()


    #Se crea una instancia de BeautifulSoup pasando el html


    #a verificar


    soup = BeautifulSoup(html)


    #Se busca la palabra table, y de ahi class y se


    #busca el contenido


    #de cada columna de la tabla.


    for row in soup('table', {'class': 'spad'})[0].tbody('tr'):


        tds = row('td')


        #Se muestra la fecha y hora de la salida del sol


        print tds[0].string, tds[1].string,tds[2].string


if __name__== "__main__":


    print "Se muestra la informacion del mes de Octubre"


    print "--------------------------------------------"


    CapturarInformacion(10,2013)


    print "Se muestra la informacion del mes de Noviembre"


    print "--------------------------------------------" 

    CapturarInformacion(11,2013)
```

The result of the script is shown below:

The information for the month of October is shown
```
--------------------------------------------

1 Oct 2013 05:46 17:48

2 Oct 2013 05:46 17:47

3 Oct 2013 05:46 17:47

4 Oct 2013 05:46 17:46

5 Oct 2013 05:46 17:45

6 Oct 2013 05:46 17:45

7 Oct 2013 05:46 17:44

8 Oct 2013 05:46 17:44

9 Oct 2013 05:46 17:43

10 Oct 2013 05:46 17:43

11 Oct 2013 05:46 17:42

12 Oct 2013 05:46 17:42

13 Oct 2013 05:46 17:41

14 Oct 2013 05:46 17:41

15 Oct 2013 05:46 17:40

16 Oct 2013 05:46 17:40

17 Oct 2013 05:46 17:39

18 Oct 2013 05:47 17:39

19 Oct 2013 05:47 17:38

20 Oct 2013 05:47 17:38

21 Oct 2013 05:47 17:37

22 Oct 2013 05:47 17:37

23 Oct 2013 05:47 17:36

24 Oct 2013 05:47 17:36

25 Oct 2013 05:47 17:36

26 Oct 2013 05:48 17:35

27 Oct 2013 05:48 17:35

28 Oct 2013 05:48 17:35

29 Oct 2013 05:48 17:34

30 Oct 2013 05:48 17:34

31 Oct 2013 05:48 17:34

Se muestra la informacion del mes de Noviembre

--------------------------------------------

1 Nov 2013 05:49 17:33

2 Nov 2013 05:49 17:33

3 Nov 2013 05:49 17:33

4 Nov 2013 05:49 17:33

5 Nov 2013 05:50 17:33

6 Nov 2013 05:50 17:32

7 Nov 2013 05:50 17:32

8 Nov 2013 05:51 17:32

9 Nov 2013 05:51 17:32

10 Nov 2013 05:51 17:32

11 Nov 2013 05:51 17:32

12 Nov 2013 05:52 17:32

13 Nov 2013 05:52 17:32

14 Nov 2013 05:53 17:31

15 Nov 2013 05:53 17:31

16 Nov 2013 05:53 17:31

17 Nov 2013 05:54 17:31

18 Nov 2013 05:54 17:31

19 Nov 2013 05:54 17:32

20 Nov 2013 05:55 17:32

21 Nov 2013 05:55 17:32

22 Nov 2013 05:56 17:32

23 Nov 2013 05:56 17:32

24 Nov 2013 05:57 17:32

25 Nov 2013 05:57 17:32

26 Nov 2013 05:58 17:32

27 Nov 2013 05:58 17:32

28 Nov 2013 05:59 17:33

29 Nov 2013 05:59 17:33

30 Nov 2013 06:00 17:33
```

As shown, you can now add dynamism to the searches you want to run on a web page, extracting its information by passing data in the url. It also shows how to use `Python Mechanize` to fetch the web page and `BeautifulSoup4` to extract the needed information.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)