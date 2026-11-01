Title: ZeroMQ Tutorial with python . Part 1.
Date: 2012-05-26 9:00
Category: Tutorial Python
Tags: Canaima,Debian,General,Python,ZeroMQ
lang: en
translation: true

[ZeroMQ](http://zeromq.org/) is a messaging library that lets you build complex communication systems with little effort (queue systems).

`ZeroMQ` is faster than other messaging systems based on the `AMQP` protocol.

This article will explain a simple use of zeroMQ in a client and server style. Port 5000 will be used for communication between the client and the server. The client randomly generates 2 numbers and passes them to the server, which performs a calculation and returns the result to the client, which shows the result on screen. The numbers are generated 1000 times, and then the letter q is sent to the server, which is the signal to terminate the server.


To install `zeroMQ` for python you have to install [python-zmq](http://zeromq.org/bindings:python) and/or `python3-zmq` for python3:

```
#apt-get install python3-zmq python-zmq
```

Server: The server code is the following:
```python
#!/usr/bin/env python
#Se importa zeromq
import zmq
#Se crea la instancia del contexto de zmq.
context = zmq.Context()
#Se define el socket con parámetro respuesta REP.
socket = context.socket(zmq.REP)
#Se asocia la dirección IP y el puerto donde el servidor escucha las peticiones.
socket.bind("tcp://127.0.0.1:5000")
#Se define un contados
c = 1
#Se genera un ciclo que sólo finaliza si se recibe la letra q.
while True:
    #Se recibe los mensajes.
    msg = socket.recv()
    #Se consulta si la longitud del mensaje es 1 y es la letra q se termina el ciclo
    if len(msg) == 1 and msg == "q":
        break
    #Se separa los datos que viene en un string separados por :
    datos = msg.split(":")
    #se realiza una suma con los datos recibidos.
    resultado = int(datos[0]) + int(datos[1])
    #Se muestra en pantalla el resultado
    print "Iteracion: %s ,He recibido: %s, el resultado es: %s "  %(c,msg,resultado)
    #Se envía el resultado al cliente
    socket.send(str(resultado))
    #Se incrementa el contador.
    c += 1
```
 
The client code is the following:
```python
#!/usr/bin/env python
#Se importa zeromq y random
import zmq
import random


#Se crea la instancia del contexto
context = zmq.Context()


#Se crea el socket y se para el argumento de petición REQ
socket = context.socket(zmq.REQ)


#Se coencta a la IP y puerto donde escucha el servidor
socket.connect("tcp://127.0.0.1:5000")


#Se genera un ciclo de 1000 repeticiones
for i in range(1000):


    #Se crea el string con el mensaje, se pasa 2 aargumentos aleatorios
    msg = "%s:%s" %(random.randint(1, 1000),random.randint(1, 1000))


    #Se envia el mensaje al servidor
    socket.send(msg)


    #Se recibe el mensaje del servidor
    msg_in = socket.recv()


    #Se muestra en patalla los datos y el resultado
    print "Iteracion: %s, Enviado: %s, Recibido: %s" %(i,msg,msg_in)


    #Si se llea a la iteración 999 se envía la letra q para finalizar
    if i ==  999: socket.send("q")

```
The result on the client side and on the server side is the following:

The figure shows the execution of the server script:

![](./images/tutorialdezeromqconpython1-1.png) 

The figure shows the execution of the client script:

![](./images/tutorialdezeromqconpython1-2.png) 
##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)

