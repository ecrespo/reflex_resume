Title: Finding the minimum of a function using fmin from scipy
Date: 2013-02-18 9:00
Category: Tutorial Python
Tags: General,matplotlib,pylab,python
lang: en
translation: true

This article shows how to find the minimum value of a function with the fmin function from `scipy`.

The article is a Spanish version of the English article "[How to find the minimum of a function using fmin from scipy](https://glowingpython.blogspot.com/2011/04/how-to-find-minimum-of-function-using.html)".

The code is shown below:

```python
#!/usr/bin/env python

#Importar numpy,pylab y la función fmin de scipy.optimize.

import numpy

import pylab

from scipy.optimize import fmin

# Se define la funcion a partir de lambda.

rsinc = lambda x: -1 * numpy.sin(x)/x

#Se define un valor x0 de -5.

x0 = -5

#Se calcula el valor minimo de la funcion en el punto x0

xmin0 = fmin(rsinc,x0)

#Se define el punto x1 con valor -4

x1 = -4

#Se calcula el valor minimo de la funcion en el punto x1

xmin1 = fmin(rsinc,x1)

# se grafica la funcion.

x = numpy.linspace(-15,15,100)

y = rsinc(x)

pylab.plot(x,y)

#Se define el punto x0 en la grafica de la funcion

pylab.plot(x0,rsinc(x0),'bd',xmin0,rsinc(xmin0),'bo')

#Se define el punto x1 en la grafica de la funcion

pylab.plot(x1,rsinc(x1),'rd',xmin1,rsinc(xmin1),'ro')

pylab.axis([-15,15,-1.3,0.3])

pylab.show()
```


The figure below shows the plot of the function:

![](./images/encontrarelminimodeunafuncionusandofmindescipy.png) 

The blue dot is the minimum found starting from the blue diamond (x= -5), and the red dot is the minimum found starting from the red diamond. This point is the global minimum found for the function.

In addition to the plot, the fmin function generates the following output:

```
Optimization terminated successfully.
         Current function value: -0.128375
         Iterations: 18
         Function evaluations: 36
Optimization terminated successfully.
         Current function value: -1.000000
         Iterations: 19
         Function evaluations: 38
```

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)