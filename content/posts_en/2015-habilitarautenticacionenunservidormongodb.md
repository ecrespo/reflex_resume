Title: Enabling authentication on a mongodb server
Date: 2015-05-08 9:00
Category: Tutorial Linux
Tags: Canaima,Debian,General,Linux,Ubuntu,Mongodb
lang: en
translation: true

The article about installing a [mongodb server](/blog/instalarunservidormongodbendebian) missed defining the authentication of the users who can connect to that server.

In this case, authentication will be enabled for access to the server.

The first step is to disable authentication in the `/etc/mongodb.conf` file:
```
# Turn on/off security.  Off is currently the default
#noauth = true
#auth = true
```
Start the `mongodb` service:
```
 systemctl start  mongodb.service
```
Check whether it came up:
```
systemctl status  mongodb.service
● mongodb.service - An object/document-oriented database
   Loaded: loaded (/lib/systemd/system/mongodb.service; enabled)
   Active: active (running) since vie 2015-05-08 11:44:26 VET; 5s ago
     Docs: man:mongod(1)
 Main PID: 3405 (mongod)
   CGroup: /system.slice/mongodb.service
           └─3405 /usr/bin/mongod --config /etc/mongodb.conf

may 08 11:44:26 grievous mongod[3405]: all output going to: /var/log/mongodb/mongodb.log
```
Access the `mongodb` shell:
```
mongo
MongoDB shell version: 2.4.10
connecting to: test
>
```

Switch to the `admin` database:
```
> use admin
switched to db admin
```
Create the admin user with password 123456 (for teaching purposes only) and the read/write and dbAdmin roles.

```
> db.addUser("admin","123")
{
 "user" : "admin",
 "readOnly" : false,
 "pwd" : "9f3121efccbe3fef09a799d5e63077c2",
 "_id" : ObjectId("554cf1405cf1b965e6f5c10f")
}
```

Exit the database:
```
> exit
bye
```

Now edit the `/etc/mongodb.conf`  file to enable authentication:
```
# Turn on/off security.  Off is currently the default
#noauth = true
auth = true
```
Restart `mongodb`:
```
systemctl stop  mongodb.service
systemctl stop  mongodb.service
systemctl status   mongodb.service
● mongodb.service - An object/document-oriented database
   Loaded: loaded (/lib/systemd/system/mongodb.service; enabled)
   Active: active (running) since vie 2015-05-08 11:58:44 VET; 4s ago
     Docs: man:mongod(1)
 Main PID: 4188 (mongod)
   CGroup: /system.slice/mongodb.service
           └─4188 /usr/bin/mongod --config /etc/mongodb.conf

may 08 11:58:44 grievous mongod[4188]: all output going to: /var/log/mongodb/mongodb.log
```
Run the `mongodb` shell and try to list the databases:
```
> show dbs
Fri May  8 12:06:19.122 listDatabases failed:{ "ok" : 0, "errmsg" : "unauthorized" } at src/mongo/shell/mongo.js:46
```
Note that you are not authorized to see the list of databases.

To log in and authenticate the user, do the following:
```
> use admin
switched to db admin
> db.auth("admin", "123")
1
```
List databases:
```
> show dbs
admin 0.203125GB
local 0.078125GB
personasdb 0.203125GB
```
List users:  
```
> db.system.users.find()
{ "_id" : ObjectId("554ce337c597c2dbd0089d74"), "user" : "admin", "pwd" : "95ec4261124ba5951720b199908d892b", "roles" : [  "readWrite",  "dbAdmin" ] }  
```


For more information, see the following links:

1. [https://dezkareid.wordpress.com/2013/07/29/control-de-usuarios-en-mongodb/](/blog/instalarunservidormongodbendebian)
2. [https://carlosazaustre.es/blog/como-conectarte-remotamente-a-tu-base-de-datos-mongodb/ (broken link)](https://carlosazaustre.es/blog/como-conectarte-remotamente-a-tu-base-de-datos-mongodb/)
3. [http://docs.mongodb.org/v2.4/tutorial/add-user-to-database/](http://docs.mongodb.org/v2.4/tutorial/add-user-to-database/)
4. [http://juanvicenteherrera.es/2011/12/20/mongodb-conceptos-de-seguridad/](http://juanvicenteherrera.es/2011/12/20/mongodb-conceptos-de-seguridad/)
5. [https://alexanderae.com/mongodb-autenticacion-autorizacion.html](https://alexanderae.com/mongodb-autenticacion-autorizacion.html)



##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)