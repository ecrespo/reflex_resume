Title: Analytic Geometry with Sympy (Segments)
Date: 2015-02-21 11:10
Category: Tutorial Python
Tags: Canaima,Debian,General,Python,Ubuntu,Sympy
lang: en
translation: true


The previous articles covered how to solve [limits](/blog/calculodelimitesconlalibreriasympy), [derivatives](/blog/calculodederivadasconsympy), [integrals](/blog/calculodeintegralesconsympy) and [solving systems of linear equations](/blog/resoluciondesistemasdeecuacionesconsympy). Now I will explain the use of Sympy in analytic geometry.

The articles on analytic geometry are based on an article in English, [Computational Geomtry in Python](https://blancosilva.github.io/post/2014/10/28/Computational-Geometry-in-Python.html?utm_source=Python+Weekly+Newsletter&utm_campaign=13e141cbb8-Python_Weekly_Issue_177_February_5_2015&utm_medium=email&utm_term=0_9e26887fc5-13e141cbb8-312675721).

This article explains how to work with segments.

Start ipython notebook (if you want to use the file for this article you can download it from the following [link (broken link)](https://bitbucket.org/ecrespo/ernesto-ecrespo.blogspot/src/ba234aef56bf9df8c2195c5f413b16732b9806ed/geometriaanalitica/geometria-segmentos.ipynb?at=default)).


Below is the script code:
```python
#!/usr/bin/env python



from sympy.geometry import *



#Definicion de puntos

P1 = Point(0, 0)

P2 = Point(3, 4)

P3 = Point(2, -1)

P4 = Point(-1, 5)



#Definicion de segmentos

S1 = Segment(P1, P2)

S2 = Segment(P3, P4)



print Point.is_collinear(P1, P2, P3); #Los puntos son colineales?



print S1.length ; #longitud del segmento 1



print S2.midpoint ;#punto medio del segmento 2



print S1.slope; #Slope del segmento 1



print S1.intersection(S2) ; #Intercepcion entre el Segmento 1 y 2



print Segment.angle_between(S1, S2);#Angulo entre el segmento 1 y 2



print S1.contains(P3);#El segmento  1 contiene a P3?

```

The result of running the script is shown below:
```python
False

5

Point(1/2, 2)

4/3

[Point(9/10, 6/5)]

acos(-sqrt(5)/5)

False
```
The following image shows the notebook running:

![](./images/geometriaanaliticaconsympysegmentos-1.png)

##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
