Title: Session handling in the sqlalchemy ORM
Date: 2013-09-18 9:00
Category: General
Tags: General,Python
lang: en
translation: true
 
Some time ago I explained how to create tables for a `sqlite3` database, insert data, remove it and query it; the article is called [Database engine abstraction with the Sqlalchemy ORM and python](/blog/abstracciondelmotordebasededatosconelormsqlalchemyypython).

Before you start trying out what is written in this article, you need to work through the article mentioned above so that you have the database with its data ready to be used in this article.

Now I explain how to use tables with data that already exist, by creating a session for the database.

This article is based on an [English sqlalchemy tutorial](https://mapfish.org/doc/tutorials/sqlalchemy.html) or the [step-by-step sqlalchemy tutorial (broken link)](http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html).

The first thing to do is create a `model.py` file that will contain the database model.
```python
#Se importa el módulo datetime

import datetime

#Se importa schema y tupes de sqlalchemy

from sqlalchemy import schema, types



#Se instancia la clase MetaData.

metadata = schema.MetaData()



#Se crea la función now que devuelve la hora actual.

def now():

    return datetime.datetime.now()



#Se crea la instancia table con los campos de la tabla grupos

grupos_table = schema.Table('grupos',metadata,

        schema.Column('id',types.Integer,primary_key=True),

        schema.Column('grupo',types.String(300),nullable=False),

        schema.Column('descripcion',types.String(500),nullable=False),

)


#Se crea la instancia table con los campos de la tabla contactos

contactos_table = schema.Table('contactos',metadata,

        schema.Column('id',types.Integer,primary_key=True),

        schema.Column('nombre',types.String(100),nullable=False),

        schema.Column('telefono',types.String(11),nullable=False),

        schema.Column('grupo_id',types.Integer,nullable=False),

)



#Se crea la clase Contactos y Grupos que heredan de object y sólo tienen pass.

class Contactos(object): pass

class Grupos(object): pass



#Se mapea la Clase Contactos con la tabla contactos_table

orm.mapper(Contactos, contactos_table)

#Se mapea la Clase Grupos con la tabla grupos_table

orm.mapper(Grupos,grupos_table)
```

With this code the existing tables and their fields are mapped.

Now create a file called `prueba-db.py` that will open the database session through the `model.py` module, where some queries, insertions and removals of data will be performed.
```python
#!/usr/bin/env python

# -*- coding: utf-8 -*-



import model

from sqlalchemy import orm

from sqlalchemy import create_engine



#Crear un engine y crear todas las tablas necesarias

engine = create_engine('sqlite:///tutorial.db', echo=False)

model.metadata.bind = engine

model.metadata.create_all()



# Configurar la sesion



sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,

            expire_on_commit=True)

session = orm.scoped_session(sm)



#Se realiza una consulta a la tabla grupos

print "Consulta inicial de la tabla contactos"

consulta = session.query(model.Contactos).all()

for lista in consulta:

    print lista.nombre,lista.telefono

print "--------------------------------"





#Agregar un contacto

contacto = model.Contactos()

contacto.nombre = u"Luisa Gonzalez"

contacto.telefono = u"04155555555"

contacto.grupo_id = 2

session.add(contacto)

session.flush()

session.commit()





#Se realiza una consulta a la tabla grupos

print "Consulta la tabla contactos con el dato incorporado"

consulta = session.query(model.Contactos).all()

for lista in consulta:

    print lista.nombre,lista.telefono

print "--------------------------------"

    



#Borrar un contacto

session.delete(contacto)

session.flush()

session.commit()



#Se realiza una consulta a la tabla grupos

print "Consulta la tabla contactos luego de borrar el dato"

consulta = session.query(model.Contactos).all()

for lista in consulta:

    print lista.nombre,lista.telefono

print "--------------------------------"
```

The result of running the `pruebas-db.py` script is shown below:
```
Consulta inicial de la tabla contactos

Ernesto Crespo 04155673029

Pedro Perez 0295212223

Jhon Doe 04184488484

Jane Doe 04184488482

Pepito de los palotes 04184588484

--------------------------------

Consulta la tabla contactos con el dato incorporado

Ernesto Crespo 04155673029

Pedro Perez 0295212223

Jhon Doe 04184488484

Jane Doe 04184488482

Pepito de los palotes 04184588484

Luisa Gonzalez 04155555555

--------------------------------

Consulta la tabla contactos luego de borrar el dato

Ernesto Crespo 04155673029

Pedro Perez 0295212223

Jhon Doe 04184488484

Jane Doe 04184488482

Pepito de los palotes 04184588484

--------------------------------
```

This way you can run queries, removals and insertions through `sqlalchemy` with sessions.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)