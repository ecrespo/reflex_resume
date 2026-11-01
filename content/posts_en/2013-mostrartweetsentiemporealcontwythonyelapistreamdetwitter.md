Title: Show tweets in real time with twython and the Twitter Stream API 
Date: 2013-09-26 9:00
Category: Tutorial Python
Tags: Debian,General,Linux,Python,Twitter,Ubuntu
lang: en
translation: true

This article uses the twitter Stream API to watch the flow of tweets the user receives or what is published on twitter in general.

The idea is to use `twython` with the [TwythonStreamer](https://twython.readthedocs.org/en/latest/usage/streaming_api.html) class to access the twitter stream API.

From the twitter API, [GET user (broken link)](https://developer.twitter.com/docs/api/1.1/get/user) will be shown, which streams the messages of a single user.

I will also show how to use [POST status filter (broken link)](https://developer.twitter.com/docs/api/1.1/post/statuses/filter), which shows all public tweets that contain a word (track).

The first example is with `GET user`, with the code below:
```python
#!/usr/bin/env python

# -*- coding: utf-8 -*-

#Se define el token de la aplicacion

CONSUMER_KEY = 'xxxxx'

CONSUMER_SECRET = 'xxxxx'

#Se define el acceso al usuario

ACCESS_KEY = 'xxxxx'

ACCESS_SECRET = 'xxxxx'

#Se importa TwythonStreamer

from twython import TwythonStreamer

#Se crea la clase MiStream que hereda de TwythonStreamer 

class MiStream(TwythonStreamer):

    #Se crea el metodo on_success que recibe data

    def on_success(self, data):

        #Si la palabra 'text' se encuentra en data se muestra en pantalla

        #su contenido

        if 'text' in data:

            print data['text'].encode('utf-8')

            #Si se desea desconectar luego del primer resultado?

            #self.disconnect()

    #Se crea el metodo on_error que recibe el codigo de estatus y data y se muestra en pantalla

    def on_error(self, status_code, data):

        print status_code, data

# Requires Authentication as of Twitter API v1.1

#Se crea la instancia de la clase MiStream con los parametros de autenticacion del API v1.1 de twittter.

stream = MiStreame(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

#Se recibe los tweets del usuario.

stream.user()
```
The result is shown below:

```python
NASA puts papers from Curiosity rover behind paywall; @mbeisen points out this is illegal &amp; shares them http://t.co/UB1jQfRpLR #openaccess

ICYMI: Boost Mobile now offering Boost Warp 4G http://t.co/qvZKtZXqOn

Empoderando a la ciudadanía para mejorar la educación en México http://t.co/GnTqhDWqzv

BREAKING: Dodgers say man killed in altercation with Giants fans in SF was son of team security guard: http://t.co/CkB75Nkt0V

RT @Anonymous_Prodi: Posible bomba nuclear de baja intensidad en Siria http://t.co/uSjjVI1T3A @Famelica_legion @AquiyAhora_2013 @wikinotici…

guía de gobierno electrónico local: http://t.co/X6i7f8NHFe  servicios electrónicos orientados al ciudadano #eGov

¡Felicidades también a @jenniferpsayago por ser la ganadora de estos increíbles productos #Samsung y @Oakley_VE! http://t.co/ZfZnNtZtCf

#linux #fedora  #art  Re: Request to join the Design Team http://t.co/CuAuncfFPU

Del Gobierno Abierto como Política y la Apertura de Datos como Programa Público http://t.co/4fmZAHA8x6  #OpenData #OGov

#linux #fedora  #art  Re: Request to join the Design Team http://t.co/RiHSMifvBQ

3D printer duplicates paintings down to the last brush stroke http://t.co/suC4T3P2Lr #3DPrinting #art

Maduro: Mi ausencia en la ONU se debió a provocaciones que habían en mi contra http://t.co/Ed1ufBiPCW

Venezuela: Turismo “raspatarjetas” mató al turismo http://t.co/Rd18XiZYZu @kaosenlarednet mm

Como las iniciativas de Datos Abiertos pueden mejorar la vida en las Ciudades? http://t.co/j8FJOUd5mk  #OpenData

RT @csoghoian: Want to read the details of some NSA #LOVEINT surveillance abuses? Now you can, thanks to Senator @ChuckGrassley http://t.co…

¿Me está diciendo usted q su teoría mágica es: no tener teoría? Creo que eso no es muy anarquista, ni lógico tampoco @fascaso @loadupyourgun

Venezuela: Turismo “raspatarjetas” mató al turismo http://t.co/Rd18XiZYZu @kaosenlarednetmmmmm

RT @C354R_B3RMUD3Z: Te interesa saber de #Soporte Tecnico en #Gnu/Linux? #inscribete, es totalmente #gratuito informate por 04243165766

RT @csoghoian: Are you an NSA analyst? Suspect that your husband is cheating on you? Tap his phone, don't get prosecuted. Page 3 of http://…

Saturday Night Live lanza canal oficial de YouTube disponible para todo el mundo http://t.co/LDFcwFxsx0

Microsoft donated $100k to IPython http://t.co/sU2UP07dJ8

Crece el huracán: exitosos Niños Cantores de diversas tendencias políticas nos dieron hoy públicamente su apoyo http://t.co/SGDvxPrczA

How is everyone? I feel like I've been away for years when it's only been a few days.
```

Now all public tweets containing the word python are shown. This is achieved by replacing the last line of the previous code with `stream.statuses.filter`, passing the `track` argument with the word to search for:
```python
stream.statuses.filter(track='python')
```
The result is shown below:
```python
lunes que viene #PUG  con pizza, cerveza, #python en @Dlabs_co . Yo no me la perdería...

Monty Python - The man who is alternately rude and polite: :#NowPlaying.#ClassicComedies..#ComedyGreats ,,,#Comedy.  http://t.co/IO3juw6nfD

Like a Kungfu master, a Pythonista knows how to kill with a single finger, and never to actually do it. http://t.co/xx0Sb8SsWV

RT @jpcolino: Python + Hadoop: Real Python in Pig trunk http://t.co/i4NZXrofvq

Affiliate Freelancer, Freelancing September 26, 2013 at 04:51PM Python web front end development by vishalchavda... http://t.co/V45nPv3LVI


Compressed 4h of Python, Win32 dbg API and Intel PIN in 2h. Still people seemed to like it. I guess a lot of people are into BSDM at @brucon


Go vs. Python: 10% longer, 10 times faster. http://t.co/v640YolHW4 and concurrent, statically compiled, and the libraries are all modern.


Quantitative Economics | #python #ebook http://t.co/eVjlO9VBoE


@MikeKellyofEM Hopefully a Monty Python style parrot...


por um tutorial de como aprender python em um dia


@tommyd_95 this could descend into a scene from a Monty Python movie ))
```

This way you can improve the capture of tweets in real time from a user's timeline or from all public tweets. 

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)