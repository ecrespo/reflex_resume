Title: Analytic Geometry with Sympy (circles)
Date: 2015-03-02 9:00
Category: Tutorial Python
Tags: Canaima,Debian,General,Python,Ubuntu,Sympy
lang: en
translation: true


Below are the articles about sympy covered previously:

* [Computing limits with sympy](/blog/calculodelimitesconlalibreriasympy)
* [Computing derivatives with sympy](/blog/calculodederivadasconsympy)
* [Computing integrals with sympy](/blog/calculodeintegralesconsympy)
* [Solving systems of linear equations with sympy](/blog/resoluciondesistemasdeecuacionesconsympy)
* [Analytic Geometry with sympy (segments)](/blog/geometriaanaliticaconsympysegmentos)
* [Analytic Geometry with sympy (lines)](/blog/geometriaanaliticaconsympyrectas)  

This article explains the analytic geometry instructions for the case of the circle.

Below is the script code:

```python


#!/usr/bin/env python

from sympy.geometry import *; #Se importa geometry de sympy

#SE crean los puntos P1,P2,P3 y P4


P1 = Point(0, 0)


P2 = Point(3, 4)


P3 = Point(2, -1)


P4 = Point(-1, 5)

L1 = Line(P1, P2); #linea 1 a partir de los puntos 1 y 2



L2 = L1.perpendicular_line(P3);#linea 2 perpendicular a la linea 1 y contenga al punto 3.



C1 = Circle(P1, 3);#se crea un circulo con centro en P1 y radio 3.



C2 = Circle(P2, P3, P4); #Se crea un circulo que contenta los puntos P1,P2 y P3



print (C2.area); #Area del circulo 2



print (C1.area);#Area del circulo 1



print (C2.radius); #Radio del circulo 2



print (C2.equation());#Ecuacion del circulo 2



print (C2.center);#Centro del circulo 2



print (C2.circumference);#Circunferencia del circulo 2



print (C2.intersection(C1)); #Intercepcion entre el circulo 2 y circulo 1



S1 = Segment(P1, P2);#segmento 1 a partir de los puntos 1 y 2



print (C2.intersection(S1));#Intercepcion entre el circulo 2 y el segmento 1



print (C2.is_tangent(L2));#La recta 2 es tangente al circulo 2?



print (C1.tangent_lines(P4)); #Cuales son las rectas tangentes  al circulo 1 con el punto 4
```


The result of running the script is the following:

```python


1105*pi/98


9*pi


sqrt(2210)/14


(x - 5/14)**2 + (y - 27/14)**2 - 1105/98


Point(5/14, 27/14)


sqrt(2210)*pi/7


[Point(55/754 + 27*sqrt(6665)/754, -5*sqrt(6665)/754 + 297/754), Point(-27*sqrt(6665)/754 + 55/754, 297/754 + 5*sqrt(6665)/754)]


[Point(3, 4)]


False


[Line(Point(-1, 5), Point(-9/26 + 15*sqrt(17)/26, 3*sqrt(17)/26 + 45/26)), Line(Point(-1, 5), Point(-15*sqrt(17)/26 - 9/26, -3*sqrt(17)/26 + 45/26))]


```

Below is an image of the execution process in ipython notebook:

![](./images/geometriaanaliticaconsympycirculos-1.png)

##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
