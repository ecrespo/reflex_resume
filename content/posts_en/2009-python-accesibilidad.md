Title: The python-autoaccesibilidad project has been created
Date: 2009-07-04 06:00
Category: Anuncio
Tags: Accesibilidad
lang: en
translation: true

The project page is at:

http://code.google.com/p/python-autoaccesibilidad/

Its description is on the wiki:

### Introduction

This program will allow the installation of accessible applications on computers
that already run Debian, without needing an internet connection or a mirror
on the network; it is useful for labs and internet centers.

For users there will be 2 Debian packages (the accesibilidad metapackage,
accesibilidad-gnome-conf-spanish and accesibilidad-gnome-conf-english) that
will make installing their machines easier.

### Details

The application will have the following features:

* Developed in python
* Modular
* It will use the python gksu module to install Debian packages, modify
sources.list and run a web server written in python.

* The configuration directories are added, along with a module to copy the configurations to all users.
* A small Debian repository is included, holding the accesibilidad metapackage and
the necessary dependencies, so no Debian mirror (a hard drive or an internet connection) is needed.

* For the moment it will only work with Debian Squeeze and Sid, since the accesibilidad metapackage
works for those two Debian versions (dependency problems and package availability
  in Lenny); a version for Lenny will come in the future.

* It will be possible to update the local package repository so that it does not depend
on package versions and the application does not have to change because of those changes.

The modules needed are:

* web.py : Starts a web server.
* su.py : Makes it easy to run commands as root by asking for the root password.
* users.py : Returns the users that exist on the computer.
* apt.py : Makes changes to the repository the machine uses and installs applications.
* autoaccesibilidad.py : Main program that installs accessible applications
on a machine using a mirror and a local web server.

It will contain 2 directories:

* conf: This directory holds all the Gnome Desktop session configuration,
the configuration of the orca screen reader and any other user session configuration.

* debian: This directory holds a local repository of the Debian packages that are required
for a computer to be accessible.

More information on the libre accesibilidad blog:

http://libreaccesibilidad.blogspot.com/2009/07/proyecto-python-autoaccesibilidad.html




===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)