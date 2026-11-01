Title: ZeroMQ tutorial with Python. Part 8.
Date: 2012-07-02 9:00 
Category: Tutorial Python
Tags: Canaima,Debian,General,Python,Ubuntu,ZeroMQ
lang: en
translation: true

Continuing with the [ZeroMQ examples](/blog/tags). This article shows the use of the PUB/SUB pattern as in the [zeroMQ article part 4](/blog/tutorialdezeromqconpython-4) .

The difference is in the transport definition: part 4 uses tcp and this time [epgm](https://api.zeromq.org/2-1:zmq-epgm) will be used, which is for multicast.

The example shown is based on the article by Saghul Ibarra on [Saghul Ibarra's blog](https://code.saghul.net/implementing-a-pubsub-based-application-with).
The producer creates a command line where the text is passed to the consumer; the consumer receives the text and only the text defined in the subscription is shown on screen.

In the producer some options are set on the socket; the ZeroMQ site has an explanation of the [options for creating the socket](https://api.zeromq.org/2-1:zmq-setsockopt). LINGER with a zero parameter makes unsent messages be discarded.

The producer code is shown below:
```python
#!/usr/bin/env python

# 

# producer

#Se importa ZeroMQ

import zmq

#Se crea la instancia de la clase Context.

context = zmq.Context()

#Se define el socket con parametro PUB

socket = context.socket(zmq.PUB)

#Se define unas opciones en el socket

#esta opcion LINGER con valor cero, descarta mensajes no enviados

socket.setsockopt(zmq.LINGER, 0)    

#Se conecta al socket a la IP y puerto

#por medio de multicast

socket.connect('epgm://192.168.10.96:5000')

#Se crea un ciclo

#si se envia el texto salir, se envia y luego finaliza el ciclo

#si no, se envia el texto

while True:

 mensaje = raw_input("->")

 print mensaje

 socket.send(mensaje)

 if mensaje == "salir": break

socket.close()
```

The consumer program code is the following: 
```python
#!/usr/bin/env python

#Importar zeroMQ

import zmq

#Se crea la instancia de la clase contexto

context = zmq.Context()

#Se define el socket con parametro SUB

socket = context.socket(zmq.SUB)

#Se conecta el socket a la IP y puerto del productor

#con el transporte epgm

socket.connect('epgm://192.168.10.96:5000')

#Se define los textos que se recibe la informacion.

#prueba, hora y salir.

socket.setsockopt(zmq.SUBSCRIBE, 'prueba')

socket.setsockopt(zmq.SUBSCRIBE, 'hora')

socket.setsockopt(zmq.SUBSCRIBE, 'salir')

#Se define un ciclo,

#se recibe la informacion

#Si el texto es salir se muestra en pantalla 

#finaliza el ciclo, si no se muestra

#el texto en pantalla

while True:

    rcv = socket.recv()

    print rcv

    if rcv == "salir": break
```
  
The following figures show the result of running both programs: 
Producer:

![](./images/tutorialdezeromqconpython8-1.png) 

Consumer:

![](./images/tutorialdezeromqconpython8-2.png) 

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)