Title: Abstracting the database engine with the Sqlalchemy ORM and python
Date: 2012-04-07 09:00
Category: Tutorial de Python
Tags: Debian,General,Linux,Python,Ubuntu
lang: en
translation: true

`ORM` or Object Relational Mapping is a programming technique for converting data between the type system used by object-oriented programming languages and the one used in a Relational Database (taken from [wikipedia](https://es.wikipedia.org/wiki/ORM)).

`Sqlalchemy` is an `ORM` tool for python that gives flexibility when developing with SQL.

Taking the previous article on [sqlite with python](/blog/sqliteconpython), the `sqlite3` module for python will be replaced by the `ORM Sqlalchemy`. This abstracts away the different statements that exist for different database engines such as `postgresql`, `mysql`, `sqlite`, so you can use any database engine with minimal changes to the program.

Here is the code showing the use of `sqlalchemy` with an `sqlite3` database:  

```python 
#!/usr/bin/env python

#Se importa sqlalchemy
from sqlalchemy import *

#Se crea la instancia del motor de la base de datos y se asocia con un
#archivo
db = create_engine('sqlite:///tutorial.db')
#se coloca la base de datos en modo no mostrar resultados 
#de las instrucciones en pantalla.
db.echo = False

#Se asocia el archivo de la base de datos a la instancia de metadatos.
metadata = MetaData(db)


#Se crea la tabla contactos tal cual el mismo ejemplo de 
#sqlite.
contactos = Table(
'contactos',metadata,
Column('id',Integer,primary_key=True),
Column('nombre', Unicode(100)),
Column('telefono',String(11)),
Column('grupo_id', ForeignKey('grupos.id')))

#Se crea la tabla de grupos tal cual el mismo ejemplo de 
#sqlite
grupos = Table(
'grupos',metadata,
Column('id',Integer,primary_key=True),
Column('grupo',Unicode(300)),
Column('descripcion',Unicode(500)))

#Se crea todas las tablas.
metadata.create_all()

#Se inserta datos en la tabla grupos.
i = grupos.insert()
i.execute(grupo='Guacara',descripcion='Ciudad de Carabobo')
i.execute({'grupo':'Valencia','descripcion':'Capital de Carabobo'},
{'grupo':'Maracay','descripcion':'Capital de Aragua'},
{'grupo':'Merida','descripcion':'Capital de Merida'})

#Se inserta datos en la tabla contactos
u = contactos.insert()
u.execute(nombre='Ernesto Crespo',telefono='04155673029',grupo_id=1)
u.execute(nombre='Pedro Perez',telefono='0295212223',grupo_id=2)
u.execute(nombre='Jhon Doe',telefono='04184488484',grupo_id=2)
u.execute(nombre='Jane Doe',telefono='04184488482',grupo_id=1)
u.execute(nombre='Pepito de los palotes',telefono='04184588484',grupo_id=3)

#Se hace consulta de la tabla contactos
s = contactos.select()
rs = s.execute()

#Se hace consultas de la tabla grupos.
t = grupos.select()
ts = t.execute()

#Se muestra la tabla grupos
print "GRUPOS"
print "-------------------------------------"
for fila in ts:
print "id: %s,Grupo: %s, Descripcion:%s" %(fila[0],fila[1],fila[2])
print "--------------------------------------"

del fila
#Se muestra la tabla contactos.
print "CONTACTOS"
print "-------------------------------------"
for fila in rs:
print "Nombre: %s, telefono %s, Grupo %s" %(fila[1],fila[2],fila[3]) 
print "--------------------------------------"

#Se borra la fila del id 1 de la tabla grupos
t = grupos.delete(text("id=1"))
t.execute()

#Se realiza una consulta de la tabla grupos
q = grupos.select()
qs = q.execute()

#Se muestra la tabla grupos, 
#ahora no tiene la fila del grupo Guacara.
print "GRUPOS"
print "-------------------------------------"
for fila in qs:
print "id: %s,Grupo: %s, Descripcion:%s" %(fila[0],fila[1],fila[2])
print "--------------------------------------"


#Se muestra los contactos del grupo 2.
print "Mostrar contactos del grupo 2"
del q
del qs
q = contactos.select(text("grupo_id=2"))
qs = q.execute()
print "-------------------------------------"
for fila in qs:
print "Nombre: %s, telefono %s, Grupo %s" %(fila[1],fila[2],fila[3]) 
print "--------------------------------------"
```    

The result of running the script is shown below:  
```
GRUPOS
-------------------------------------
id: 1,Grupo: Guacara, Descripcion:Ciudad de Carabobo
id: 2,Grupo: Valencia, Descripcion:Capital de Carabobo
id: 3,Grupo: Maracay, Descripcion:Capital de Aragua
id: 4,Grupo: Merida, Descripcion:Capital de Merida
--------------------------------------
CONTACTOS
-------------------------------------
Nombre: Ernesto Crespo, telefono 04155673029, Grupo 1
Nombre: Pedro Perez, telefono 0295212223, Grupo 2
Nombre: Jhon Doe, telefono 04184488484, Grupo 2
Nombre: Jane Doe, telefono 04184488482, Grupo 1
Nombre: Pepito de los palotes, telefono 04184588484, Grupo 3
--------------------------------------
GRUPOS
-------------------------------------
id: 2,Grupo: Valencia, Descripcion:Capital de Carabobo
id: 3,Grupo: Maracay, Descripcion:Capital de Aragua
id: 4,Grupo: Merida, Descripcion:Capital de Merida
--------------------------------------
Mostrar contactos del grupo 2
-------------------------------------
Nombre: Pedro Perez, telefono 0295212223, Grupo 2
Nombre: Jhon Doe, telefono 04184488484, Grupo 2
--------------------------------------
```

This makes it easier to access a database without using its API directly, and it also makes it possible to use any database engine in the application being developed.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
