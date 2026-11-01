Title: Solving systems of linear equations by QR decomposition using Numpy
Date: 2013-02-21 9:00
Category: Tutorial Python
Tags: General,numpy,Python
lang: en
translation: true

In December an [article](/blog/resoluciondesistemasdeecuacionesconnumpy) was published explaining how to solve systems of equations.

This article is based on the English article [QR descomposition with numpy ](https://glowingpython.blogspot.com/2011/05/qr-decomposition-with-numpy.html).

If you want to find out more about QR decomposition you can check the [wikipedia](https://es.wikipedia.org/wiki/Descomposici%C3%B3n_QR) page or the following [page](https://rkb.home.cern.ch/rkb/AN16pp/node224.html#SECTION0002240000000000000000).

The equations used are:
```
3x+9y-10z  =   24
x-6y+4z      =   -4
10x-2y+8z  =  20
```
Where `Ax = b.`
```
A = [[3 9 -10][1 -6 4][10 -2 8]] y
B  = [[24][-4[[20]]
```

The code is shown below:
```python
#!/usr/bin/env python

# -*- coding: utf-8 -*-

from numpy import *


#Se define los valores de la matriz A
A = array([[3,9,-10],[1,-6,4],[10,-2,8]])

Q,R = linalg.qr(A) # qr decomposition of A

#Se definen los valores de la matriz B
b = array([[24],[-4],[20]])


#resolver Ax=b usando la funcion estandar numpy
x = linalg.solve(A,b)


#resolver Ax = b usando Q y R.
y = dot(Q.T,b)
xQR = linalg.solve(R,y) 

print "\nComparacion de Soluciones:"
print x.T,'Ax=b'
print xQR.T,'Rx=y'
```
When you run the script you get the following:

```python
python qr.py 
``` 


Comparison of Solutions:
```python
[[ 2.99029126  0.40776699 -1.13592233]] Ax=b

[[ 2.99029126  0.40776699 -1.13592233]] Rx=y
```

As you can see, the solution using the standard numpy function and the one using QR decomposition produce the same result.

##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)