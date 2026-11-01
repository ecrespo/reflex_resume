Title: Installing a mongodb server on Debian  
Date: 2014-09-13 9:00  
Category: Linux,Desarrollo  
Tags: Canaima,Debian,General,Linux,Ubuntu,mongodb
lang: en  
translation: true  

`Mongodb` is a non-relational (nosql) database that is widely used at the moment and is free software.

To install the server and the client on Debian, run:
```
apt-get install mongodb mongodb-clients mongodb-server
```
Configuring `mongodb`.
The configuration of the `mongodb` server is in `/etc/mongodb.conf`:
```
# donde se almacena los datos
dbpath=/var/lib/mongodb
#El log se guarda en el archivo:
logpath=/var/log/mongodb/mongodb.log
#Se define agregar info al log.
logappend=true
#Se define la ip y el puerto donde escuchará mongodb
bind_ip = 127.0.0.1
port = 27017
# Se habilita el journaling, http://www.mongodb.org/display/DOCS/Journaling
journal=true
# Se habilita o deshabilita la autenticación, por defecto está deshabilitado
#noauth = true
#auth = true
```
Start the service (since I am using systemd, the systemctl command is used):
Start the service:
```
systemctl start mongodb.service
```
Service status:
```
systemctl status mongodb.service 
mongodb.service - An object/document-oriented database
   Loaded: loaded (/lib/systemd/system/mongodb.service; disabled)
   Active: active (running) since sáb 2014-09-13 21:08:10 VET; 2s ago
     Docs: man:mongod(1)
 Main PID: 5542 (mongod)
   CGroup: /system.slice/mongodb.service
           └─5542 /usr/bin/mongod --config /etc/mongodb.conf

sep 13 21:08:10 grievous systemd[1]: Starting An object/document-oriented database...
sep 13 21:08:10 grievous systemd[1]: Started An object/document-oriented database.
sep 13 21:08:10 grievous mongod[5542]: all output going to: /var/log/mongodb/mongodb.log
```

Check that the process is up:
```
ps aux | grep mongo
mongodb   5542  0.4  0.9 385176 38512 ?        Ssl  21:08   0:01 /usr/bin/mongod --config /etc/mongodb.conf
```
Check that the ports are open:
```
netstat -anp  | grep mongo
tcp        0      0 127.0.0.1:27017         0.0.0.0:*               LISTEN      5542/mongod     
tcp        0      0 127.0.0.1:28017         0.0.0.0:*               LISTEN      5542/mongod     
unix  2      [ ACC ]     STREAM     LISTENING     138512   5542/mongod         /tmp/mongodb-27017.soc
``` 
Connect to the mongodb server:
```
#mongo
MongoDB shell version: 2.4.10
connecting to: test
>
```
Select a database:
```
> db
test
```
Show the list of database names:
``` 
> show dbs 
local 0.078125GB
```
Switch to a new database called pruebas:
``` 
> use pruebas
switched to db pruebas
```
Confirm that the session switched to the pruebas database:
```
> db
pruebas
```
Show the mongo help:
```
> help
 db.help()                    help on db methods
 db.mycoll.help()             help on collection methods
 sh.help()                    sharding helpers
 rs.help()                    replica set helpers
 help admin                   administrative help
 help connect                 connecting to a db help
 help keys                    key shortcuts
 help misc                    misc things to know
 help mr                      mapreduce

 show dbs                     show database names
 show collections             show collections in current database
 show users                   show users in current database
 show profile                 show most recent system.profile entries with time >= 1ms
 show logs                    show the accessible logger names
 show log [name]              prints out the last segment of log in memory, 'global' is default
 use <db_name>                set current database
 db.foo.find()                list objects in collection foo
 db.foo.find( { a : 1 } )     list objects in foo where a == 1
 it                           result of the last line evaluated; use to further iterate
 DBQuery.shellBatchSize = x   set default number of items to display on shell
 exit                         quit the mongo shell
```
Create 2 documents j and k using javascript syntax: 
```
> j = {name: 'mongo'}
{ "name" : "mongo" }
> k = {x:3}
{ "x" : 3 }
```
Insert the documents j and k into the testData collection:
```
> db.testData.insert( j )
> db.testData.insert( k )
```
Confirm that the testData collection exists:
```
> show collections
system.indexes
testData
```
Confirm that the documents exist in the testData collection:
```
> db.testData.find()
{ "_id" : ObjectId("5414fdec21061053051d13e8"), "name" : "mongo" }
{ "_id" : ObjectId("5414fdf721061053051d13e9"), "x" : 3 }

Imprimir el json de j y k:
> printjson(j)
{ "name" : "mongo" }
> printjson(k)
{ "x" : 3 }
```

In the next article I will explain how to work with mongo from python.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)