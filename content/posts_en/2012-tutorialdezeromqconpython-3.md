Title: ZeroMQ Tutorial with Python. Part 3.
Date: 2012-05-28  9:00 
Category: Tutorial Python
Tags: Canaima,Debian,General,Linux,Python,Ubuntu,ZeroMQ
lang: en
translation: true

Building on the article [ZeroMQ part 1](/blog/tutorialdezeromqconpython-1), you can create several servers (like an application cluster). 

This time 3 server scripts are created; they can be on the same machine or on different machines. The only thing I changed in each script is the port it listens on for the service.

In the client, 3 sockets are created with the ports where the 3 servers listen.

The idea is for the client to send a message, and for the servers to receive it and send it back to the client.

The code of the client-side script is the following:
```python
#!/usr/bin/env python

#importar zeromq
import zmq

#Se crea una instancia del contexto
context = zmq.Context()
#Se crea el socket con parametro peticion (REQ)
socket = context.socket(zmq.REQ)
#Se crean 3 sockets con la IP y los 3 puertos donde escucha 
#los 3 servidores.
socket.connect("tcp://127.0.0.1:5000")
socket.connect("tcp://127.0.0.1:6000")
socket.connect("tcp://127.0.0.1:7000")
#Se crea un ciclo de 100 repeticiones
for i in range(100):
    #Se crea el string del mensaje
    mensaje = "mensaje %s" % i
    #Se envia el mensaje
    socket.send(mensaje)
    #Se muestra en pantalla el mensaje enviado
    print "Enviando", mensaje
    #Se recibe el mensaje de vuelta
    msg_in = socket.recv()
```  

The server scripts are shown below:
Server 1:  

```python
#!/usr/bin/env python

#Se importa zeroMQ
import zmq
#Se crea la instancia del contexto
context = zmq.Context()
#Se crea el socket pasandole como parametro respuesta (REP)
socket = context.socket(zmq.REP)
#Se asocia el socket a la IP y el puerto
socket.bind("tcp://127.0.0.1:5000")

#Se crea un ciclo
while True:
    #Se recibe el mensaje
    mensaje = socket.recv()
    #Se muestra en pantalla el mensaje recibido
    print "Recibiendo", mensaje
    #Se envia el mensaje de regreso al cliente
    socket.send(mensaje)  
```  
 
Server 2:  
```python
#!/usr/bin/env python

#Se importa zeroMQ
import zmq
#Se crea la instancia del contexto
context = zmq.Context()
#Se crea el socket pasandole como parametro respuesta (REP)
socket = context.socket(zmq.REP)
#Se asocia el socket a la IP y el puerto
socket.bind("tcp://127.0.0.1:6000")

#Se crea un ciclo
while True:
    #Se recibe el mensaje
    mensaje = socket.recv()
    #Se muestra en pantalla el mensaje recibido
    print "Recibiendo", mensaje
    #Se envia el mensaje de regreso al cliente
    socket.send(mensaje)  
```  
 
Server 3:  
```python
 
#!/usr/bin/env python

#Se importa zeroMQ
import zmq
#Se crea la instancia del contexto
context = zmq.Context()
#Se crea el socket pasandole como parametro respuesta (REP)
socket = context.socket(zmq.REP)
#Se asocia el socket a la IP y el puerto
socket.bind("tcp://127.0.0.1:7000")

#Se crea un ciclo
while True:
    #Se recibe el mensaje
    mensaje = socket.recv()
    #Se muestra en pantalla el mensaje recibido
    print "Recibiendo", mensaje
    #Se envia el mensaje de regreso al cliente
    socket.send(mensaje)
```  

Next, start the 3 servers and then the client:
The following figure shows the messages sent by the client:

![](./images/tutorialdezeromqconpython3-1.png) 

The figures of the 3 servers are shown below:

Server 1:

![](./images/tutorialdezeromqconpython3-2.png) 

Server 2:

![](./images/tutorialdezeromqconpython3-3.png) 

Server 3:

![](./images/tutorialdezeromqconpython3-4.png) 

Looking at the 3 server figures, you can see how the reception of messages is distributed evenly.

 This scheme could later be made somewhat more complex by adding a queue between the clients and the servers. 

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)