Title: Using mongodb through python.   
Date: 2014-09-21 9:00  
Category: Tutorial Python  
Tags: Canaima,Debian,Linux,Python,Ubuntu,mongodb 
lang: en
translation: true

In a [previous article (broken link)](/blog/instalarunservidormongodbendebian) I explained how to start a `mongodb` server and some usage examples.

Now I will explain how to use `mongodb` through python with `pymongo`.

There are two ways to install `pymongo`, one for Debian-based distributions:
For Python 2:
```
apt-get install python-pymongo python-pymongo-doc python-pymongo-ext
```
For Python 3:
```
apt-get install python3-pymongo python3-pymongo-ext
```
Or with `pip`:
```
pip install pymongo
```
The idea is to show how python connects to `mongodb`, how to create the database, and how to insert, list and delete documents.

Here is the script code:

```python
#!/usr/bin/env python3


# -*- coding: utf-8 -*-

from pymongo import Connection

#conexion a mongodb

con = Connection('localhost')

#Listas las base de datos

print(con.database_names())

#Conectarse a la base de datos pruebas.

db = con.pruebasdb

#Se crea una coleccion que se llama estados

estados = db.estados

#Lista de estados.

listaestados = [{'nombre': 'Carabobo', 'region':'centro','ciudades': 10},


    {'nombre': 'Lara', 'region':'centro occidente','ciudades': 8},


    {'nombre':'Merida','region':'andes','ciudades':6},


    {'nombre':'Aragua','region':'centro','ciudades':13}]

#Insertar los datos en el documento


for lista in listaestados:


    estados.insert(lista)

#Se lista un simple documento


print("Se lista un simple documento")


print("---------------------------")


print(estados.find_one({'nombre':'Carabobo'}))


#Se remueve el documento del estado Carabobo


estados.remove({"nombre" : "Carabobo"})


print("Se lista todos los documentos")


print("-----------------------------")


#Listar los datos


for i in estados.find():


    print(i)

#

print("Se cuenta la cantidad de documentos")


print("-----------------------------------")


print(estados.count())


#Borrar todos los datos


estados.drop()


con.close()


```

The result of the execution is shown below:
```
['otradb', 'pruebas', 'pruebasdb', 'nuevadb', 'local']

Se lista un simple documento

---------------------------

{'_id': ObjectId('541f0ce123d1e1604504e0e6'), 'region': 'centro', 'nombre': 'Carabobo', 'ciudades': 10}

Se lista todos los documentos

-----------------------------

{'_id': ObjectId('541f0ce123d1e1604504e0e7'), 'region': 'centro occidente', 'nombre': 'Lara', 'ciudades': 8}

{'_id': ObjectId('541f0ce123d1e1604504e0e8'), 'region': 'andes', 'nombre': 'Merida', 'ciudades': 6}

{'_id': ObjectId('541f0ce123d1e1604504e0e9'), 'region': 'centro', 'nombre': 'Aragua', 'ciudades': 13}

Se cuenta la cantidad de documentos

-----------------------------------

3

```


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)