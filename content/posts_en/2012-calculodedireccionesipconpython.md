Title: IP address calculation with Python
Date: 2012-03-04 09:00
Category: Tutorial de Python
Tags: Canaima,Debian,General,Python,Seguridad,Ubuntu
lang: en
translation: true

I remember that when I took the computer networks course, you had to calculate network segments, do `subnetting`, `supernetting`, `NAT`, etc., and all the calculations had to be done with pencil and paper, converting IP addresses into 4 bytes separated by dots; even in the graduate classes the use of IP calculators was not allowed.

For Python there is a library that lets you do the calculations to define a network, a network segment, or recognize when an IP belongs to a given network segment.

The library is called `ipcalc`; you can see the description and an example at the following [link](https://pypi.python.org/pypi/ipcalc/).

To install it from the Python package index you can use `pip` or `easy_install`:  

```python 
#pip install ipcalc
```  

Or  

```python 
#easy_install ipcalc
```

On Debian, run `apt-get`:  

```
#apt-get install python-ipcalc
```

Run python from the console:  
```
ecrespo@jewel:~$ python
Python 2.7.2+ (default, Dec  1 2011, 01:55:02)
[GCC 4.6.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
```	
Import IP and Network from `ipcalc`:  

```python 
>>> from ipcalc import IP, Network
```

This shows the IP segment of network 192.168.10.0 with 30 bits set to 1 in the mask (mask 255.255.255.252):  

```python 
>>> for x in Network('192.168.10.0/30'): print str(x)
...
192.168.10.0
192.168.10.1
192.168.10.2
192.168.10.3
```
	
As you can see, there are 4 IP addresses, of which the first (192.168.10.0) is the subnet address and the last (192.168.10.3) is the broadcast address of that subnet.

If the mask bits are changed to 29, the range of IPs of that subnet grows from 4 to 8 IPs:  

```python 
>>> for x in Network('192.168.10.0/29'): print str(x)
...
192.168.10.0
192.168.10.1
192.168.10.2
192.168.10.3
192.168.10.4
192.168.10.5
192.168.10.6
192.168.10.7
```
	
You can also check whether a given IP is in a network segment or subnet. As an example, we will check whether IP 192.168.10.8 is in subnet 192.168.10.0/29 (obviously not):  

```python 
>>> '192.168.10.8' in Network('192.168.10.0/29')
False
```
	
If you try IP 192.168.10.1, the query returns True:  

```python 
>>> '192.168.10.1' in Network('192.168.10.0/29')
True
```

The last example is the case of a network 192.68.10.0/22 or 192.168.10.0/255.255.252.0, where we want to find out the first IP and the last IP of that network segment:  

```python 
>>> '192.168.9.1' in Network('192.168.10.0/22')
False
>>> '192.168.9.255' in Network('192.168.10.0/22')
False
>>> '192.168.10.0' in Network('192.168.10.0/22')
True
>>> '192.168.10.1' in Network('192.168.10.0/22')
True
>>> '192.168.11.1' in Network('192.168.10.0/22')
True
>>> '192.168.12.1' in Network('192.168.10.0/22')
True
>>> '192.168.13.1' in Network('192.168.10.0/22')
True
>>> '192.168.14.1' in Network('192.168.10.0/22')
False
>>> '192.168.13.255' in Network('192.168.10.0/22')
True
```
	
From this result, the first IP is 192.168.10.0 and the last is 192.168.13.255.

It can also be used to calculate IPv6 addresses.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)