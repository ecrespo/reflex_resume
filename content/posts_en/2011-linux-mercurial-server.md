Title: Sharing Mercurial repositories with mercurial-server
Date: 2011-08-20 09:00
Category: Tutorial de Linux
Tags: Linux,Debian, Ubuntu, Canaima,mercurial
lang: en
translation: true

There are several articles about mercurial on this blog: a [mercurial tutorial](/blog/cvmercurial) (an update is coming), [how to package for Debian with mercurial](/blog/paquetedebianconmercurial) (an update is coming) and the latest one, [how to manage configuration with mercurial](/blog/linux-etckeeper).

This article explains how to share Mercurial repositories with mercurial-server; it is based on the [tutorial in English (broken link)](http://dev.lshift.net/paul/mercurial-server/docbook.html).

Mercurial-server does not authenticate using passwords but rather ssh public keys. All users who want to access the mercurial repository need a public key. 

At the following link you have a guide on how to create [public keys](http://rafael.bonifaz.ec/blog/2011/01/ssh-con-claves-publicas-y-privadas/).

### Initial access to mercurial-server.

Install mercurial-server:

```
aptitude install mercurial-server 
```

Connect to the grievous server with forwarding enabled.

```
ernesto@jewel:~$ ssh -A grievous
```

Add the private key to the authentication agent. 

```
ernesto@grievous:~$ ssh-add -L > my-key
```

Create the directory for the user ernesto in mercurial-server, copy the key and update the authentication repository. 

```
ernesto@grievous:~$ sudo mkdir -p /etc/mercurial-server/keys/root/ernesto
ernesto@grievous:~$ sudo cp my-key /etc/mercurial-server/keys/root/ernesto/jewel
ernesto@grievous:~$ sudo -u hg /usr/share/mercurial-server/refresh-auth
ernesto@grievous:~$ exit
```

Create a repository.

```
 cd proyectos/pysms-send
```

Clone the project on the grievous server: 

```
ernesto@jewel:~/proyectos/pysms-send$ hg clone . ssh://hg@grievous/ernesto/pysms-send
searching for changes
27 changesets found
remote: adding changesets
remote: adding manifests
remote: adding file changes
remote: added 27 changesets with 52 changes to 24 files
```

Check whether there are changes in the repository.

```
ernesto@jewel:~/proyectos/pysms-send$ hg pull ssh://hg@grievous/ernesto/pysms-send
pulling from ssh://hg@grievous/ernesto/pysms-send
searching for changes
no changes found
```

The next article will explain how to add users to the repository and control access to it.





===

Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
