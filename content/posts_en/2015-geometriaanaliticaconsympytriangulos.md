Title: Analytic Geometry with Sympy (triangles)  
Date: 2015-03-22 9:00  
Category: Tutorial Python  
Tags: Canaima,Debian,General,Python,Ubuntu,Sympy  
lang: en  
translation: true  

Here are the articles about sympy covered previously:

* [Computing limits with sympy](/blog/calculodelimitesconlalibreriasympy)
* [Computing derivatives with sympy](/blog/calculodederivadasconsympy)
* [Computing integrals with sympy](/blog/calculodeintegralesconsympy)
* [Solving systems of linear equations with sympy](/blog/resoluciondesistemasdeecuacionesconsympy)
* [Analytic Geometry with sympy (segments)](/blog/geometriaanaliticaconsympysegmentos)
* [Analytic Geometry with sympy (lines)](/blog/geometriaanaliticaconsympyrectas)
* [Analytic Geometry with sympy (circles)](/blog/geometriaanaliticaconsympycirculos)  

This article explains the analytic geometry instructions for the case of the triangle.

The script code is the following:
```python
#!/usr/bin/env python

from sympy.geometry import *


#Creacion de 4 puntos
P1 = Point(0, 0)
P2 = Point(3, 4)
P3 = Point(2, -1)
P4 = Point(-1, 5)

T = Triangle(P1, P2, P3) ; #Se crea el triangulo con los puntos p1,p2 y p3

print (T.area); #Se calcula el area del triangulo

print (T.angles); #Angulos del triangulo

print (T.sides);#Lados del triangulo

print (T.perimeter);#Perimetro

print (T.is_right())  ; #triangulo recto?

print (T.is_equilateral());#triangulo equilatero?

print (T.is_isosceles());#triangulo isosceles?

print (T.is_scalene());#triangulo escaleno?

print (T.altitudes);#Altitudes

print (T.orthocenter) ;#Intercepcion de las altitudes

print (T.bisectors()) ;#bisector

print (T.incenter) ;#en centro

print (T.incircle); #en circulo

print (T.inradius); #en radio

print (T.medians); #medianas

print (T.centroid);#intercepcion de las medianas

print (T.circumcenter); #intercepcion de bisectores perpendiculares

print (T.circumcircle)

print (T.circumradius)

print (T.medial)

C1 = Circle(P1, 3);#se crea un circulo con centro en P1 y radio 3.

print (T.intersection(C1));#intercepcion del triangulo con el circulo c1

print (T.distance(T.circumcenter)); #minima distancia desde un punto a otro de un segmento

print (T.is_similar(Triangle(P1, P2, P4)));# si dos triangulos son similares?

```


The output of the script is shown below:
```
-11/2
{Point(2, -1): acos(3*sqrt(130)/130), Point(0, 0): acos(2*sqrt(5)/25), Point(3, 4): acos(23*sqrt(26)/130)}
[Segment(Point(0, 0), Point(3, 4)), Segment(Point(2, -1), Point(3, 4)), Segment(Point(0, 0), Point(2, -1))]
sqrt(5) + 5 + sqrt(26)
False
False
False
True
{Point(2, -1): Segment(Point(6/25, 8/25), Point(2, -1)), Point(0, 0): Segment(Point(0, 0), Point(55/26, -11/26)), Point(3, 4): Segment(Point(4/5, -2/5), Point(3, 4))}
Point(10/11, -2/11)
{Point(2, -1): Segment(Point(3*sqrt(5)/(sqrt(5) + sqrt(26)), 4*sqrt(5)/(sqrt(5) + sqrt(26))), Point(2, -1)), Point(0, 0): Segment(Point(0, 0), Point(sqrt(5)/4 + 7/4, -9/4 + 5*sqrt(5)/4)), Point(3, 4): Segment(Point(-50 + 10*sqrt(26), -5*sqrt(26) + 25), Point(3, 4))}
Point((3*sqrt(5) + 10)/(sqrt(5) + 5 + sqrt(26)), (-5 + 4*sqrt(5))/(sqrt(5) + 5 + sqrt(26)))
Circle(Point((3*sqrt(5) + 10)/(sqrt(5) + 5 + sqrt(26)), (-5 + 4*sqrt(5))/(sqrt(5) + 5 + sqrt(26))), -11/(sqrt(5) + 5 + sqrt(26)))
-11/(sqrt(5) + 5 + sqrt(26))
{Point(2, -1): Segment(Point(3/2, 2), Point(2, -1)), Point(0, 0): Segment(Point(0, 0), Point(5/2, 3/2)), Point(3, 4): Segment(Point(1, -1/2), Point(3, 4))}
Point(5/3, 1)
Point(45/22, 35/22)
Circle(Point(45/22, 35/22), 5*sqrt(130)/22)
5*sqrt(130)/22
Triangle(Point(3/2, 2), Point(5/2, 3/2), Point(1, -1/2))
[Point(9/5, 12/5), Point(sqrt(113)/26 + 55/26, -11/26 + 5*sqrt(113)/26)]
sqrt(26)/11
False
```
You can see the code of the script above at the following [link (broken link)](https://bitbucket.org/ecrespo/ernesto-ecrespo.blogspot/src/b0d6030a28a7c1fdc96f58e18047ba7b39945d79/geometriaanalitica/geometria-triangulo.py?at=default) on bitbucket.org.

You can also use a notebook (ipython notebook); the file that was used can be downloaded at the [link (broken link)](https://bitbucket.org/ecrespo/ernesto-ecrespo.blogspot/src/b0d6030a28a7c1fdc96f58e18047ba7b39945d79/geometriaanalitica/Geometr%C3%ADa%20Anal%C3%ADtica%20-%20Tri%C3%A1ngulo.ipynb?at=default).

The following figures show the execution of the notebook:

![](./images/geometriaanaliticaconsympytriangulos-1.png)

![](./images/geometriaanaliticaconsympytriangulos-2.png)

![](./images/geometriaanaliticaconsympytriangulos-3.png)

![](./images/geometriaanaliticaconsympytriangulos-4.png)


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)