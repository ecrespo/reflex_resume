Title:  Encrypting DNS traffic on Linux with DNSCrypt and OpenDNS
Date: 2012-02-20 09:00
Category: Tutorial de Python
Tags: Canaima,Debian,DNS,gnome,Linux,Redes,Seguridad,Ubuntu
lang: en
translation: true

`DNSCrypt` lets you encrypt DNS queries between the computer and the OpenDNS DNS servers, which protects the machine from Man-in-the-Middle attacks.

The article this tutorial is based on is at the following [link](http://www.webupd8.org/2014/08/encrypt-dns-traffic-in-ubuntu-with.html).
To install `dnscrypt` on Debian, download the package from the [Github (broken link)](https://github.com/opendns/dnscrypt-proxy/downloads) repository.

Run `dpkg`:

```
#dpkg -i dnscrypt-proxy_0.9_i386.deb
```

Start the dns proxy as a daemon:  

```
#dnscrypt-proxy --daemonize
```

Edit the wireless connections; in this case the network the computer connects to is wireless:

![](./images/cifrareltraficodednsenlinuxcondnscryptyopendns-1.png) 


Select the wireless network and edit its settings:

![](./images/cifrareltraficodednsenlinuxcondnscryptyopendns-2.png) 

Select the IPv4 Settings tab, in the method select Automatic (DHCP) addresses only, and enter the IP 127.0.0.1 in DNS servers:

![](./images/cifrareltraficodednsenlinuxcondnscryptyopendns-3.png) 

To verify that the `OpenDNS` DNS servers are being used, open the browser at the URL http://www.opendns.com/welcome :  

![](./images/cifrareltraficodednsenlinuxcondnscryptyopendns-4.png) 


The communication with the `OpenDNS` servers is now encrypted.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
