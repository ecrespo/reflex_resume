Title: Querying DNS with Scapy
Date: 2017-07-16 09:00
Category: Tutorial Python
Tags: General,Debian,Python,DNS
lang: en
translation: true
 
A few years ago I wrote an article on [discovering machines on a local network with python using ipcalc and scapy (broken link)](/blog/descubrirequiposenunaredlocalconpythonipcalcyscapy); now I show how to use scapy to query a given DNS server.



The program is very simple: it is a function that is passed the server and the url to query and returns the IP of the url. The code is shown below:

```python

#!/usr/bin/env python3


from scapy.all import *


def consulta(dns="8.8.8.8",dominio="www.google.com"):
    dnsServer = dns
    domconsulta= dominio
    #Se define la estructura del paquete de consulta de DNS, que es un paquete UDP
    #Que va por el puerto 53, se le pasa el servidor y el url.
    paquete_dns= IP(dst=dnsServer)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=domconsulta))
    #Se hace la consulta y se devuelve el resultado
    request_pqt = sr1(paquete_dns,verbose=0)
    return request_pqt[DNS].summary()
    
if __name__ == "__main__":
    print (consulta("8.8.8.8","www.debian.org"))
```

Running the script gives the following result:
```python
sudo python3 pydns1.py
WARNING: No route found for IPv6 destination :: (no default route?). This affects only IPv6
DNS Ans "'128.31.0.62'"
```

As you can see, the IP of www.debian.org is 128.31.0.62.




##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
