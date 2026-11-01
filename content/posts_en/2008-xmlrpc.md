Title: XML-RPC example in Python
Date: 2008-03-23 10:50
lang: en
Category: XML-RPC,Python

XML-RPC lets you create a web service that receives some parameters 
and returns a result. It is like a function, but the data 
travels over the network.

The example is a web service that receives a value and returns twice 
that value. Something simple.

The server:

```
#Se importa el módulo XMLRPC
from SimpleXMLRPCServer import SimpleXMLRPCServer
#Se asocia a un puerto en este caso 4242
s = SimpleXMLRPCServer(("", 4242))
#La función que toma x y devuelve el doble de x.
def twice(x):
return x*2
#se registra la función
s.register_function(twice)
#se inicia el servidor
s.serve_forever()
```

The client:
```
#Se importa el módulo ServerProxy de xmlrpclib.
from xmlrpclib import ServerProxy
#Se conecta al equipo por el puerto 4242
s = ServerProxy('http://localhost:4242')
#Se llama a la función pasandole x y devuelve el doble de x
s.twice(2)
4
s.twice(3)
6
s.twice(15)
30
```


The server shows the following messages:
```
localhost - - [24/Mar/2008 00:13:38] "POST /RPC2 HTTP/1.0" 200 -
localhost - - [24/Mar/2008 00:14:23] "POST /RPC2 HTTP/1.0" 200 -
localhost - - [24/Mar/2008 00:14:36] "POST /RPC2 HTTP/1.0" 200 -
```

These are the responses to the client's connections.
This program can be improved by checking the type of data the 
client sends, to avoid errors when a string is sent instead of a number.
