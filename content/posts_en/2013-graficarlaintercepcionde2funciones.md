Title: Plotting the intersection of 2 functions
Date: 2013-02-15 9:00
Category: Tutorial Python
Tags: General,numpy,Python
lang: en
translation: true

This article explains how to find the intersection of 2 functions, in this case a sine function with a cosine function.

The article is based on one in English called "[How to find the intersection of two functions](https://glowingpython.blogspot.com/2011/05/hot-to-find-intersection-of-two.html) ".

The plot will show the intersection of the functions sin(x) and cos(x) starting from an initial x value of zero. The fsolve function will be used, which returns the root of a (non-linear) equation defined by func(x) = 0.

The code is shown below:

```python
#!/usr/bin/env python

from scipy.optimize import fsolve

#Importar pylab

import pylab

#Importar numpy

import numpy

#Se define la funcion que calcula la intercepcion

#de 2 funciones.

def EncontrarIntercepcion(fun1,fun2,x0):
    #Se usa la función lambda de la diferencia de ambas funciones con

    #valor inicial x0
    return fsolve(lambda x : fun1(x) - fun2(x),x0)

if __name__ == '__main__':

    #se calcula el resultado de la intercepcion de 2 funciones

    #sin y cos con valor inicial de 0.

    resultado = EncontrarInterseccion(numpy.sin,numpy.cos,0.0)

    #se genera el rango de -2 a 2.

    x = numpy.linspace(-2,2,50)

    #Se genera la grafica, 

    pylab.plot(x,numpy.sin(x),x,numpy.cos(x),result,numpy.sin(result),'ro')

    #se muestra la grafica.

    pylab.show()
```

The plot is shown below:

![](./images/graficarlaintercepcionde2funciones.png) 

The sine function is in blue, the cosine plot is in green and the intersection is a red dot.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)