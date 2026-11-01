Title: Geolocating IP addresses and Internet domains with GeoIP in python
Date: 2012-02-26 09:00
Category: Tutorial de Python  
Tags: Canaima,Debian,Linux,Python,Redes,Ubuntu
lang: en
translation: true

Worldwide, several groups of IPv4 addresses (Classes A, B or C) were created, which make it possible to define networks and ranges of machines for those networks.

Of course, there is currently a migration to IPv6 since IPv4 addresses ran out a couple of years ago, roughly (although there are solutions such as NAT, Subnetting or Supernetting that allow IPs to be used more efficiently).

With GeoIP for python you can find out which Country an IP comes from, find out where a specific domain or site is hosted, and learn the IP range of an IPv4 class.

To install `python-geoip` the Debian way (Debian, Canaima, Ubuntu, LinuxMint), become superuser and run:  

```
#apt-get install python-geoip
```

Run the python command interpreter:  
```
ecrespo@jewel:~$ python
Python 2.7.2+ (default, Dec  1 2011, 01:55:02)
[GCC 4.6.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```	
Import the `geoip` module:  
```python 
>>> import GeoIP
```
Create the GeoIP instance object, associating it with the GeoIP information in the memory cache:  
```python 
>>> gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
```
Look up in which Country yahoo.com is hosted:  
```python 
>>> print gi.country_code_by_name("yahoo.com")
US
>>> print gi.country_name_by_name("yahoo.com")
United States
```
In the first case the Country code is returned, in the second the Country name is returned.

Now let's try yahoo.es:  
```python 
>>> print gi.country_code_by_name("www.yahoo.es")
IE
>>> print gi.country_name_by_name("www.yahoo.es")
Ireland
```
Note that yahoo.com is hosted in the United States and yahoo.es is hosted in Ireland.

Now let's look up in which Country www.cantv.net is hosted (obviously):  
```python 
>>> print gi.country_code_by_name("www.cantv.net")
VE
>>> print gi.country_name_by_name("www.cantv.net")
Venezuela
```
Although it is possible for Venezuelan domains to be hosted in other Countries, an example would be www.crespo.org.ve:  
```python 
>>> print gi.country_name_by_name("www.crespo.org.ve")
Sweden
```
Finally, let's try finding the Country according to the IP passed in:  
```python 
>>> print gi.country_name_by_addr("24.24.24.24")
United States
>>> print gi.country_name_by_addr("150.186.32.0")
Venezuela
```
The first IP is in the United States and the second in Venezuela.

To find the IP range of the Venezuelan IP, run `geoip` asking it to return the IP range:  
```python 
>>> print gi.range_by_ip("150.186.32.0")
('150.185.0.0', '150.189.255.255'
```
Given the range of addresses it covers, this IP is a class B.

This tool can be used for Web applications with Django, for example, and such applications can show information about the Country from which users connect.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)

