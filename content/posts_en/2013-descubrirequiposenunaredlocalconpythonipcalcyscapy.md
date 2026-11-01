Title: Discovering hosts on a Local Network with Python (ipcalc and scapy).
Date: 2013-04-22 9:00
Category: Tutorial Python
Tags: Canaima,Debian,General,Linux,Python,scapy,ipcalc
lang: en
translation: true


If you have a network with open IP assignment, administration gets somewhat complicated, so you need to keep a record of the IP assignments to the machines on the local network.

An administrator friend made a record with a proprietary tool on Windows. I remembered the python library ipcalc, which makes calculating IP addresses and networks easier (an article on how to use it [here](https://scapy.readthedocs.io/en/latest/#about-scapy)).

There is also the scapy library or tool, which lets you capture and modify network packets (the documentation can be found at the following [link](https://scapy.readthedocs.io/en/latest/#about-scapy)).

An alternative is to use the ping and arp commands from python through the commands module; it is preferable to use scapy, which lets you discover the MAC address of the machines that have the IPs assigned.

So on one hand ipcalc is used to define the network range according to the mask, and then scapy discovers the MAC addresses.

Here is the code that returns the MAC address of each IP in use on the network:

```python

#!/usr/bin/env python

#Se importa los modulos necesarios.

from ipcalc import IP, Network

from scapy.all import srp,Ether,ARP,conf

#Se desactiva el verbose de la captura y envio de paquetes.

conf.verb=0

#Se genera un ciclo con el rango de IPs dando la RED y la mascara

for ip in Network('192.168.12.128/25'):

    #Se realiza un broadcast de MAC pasando cada IP el cual devuelve la 

    #direccion MAC de la IP consultada.

    ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=str(ip)),timeout=2)

    for snd,rcv in ans:

        #Se muestra en pantalla la direccion MAC y la direccion IP

        print rcv.sprintf(r"%Ether.src% y %ARP.psrc%")
```

When you run the program you get the following:

```python

ernesto@jewel:~/bin/python$ sudo ./descubrir.py

WARNING: No route found for IPv6 destination :: (no default route?)

00:26:35:c6:93:0d y 192.168.12.130

00:2e:0b:c5:70:3c y 192.168.12.132

00:2e:90:c2:ec:51 y 192.168.12.134

00:50:ca:c1:71:8a y 192.168.12.136

00:32:57:ce:81:e7 y 192.168.12.138

00:2e:90:c4:58:7c y 192.168.12.139

00:2c:25:ce:ae:be y 192.168.12.140

d0:37:88:c4:11:ed y 192.168.12.141

00:2e:90:cc:f5:16 y 192.168.12.142

00:2c:c4:c4:26:28 y 192.168.12.148

40:7a:ab:ce:11:c0 y 192.168.12.150

3c:53:8e:cc:4d:89 y 192.168.12.161

1c:5b:d6:c9:6d:a9 y 192.168.12.169

00:2e:7f:c4:8d:d7 y 192.168.12.170

00:24:c2:c8:23:8d y 192.168.12.172

68:19:ed:c75:44:31 y 192.168.12.174

74:3f:68:c2:91:d6 y 192.168.12.196

00:30:aa:c2:6d:3c y 192.168.12.201

c8:3c:dc:c8:a9:53 y 192.168.12.208

00:34:f2:c5:2f:21 y 192.168.12.211

00:34:f2:cc:2e:d0 y 192.168.12.212

00:34:f2:c5:35:70 y 192.168.12.214

00:34:f2:c3:1a:ee y 192.168.12.215

00:34:f2:c3:1b:4c y 192.168.12.216

00:34:f2:c5:33:49 y 192.168.12.224

00:3c:02:c6:b5:3f y 192.168.12.225

00:3e:90:c8:bb:d6 y 192.168.12.251
```


So from Linux and with Python you can capture the MAC address information of the assigned IPs with just a few lines of code.

##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)