Title: Solving systems of equations with Sympy  
Date: 2015-02-21 11:00  
Category: Tutorial Python  
Tags: Canaima,Debian,General,Python,Ubuntu,Sympy
lang: en
translation: true  

So far there are the following articles on using the `Sympy` library:

* [Computing limits with the Sympy library](/blog/calculodelimitesconlalibreriasympy)

* [Computing derivatives with the Sympy library](/blog/calculodederivadasconsympy)

* [Computing integrals with the Sympy library](/blog/calculodeintegralesconsympy)


This time I will explain how to use the `Sympy` library to solve systems of equations, using the example from a previous article ([Solving systems of linear equations by QR decomposition using Numpy](/blog/resoluciondesistemasdeecuacioneslinealespordescomposionqrusandonumpy)).

Start ipython notebook (if you want to use the file you can download it from the following [link (broken link)](https://bitbucket.org/ecrespo/ernesto-ecrespo.blogspot/src/d1791a6a85834e57c86721f892a3ad22dce6644f/sistecuaciones/sisteecuaciones.ipynb?at=default)):

The script code is shown below:

```python
#!/usr/bin/env python


#Se importa sympy


from sympy import *


#Se define las variables simbolicas x,y,z


x = Symbol('x')


y = Symbol('y')


z= Symbol('z')


#Resolver el sistema de ecuaciones


#3x+9y-10z  =   24


#x-6y+4z      =   -4


#10x-2y+8z  =  20


resultado =solve([3*x+9*y-10*z-24,x-6*y+4*z+4,10*x-2*y+8*z-20],[x,y,z])


print resultado
```

Running the script gives the following:
```
{x: 308/103, z: -117/103, y: 42/103}
```

Note that the result obtained is the same as in the article [mentioned](/blog/resoluciondesistemasdeecuacioneslinealespordescomposionqrusandonumpy) above.


The image of using the notebook is shown below:

![](./images/resoluciondesistemasdeecuacionesconsympy-1.png)

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
