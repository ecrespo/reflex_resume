Title: Sqlite with python
Date: 2012-04-04 09:00
Category: Tutorial de Python 
Tags:  General,Python
lang: en
translation: true

The `pysms-send` program will get some improvements, among them an address book for contacts.

For this, `sqlite3` or `mongoDB` will be tried. This article will work with `sqlite3`. Two tables will be created, one for contacts and one for groups. The contacts table has the fields id, contact name, phone and group. The group table will have the fields id, group name and group description.

In the contacts table, the group field is a reference to the id of the group table, so each contact is related to a group.


The `contactos.sql` file contains the following:  
```
create table contactos (
id integer primary key,
nombre text not null,
grupo integer references grupos(id)
on delete restrict
deferrable initially deferred,
telefono text not null default 'Desconocido',
unique (nombre,telefono));

create table grupos (
id integer primary key,
nombre text not null,  
descripcion text not null CHECK(descripcion !=''),
unique (nombre)); 
```

The `contactos` table has the id field, which is an integer and the primary key; the name field is not null; the group field references the id field of the grupos table; the phone field is a non-null text with a default value of unknown; and the unique values are the name and the phone, which prevents repeated phone numbers.

The `grupos` table has the id field, which is an integer and the primary key; the name field is non-null text; the description field is not null and is checked so that it is not an empty string; and the unique field is the name.

To generate the database, the following statement is run:  

```
sqlite3 sms.db < sms.sql
```

This creates the `sqlite` database in the `sms.db` file.

If you want to interact with the database, run `sqlite3` with the name of the database and an interpreter will open:
```
ecrespo@jewel:~/bin/python$ sqlite3 sms.db 
SQLite version 3.7.11 2012-03-20 11:35:50
Enter ".help" for instructions
Enter SQL statements terminated with a ";"
sqlite>
```

Next, a group is added to the `grupos` table:  

```
sqlite> insert into grupos (nombre,descripcion) values ('Guacara','Ciudad del Estado Carabobo');
```

Now a contact is added to the `contactos` table:  

```
insert into contactos (nombre,grupo,telefono) values ('Ernesto Crespo',1,'04315633119');
```


Query the `grupos` table and then the `contactos` table:  
```
sqlite> select * from grupos;
1|Guacara|Ciudad del Estado Carabobo
sqlite> select * from contactos ;
1|Ernesto Crespo|1|04315633119
```

To delete the `contacto`, run:  

```
sqlite> delete from contactos where id=1;
```

The id was used to delete the contact.

Next, a series of python scripts will be created that insert data into the database, query it and delete it (the basic actions on a database).
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Se importa el modulo sqlite3
import sqlite3

#Se crea la funcion main
def main():
#Se establece la instancia connect a la base de datos sms.db
con = sqlite3.connect("sms.db")
#Se crea el cursor que permite la ejecucion de instrucciones sql
cur = con.cursor()

#Se crea una lista con tuplas como sus elementos.
#Las tuplas contienen los datos a insertar en la tabla grupos.
datos =[('valencia' ,'Capital Estado Carabobo'),
('Maracay','Capital Estado Aragua'),
('Barquisimeto','Capital del Estado Lara'),]
#Se recorre la lista
for t in datos:
cur.execute('insert into grupos (nombre,descripcion) values (?,?)',t)
#Se realiza la transaccion.
con.commit()

#Ahora se lista los datos de la tabla grupos
cur.execute('select * from grupos')
#Se captura uno
fila = cur.fetchone()
#Se recorre cada fila
while fila:
#Se muestra los elementos nombre y descripcion.
print fila[1],fila[2]
#Se pasa a la siguiente fila
fila = cur.fetchone()

#Se cierra el cursor
cur.close()
#Se cierra la conexion.
con.close()

#Se sale de la funcion .
return 0

if __name__ == '__main__':
main()
```
    
When the script is run, it returns the list of `grupos` with their description:
```
ecrespo@jewel:~/bin/python$ python grupos-sms.py 
Guacara Ciudad del Estado Carabobo
valencia Capital Estado Carabobo
Maracay Capital Estado Aragua
Barquisimeto Capital del Estado Lara
```

##  ##
===
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:


![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)