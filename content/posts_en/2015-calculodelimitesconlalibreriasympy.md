Title: Calculating limits with the sympy library  
Date: 2015-02-21 08:00  
Category: Tutorial Python  
Tags: Canaima,Debian,General,Python,Ubuntu,Sympy
lang: en  
translation: true  

The [Sympy (broken link)](https://www.sympy.org/en/index.html$) library lets you calculate limits, derivatives, integrals and more, using symbolic notation.

You can review the sympy documentation at the following [link](https://docs.sympy.org/latest/index.html).

To install `sympy` and `ipython-notebook` on Debian, run:
```
apt-get install python-sympy ipython-notebook
```
In this case I will show how to calculate limits with `sympy`.

Run a notebook server (at the following [link (broken link)](https://bitbucket.org/ecrespo/ernesto-ecrespo.blogspot/src/c7ba713cb44687395f99860ebb5d2cb049173834/limites/limites.ipynb?at=default) you will find the file used for this article).
```
$ipython notebook
```
Open the browser at http://localhost:8888 and create a notebook (if you downloaded the file from the link, open the file mentioned above):

In this case a script called `limites.py` will be used:
```python
#!/usr/bin/env python

# coding: utf-8

from sympy import *

#Se define la variable x como simbolica

x = Symbol("x")

#Calculo de limite de (1/x) cuando x tiende a cero

valor = limit(1/x,x,0)

print valor

#Calculo de limite de (1/x) cuando x tiende a infinito

valor = limit(1/x,x,oo)

print valor

#limite de (5x/2x-3) cuando x tiende a infinito.

valor = limit(5*x/(2*x-3),x,oo)

print valor

```


The result of running it is the following:

```
oo


0


5/2
```



In the first case the result is infinity, in the second it is zero, and in the last one it is 2.5.

Below is an image of ipython notebook in use:


![](./images/calculodelimitesconlalibreriasympy-1.png)


##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
