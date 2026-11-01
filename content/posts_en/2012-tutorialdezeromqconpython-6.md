Title: ZeroMQ tutorial with Python (PUSH/PULL). Part 6.
Date: 2012-06-03 9:00 
Category: Tutorial Python
Tags: Canaima,Debian,General,Python,Ubuntu,ZeroMQ
lang: en
translation: true

Continuing the series on [ZeroMQ](/blog/tags).

This article explains how PUSH and PULL work.

The idea is that there is a sender (emisor), which sends strings to the "workers", which are processed in different ways or in the same way (a way of achieving scalability). Once the "workers" have processed the information received from the sender, they pass it to the result node (resultado), which displays the information on screen.

The figure shows the process just explained:

![](./images/tutorialdezeromqconpython6-1.png) 

The sender code is the following:
```python
#!/usr/bin/python

#Se importa zeroMQ y random

import zmq

import random

#Se crea la instancia del contexto

context = zmq.Context()

#Se crea el socket con el argumento PUSH

envio =context.socket(zmq.PUSH)

#Se asocia el socket a escuchar todas las IPs y el puerto 5557

envio.bind("tcp://*:5557")

#se muestra que es necesario esperar que arranquen los workers

print "Hay que esperar que los workers se inicien"

#Al dar enter se inicia el proceso de transmision

raw_input()

print "Se inicia la transmision del trabajo..."

#tupla de strings que se van a enviar

cadenas = ['hola', 'aloha','hello','buenas noches','buenas tardes','buenos dias','bienvenido']

#Se crea un ciclo para recorrer la tupla

for i in range(len(cadenas)):

 cadena = cadenas[i]

 envio.send(cadena)

 print "Enviando: {0}".format(cadena)

```

The worker code is the following:
```python
#!/usr/bin/python

#Se importa ZeroMQ y sleep de time

import zmq

from time import sleep

#Se crea la instancia del contexto

context = zmq.Context()

#Se define el Socket con argumento PULL

recepcion = context.socket(zmq.PULL)

#Se conecta el socket a localhost puerto 5557

#Es el puerto donde origen envia con PUSH los datos

recepcion.connect("tcp://localhost:5557")

#Se crea el socket de envio de los datos procesados con argumento PUSH

envio = context.socket(zmq.PUSH)

#Se conecta el socket a localhost y puerto 5558

envio.connect("tcp://localhost:5558")

#Se genera un ciclo

#donde se recive lo transmitido por origen

#se procesa (se coloca en mayusculas)

#se muestra en pantalla y se envia.

#los ciclos tienen un retardo de 1 seg

while True:

 cadena = recepcion.recv()

 print "Proceso:{0}".format(cadena)

 envio.send(cadena.upper())

 sleep(1)

El código de resultado es el siguiente:

#!/usr/bin/python

#Se importa ZeroMQ

import zmq

#Se crea la instancia del contexto

context = zmq.Context()

#Se crea el socket PULL que recibe los mensajes de los workers

recepcion = context.socket(zmq.PULL)

#Se asocia el socket a escuchar todas las IPs en el puerto 5558

#el puerto donde los workers envian los mensajes

recepcion.bind("tcp://*:5558")

#Se inicia un ciclo donde se recibe los mensajes

#de los workers y se muestra en pantalla

while True:

 mensaje = recepcion.recv()

 print "Recibo: {0}".format(mensaje)

```

You have to start the scripts resultado, worker (worker1 and an identical copy called worker2) and origen.

The following figure shows the output of origen:

![](./images/tutorialdezeromqconpython6-2.png) 

The following figure shows the output of worker1 and worker2:

![](./images/tutorialdezeromqconpython6-3.png) 

![](./images/tutorialdezeromqconpython6-4.png) 

Note that the workers share the work evenly.

The following figure shows what resultado displays on screen:

![](./images/tutorialdezeromqconpython6-5.png) 

As you can see, the workers process the text strings they receive from origen, convert them to uppercase and send them to resultado so that it can display them on screen.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)