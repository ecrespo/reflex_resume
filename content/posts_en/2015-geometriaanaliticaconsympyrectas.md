Title: Analytic Geometry with Sympy (lines)  
Date: 2015-02-23 11:20  
Category: Tutorial Python  
Tags: Canaima,Debian,General,Python,Ubuntu,Sympy
lang: en
translation: true  

Continuing with Sympy's analytic geometry, this time the handling of lines is explained.

A summary of the previous articles:

* [Calculating limits with Sympy](/blog/calculodelimitesconlalibreriasympy)

* [Calculating derivatives with Sympy](/blog/calculodederivadasconsympy)

* [Calculating integrals with Sympy](/blog/calculodeintegralesconsympy)

* [Solving systems of linear equations with Sympy](/blog/resoluciondesistemasdeecuacionesconsympy)

* [Analytic geometry with Sympy (segments)](/blog/geometriaanaliticaconsympysegmentos)

At the following [link (broken link)](https://bitbucket.org/ecrespo/ernesto-ecrespo.blogspot/src/c645a908ed04a4cf0178f41df93fe1d9c871eee8/geometriaanalitica/geometria-lineas.ipynb?at=default) you will find the notebook file with the code that is explained next.

The code of the line-handling script is shown below.
```python
#!/usr/bin/env python

from sympy.geometry import *



#Creacion de 4 puntos

P1 = Point(0, 0)

P2 = Point(3, 4)

P3 = Point(2, -1)

P4 = Point(-1, 5)



#Creacion de 2 segmentos

S1 = Segment(P1, P2);#segmento 1 a partir de los puntos 1 y 2

S2 = Segment(P3, P4);#Segmento 2 a partir de los puntos 3 y 4



#Se crea 2 rectas

#A partir de los puntos 1 y 2

L1 = Line(P1, P2)

#Se crea la recta 2 que ser perpendicular a la recta 1 y contenga al punto 3

L2 = L1.perpendicular_line(P3)





#Manejo de rectas



print L2.arbitrary_point();#Punto arbitrario de la recta 2 (ecuacion parametrica)

print L2.equation() ;#ecuacion de la recta 2

print L2.contains(P4);#Linea 2 contiene al punto 4?

print L2.distance(P4);#distancia del punto 4 a la recta 2?

print L1.is_parallel(S2);#La recta 1 es paralela al segmento 2?
```
The result of running the script follows:  
```
Point(4*t + 2, -3*t - 1)

3*x + 4*y - 2

False

3

False
```

An image of the notebook execution for this article is shown below:

![](./images/geometriaanaliticaconsympyrectas-1.png)

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
