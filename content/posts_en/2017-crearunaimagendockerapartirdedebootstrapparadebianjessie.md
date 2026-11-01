Title: Creating a Docker image from debootstrap for Debian Jessie
Date: 2017-03-27 09:00
Category: Tutorial de Linux
Tags: Linux,Debian,Ubuntu,Docker,debootstrap
lang: en
translation: true

Before getting into creating a Docker image from Debian's debootstrap, here is the link to the [docker articles on the blog](/blog/tags).

The first thing to do is install `debootstrap`:
```
#apt-get install debootstrap
```
Next, create a directory to build the `debootstrap` chroot:
```
mkdir debian-jaula
```
Now run `debootstrap`, passing the distribution to download, the directory where the chroot is created and the repository to use:
```
debootstrap jessie debian-jaula/ http://ftp.debian.org/debian
I: Retrieving Release 
I: Retrieving Release.gpg 
I: Checking Release signature
I: Valid Release signature (key id 75DDC3C4A499F1A18CB5F3C8CBF8D6FD518E17E1)
I: Validating Packages 
I: Resolving dependencies of required packages...
I: Resolving dependencies of base packages...
I: Found additional required dependencies: acl adduser dmsetup insserv libaudit-common libaudit1 libbz2-1.0 libcap2 libcap2-bin libcryptsetup4 libdb5.3 libdebconfclient0 libdevmapper1.02.1 libgcrypt20 libgpg-error0 libkmod2 libncursesw5 libprocps3 libsemanage-common libsemanage1 libslang2 libsystemd0 libudev1 libustr-1.0-1 procps systemd systemd-sysv udev 
I: Found additional base dependencies: libdns-export100 libffi6 libgmp10 libgnutls-deb0-28 libgnutls-openssl27 libhogweed2 libicu52 libidn11 libirs-export91 libisc-export95 libisccfg-export90 libmnl0 libnetfilter-acct1 libnettle4 libnfnetlink0 libp11-kit0 libpsl0 libtasn1-6 
I: Checking component main on http://ftp.debian.org/debian...
I: Validating acl 2.2.52-2
I: Retrieving libacl1 2.2.52-2
I: Validating libacl1 2.2.52-2
........................
..............
I: Configuring isc-dhcp-client...
I: Configuring tasksel...
I: Configuring tasksel-data...
I: Configuring libc-bin...
I: Configuring systemd...
I: Base system installed successfully.
```

Now the contents of the directory are shown:
```
ls debian-jaula/
bin/  boot/  dev/  etc/  home/  lib/  lib64/  media/  mnt/  opt/  proc/  root/  run/  sbin/  srv/  sys/  tmp/  usr/  var/
```
Now create the image using `tar` and `docker import`:
```
tar -C debian-jaula/ -c . | docker import - ecrespo/debian
sha256:49ad34e39c5f9ede2c1c57994895065236a5965496631e8fcab00b00778d85fa
```
As you can see, the image is generated along with its ID in sha256; the part that identifies the image is underlined, and the images are listed.

Running `docker images` gives the following:
```
REPOSITORY                                        TAG                 IMAGE ID            CREATED             SIZE
ecrespo/debian                                    latest              49ad34e39c5f        2 minutes ago       272.7 MB
```

With the chroot ready, you can make customizations and adaptations in order to create the docker image.

This article is based on the documentation in the [Debian wiki about debootstrap](http://wiki.debian.org/Debootstrap) and on an article about the [docker base image](http://docs.docker.com/engine/userguide/eng-image/baseimages/). 

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
