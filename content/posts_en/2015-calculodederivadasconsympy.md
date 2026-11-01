Title:Calculating derivatives with sympy
Date: 2015-02-21 09:00  
Category: Tutorial Python  
Tags: Canaima,Debian,General,Python,Ubuntu  
lang: en
translation: true  


The [previous article](/blog/calculodelimitesconlalibreriasympy) explained how to calculate limits of functions; this article shows how to calculate the derivative.


Start notebook (if you want to open the file used for this article, you can find it at the following [link (broken link)](https://bitbucket.org/ecrespo/ernesto-ecrespo.blogspot/src/286db40e8218d4d39863751a4bc850672bd93592/derivadas/derivadas.ipynb?at=default)):
```python
$ipython notebook
```
You can create a notebook (or open the notebook mentioned in the previous link).

Below is the script that calculates the derivatives of 3 different functions:
```python
#!/usr/bin/env python

# coding: utf-8


#Se importa sympy

from sympy import *


x = Symbol('x')



#Se calcula la derivada de la funcion cos(sin(x^3)) con respecto a x

print diff(cos(sin(x**3)),x)



#Se calcula la derivada de la funcion 5(x^5)+3(x^3)-6x+5

print diff(5*(x**5)+3*(x**3)-6*x+5,x)



#Calcula la derivada ene-sima de x^2+8x-4+sin(2x)

print diff(x**2+8*x-4+sin(2*x),x,2)

```

Running the script shows the result of executing the 3 print statements:
```
-3*x**2*sin(sin(x**3))*cos(x**3)
25*x**4 + 9*x**2 - 6
2*(-2*sin(2*x) + 1)
x,2)
```
Running the script shows the result of executing the 3 print statements:
```
-3*x**2*sin(sin(x**3))*cos(x**3)
25*x**4 + 9*x**2 - 6
2*(-2*sin(2*x) + 1)
```

Below is an image of the resulting notebook:

![](./images/calculodederivadasconsympy-1.png)


Below is an image of the resulting notebook:

![](./images/calculodederivadasconsympy-2.png)


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
