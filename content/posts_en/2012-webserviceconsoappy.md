Title: WebService with Soappy
Date:  2012-02-06 09:30
Category: Tutorial de Python 
Tags: Debian,General,Linux,Python,Ubuntu
lang: en
translation: true

A long time ago I wrote an example of how to use [xml-rpc ](/blog/xmlrpc) from python as a webservice.
In this case I will explain the use of another protocol derived from `xml-rpc` called `SOAP` (Simple Object Access Protocol).

`SOAP` is a standard protocol that defines how two objects in different processes can communicate by exchanging `XML` data. You can find more information on the [wikipedia](https://es.wikipedia.org/wiki/SOAP) page.


In python there is a module for working with SOAP called [soappy](https://pypi.org/project/SOAPpy/). The first thing to do is install it.  

```
#apt-get install python-soappy
```

The idea is to create 4 functions, for addition, subtraction, multiplication and division, register them in the `SOAP` service, bring up the server and make the calls from the client.

The `SOAP` server program is the following:  
```
#!/usr/bin/env python

import SOAPpy
	
#Funciones que devuelven la suma, resta, multiplicacion y division de 2 numeros
	
def suma(a,b):
    return a+b

def resta(a,b):
    return a-b
	
def multiplicacion(a,b):
    return a*b
	
def division(a,b):
    return a/b
	
#Se crea la instancia del servicio SOAP en el equipo por el puerto 8080.
server = SOAPpy.SOAPServer(("localhost", 8080))
	
#Registro de las funciones suma,resta, multiplicacion y division
#en el servicio SOAP.
server.registerFunction(suma)
server.registerFunction(resta)
server.registerFunction(multiplicacion)
server.registerFunction(division)
	
#Levantar el servicio SOAP.
server.serve_forever()
```
The `SOAP` client program is the following:  
```
#!/usr/bin/env python

#Se importa el modulo SOAPpy
import SOAPpy
	
#Se crea la instancia del proxy SOAP
#a el servidor SOAP
server = SOAPpy.SOAPProxy("http://localhost:8080/")

#Se llama las funciones registradas en el servidor SOAP
print "El resultado de la suma es: ", server.suma(5,10)
print "El resultado de la resta es: ",server.resta(20,5)
print "El resultado de la multiplicacion es: ", server.multiplicacion(10,5)
print "El resultado de la division es: ", server.division(10,3)
```
	
Give both files execute permissions, run the server first and then the client, which returns the following result:

Each program is run in a separate console.  

```ecrespo@jewel:~/bin$ ./soapservidor.py```
	
```
ecrespo@jewel:~/bin$ ./soapcliente.py
El resultado de la suma es:  15
El resultado de la resta es:  15
El resultado de la multiplicacion es:  50
El resultado de la division es:  3
```	

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
