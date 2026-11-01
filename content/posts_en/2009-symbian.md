Title: Symbian operating system for cell phones
Date: 2009-05-10 08:00
Category: Sistemas Operativos
Tags: Symbian
lang: en
translation: true

### SymbianOS

It is an open operating system designed for mobile devices, with libraries,
a user interface framework and tools developed by Symbian Ltd, running
exclusively on ARM processors.

### Design

Its structure is similar to many desktop operating systems, with preemptive
multitasking and memory protection. EPOC was inspired by the way OpenVMS handles multiple tasks.

SymbianOS was built keeping 3 rules in mind: the integrity and security of the
user's data is paramount, the user's time must not be wasted, and all resources
are scarce. All the applications and the operating system were developed with
object-oriented programming following the MVC paradigm.

### Structure

The Symbian operating system model contains the following layers from top
to bottom:

* User Interface framework layer
* Application services layer
* Java ME
* Operating system services layer
* Generic operating system services
* Communication services
* Multimedia and graphics services
* Connectivity services
* Base services layer
* Hardware Interface and kernel services layer

The Base services are at the lowest level with respect to user
operations; they include the file server and user libraries, the plugin framework
that manages all the plugins, the central repository, the database manager
and encryption services.

The Symbian operating system has a microkernel architecture, which means
that it uses the bare minimum inside the kernel, achieving robustness and availability. The kernel
contains a scheduler, memory management, and device drivers, but
other services such as networking, telephony, or file system support are located
in the operating system services layer or the base services layer. The inclusion
of the device drivers means that the kernel is not a true microkernel.

The Symbian operating system was designed with compatibility with other
devices in mind, especially devices that handle removable file systems;
in its early days EPOC adopted the FAT file system as its internal file system.

There is a large number of networking and communications subsystems, which has 3 main
servers: ETEL (EPOC Telephony), ESOCK (EPOC Sockets) and C32 (responsible for
  serial communication); each of these has a plugin scheme. The subsystem
  also contains code that belongs to a short range of communications such as
  Bluetooth, IrDA and USB.



Free Software for Symbian 9.1

* Utilities
* Putty: ssh and telnet client
* Internet radio
* SymTorrent: torrent client
* Symella: gnutella client
* Python interpreter: this gives us the chance to develop applications for Symbian with python in addition to Java.
* Apache web server
* Game emulation
* ScummVM
* Multimedia
* Oggplay
* Symbian announces PIPS (Posix on Symbian), which will increase the number of free software applications written for Symbian

===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)