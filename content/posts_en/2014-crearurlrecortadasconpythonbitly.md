Title: Creating shortened URLs with Python (bit.ly)  
Date: 2014-01-25 9:00  
Category: Tutorial Python  
Tags:  Canaima,Debian,General,Python,Ubuntu,bit.ly
lang: en
translation: true  

We all know how popular URL shortening sites have become because of the microblogging limit of 144 characters (where we have to save on typing).

Shorteners reduce the number of characters a url we want to share can have.

There are several sites that make shortening URLs easy:

- Bit.ly
- Goo.gl
- TinyURL  

In this case we will try `bit.ly`; the site has an API so it can be accessed from a program, and its documentation is [here](https://dev.bitly.com/api.html).

[You need to register the application (broken link)](https://bitly.com/a/sign_in?rd=/a/oauth_apps) and then look up the [apikey (broken link)](https://bitly.com/a/your_api_key).

The script to be written requires the following python modules:

- `urllib`
- `urllib2`
- `re`
- `simplejson`  

The script is simple: it imports the modules to use, passes the user and the apikey obtained from ' `bit.ly` and calls the function that shortens the url.

The code is shown below:
```python
#!/usr/bin/python


# Script que convierte un url a un url recortado por medio de bit.ly


# requiere urllib, urllib2, re, simplejson





#Se intenta importar los modulos que se necesito si no devuelve mensaje de error


#donde se menciona que se requiere los los modulos.


try:


  from re import match


  from urllib2 import urlopen, Request, HTTPError


  from urllib import urlencode


  from simplejson import loads


except ImportError, e:


  raise Exception('Required module missing: %s' % e.args[0])





#Definicion de usuario y clave bit.ly


user = "o_5j8ri77vv6aa"


apikey  = "R_172fe1dcf183470c85ce345aaa784cf9395"





#Funcion que recorta el url, se le pasa un url y devuelve el mismo recortado


def shorten(url):


    #Se maneja la excepcion de error http





    try:


        #Se le pasa los parametros url, user, apikey y formato de serializacion en


        #este caso json


        params = urlencode({'longUrl': url, 'login': user, 'apiKey': apikey, 'format': 'json'})


        #Se hace la solicitud al api de bit.ly pasandole los parametros


        req = Request("http://api.bit.ly/v3/shorten?%s" % params)


        #Se abre la respuesta.


        response = urlopen(req)


        #Se lee y se carga


        j = loads(response.read())


        #Si el codigo de estatus de la peticion http es 200


        #se retona el url recortada


        if j['status_code'] == 200:


            return j['data']['url']


        #Si no es 200 se genera una excepcion pasando el mensaje de estatus


        raise Exception('%s'%j['status_txt'])


    #Si no se logra la conexion http se devuelve un mensaje de error.


    except HTTPError, e:


        raise('HTTP error%s'%e.read())

if __name__ == '__main__':


    #Se importa argv del modulo sys


    from sys import argv


    #Si no inicia el argumento con http se devuelve un mensaje de error 


    #solicitando que se coloque el http al url.


    if not match('http://',argv[1]):


        raise Exception('Debe iniciar con "http://"')


    #Se muestra en la consola el url recortado

    print shorten(argv[1])

```

Running the script gives the following:  
```
ernesto@grievous:~/bin/python$ ./acortarurl.py http://blog.crespo.org.ve

http://bit.ly/LXP0QB

```

With the script you can now shorten urls, for example from the previous article where we [get the list of a blog's articles through rss](/blog/jugandoconrssdelblogdesdepython).

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)