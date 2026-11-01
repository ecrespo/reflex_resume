Title: Getting network interface information with python (netifaces)
Date: 2012-02-07 09:00
Category: Tutorial de Python  
Tags: Canaima,Debian,General,Python,Redes,Ubuntu
lang: en
translation: true

There is a python module that lets you get information about network interfaces.

The module is called `netifaces`; with it you can get the list of interfaces on your machine, the Network Link information of each interface, its IPv4 address and its IPv6 address.

To install the module, run `apt-get` on Debian/Canaima/Ubuntu.  

```
#apt-get install python-netifaces
```

The idea is to create a script that gets the list of interfaces on the machine and shows the information of each one of them.

The program code is shown below:  

```python 
#!/usr/bin/env python

#Se importa el modulo netifaces
import netifaces

#Se captura la lista de interfaces en el equipo
interfaces = netifaces.interfaces()
#Se muestra las interfaces
print "interfaces: ", interfaces

#Se recorre la lista de interfaces
for interface in interfaces:
#Se captura la informacion de cada interfaz
datos = netifaces.ifaddresses(interface)
print "--------------------------"
#Se muestra el nombre de la interface
print "Interface: %s" %interface
#Se captura la lista de parametros que tiene la interface
variables = datos.keys()
#Se muestra la direccion de la capa de enlace de red de la interface
print "Capa de enlace de red: ", datos[netifaces.AF_LINK][0]['addr']
#Si esta presente la informacion de IPV4 se muestra
if netifaces.AF_INET in variables:
print "IPv4: IP: %s, Mascara: %s" %(datos[netifaces.AF_INET][0]['addr'], datos[netifaces.AF_INET][0]['netmask'])
#Si esta presente la informacion de IPv6 se muestra
if netifaces.AF_INET in variables:
print "IPv6: IP: %s, Mascara: %s " %(datos[netifaces.AF_INET6][0]	['addr'], datos[netifaces.AF_INET6][0]['netmask'])
```
The program's output is shown below:
```python 
interfaces: ['lo', 'eth0', 'wlan0']
--------------------------
Interface: lo
Capa de enlace de red: 00:00:00:00:00:00
IPv4: IP: 127.0.0.1, Mascara: 255.0.0.0
IPv6: IP: ::1, Mascara: ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
--------------------------
Interface: eth0
Capa de enlace de red: 71:6a:b7:77:46:5f
--------------------------
Interface: wlan0
Capa de enlace de red: 00:26:85:74:fe:89
IPv4: IP: 192.168.10.108, Mascara: 255.255.255.0
IPv6: IP: fe80::236:92ff:fa54:fe89%wlan0, Mascara: ffff:ffff:ffff:ffff::
```
For more information about the module you can visit the information on the [Python](https://pypi.org/project/netifaces/) page or the [application](https://alastairs-place.net/projects/netifaces/) site. 


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)