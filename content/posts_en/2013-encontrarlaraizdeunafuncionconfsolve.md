Title: Finding the root of a function with fsolve
Date: 2013-02-14 10:00
Category: Tutorial Python
Tags: Canaima,Debian, General,Linux,matplotlib,numpy,Python,Ubuntu
lang: en
translation: true

This article explains how to calculate the root of a function using the `fsolve` function.

The article is based on an English article "[How to find the rooots of a function with fsolve](https://glowingpython.blogspot.com/2011/05/how-to-find-roots-of-function-with.html)".

The fsolve function returns the roots of a nonlinear equation defined by `f(x) = 0`.
In this case we will calculate the root of the function `f(x) = x^3`.

Here is the code:

```python
#Import fsolve para calcular la raiz de la funcion x^3

from scipy.optimize import fsolve

#Importar pylab

import pylab

#importar numpy

import numpy

#se calcula la potencia 3 de x con la funcion lambda

potencia3 = lambda x : x**3

#Se calcula la raiz de x^3 iniciando con x = 10

resultado = fsolve(potencia3,10) # starting from x = 10

print resultado

#Se define 400 valores de x entre -4 a 4

x = numpy.linspace(-4,4,400)

#Se genera la grafica, pasando el valor de x

#la potencia 3era de x, el valor de resultado, la potencia 3era de resultado

pylab.plot(x,potencia3(x),resultado,potencia3(resultado),'ro')

#Se define el grid

pylab.grid(b=1)

#Se muestra la grafica

pylab.show()
```
The plot shows the point where the root of the function is found:

![](./images/encontrarlaraizdeunafuncionconfsolve.png) 

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)