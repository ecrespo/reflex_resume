Title: Back to basics, OOP in Python (part 1)
Date: 2015-12-18 9:00
Category: Tutorial Python  
Tags: Python,POO
lang: en
translation: true


After a while of writing articles on very diverse python topics, I am now starting a series on object-oriented programming from the basics up to the new features added to the language.

This will also help me correct some of my practices regarding object-oriented programming and learn new ones.

I am currently using a web tool that evaluates code quality; this site is called [www.quantifiedcode.com. (broken link)](https://www.quantifiedcode.com/)

I ran into errors in a project, which is why I am starting this series of articles.

The following figure shows how the tool displays the errors:

![](./images/volviendoalobasicopooenpython1-1.png)

The nice thing is that when you commit to github, `quantifiedcode` automatically sends an email with the issues.


Well, now on to the article itself.

We have a city class with several methods.

The code is shown below:
```python

#!/usr/bin/env python3

from math import *

#Se crea la clase ciudad que hereda de object.

#Esto se declara asi actualmente por convencion.

class Ciudad(object):

 #Datos

 cont_ciudad = 0

 id_ciudad = 0


 def __init__(self,nombre='',x=0,y=0):

  """Constructor que recibe el nombre de la ciudad,x y y"""

  self.nombre = nombre

  self.x = x

  self.y = y

  Ciudad.cont_ciudad += 1

  self.id_ciudad = Ciudad.cont_ciudad



 def __str__(self):

  """Metodo que retorna un string con la info de la ciudad"""

  return 'Ciudad: ' + self.nombre + ',id= ' + str(self.id_ciudad) + ',x= %s,y=%s' %(self.x,self.y)



 def __set__( self, nombre):

  """Metodo que asigna un valor"""

  self.nombre= nombre



 def __get__( self):

  """Metodo que obtiene un valor"""

  return  self.nombre



 def mover_a(self,x=0,y=0):

  """Metodo que cambia de valor a x y y"""

  self.x += x

  self.y += y



 def distancia(self, otra_ciudad):

  """Metodo que calcula la distancia con respecto a otra ciudad"""

  xi = pow(otra_ciudad.x-self.x,2)

  yi = pow(otra_ciudad.y-self.y,2)

  return sqrt(xi+ yi)



 def __del__(self):

  """Elimina la clase"""

  #obtener el nombre de una clase

  class_name = self.__class__.__name__

  print('class ', class_name, 'destroyed')





 #Inicializando un metodo estatico

 #Es el caso que no se referencia al objeto en si mismo con

 #self

 @staticmethod

 def info():

  """Metodo que devuelve el nombre del desarrollador"""

  return  "Desarrollado por Seraph"







if __name__ == "__main__":

 a = Ciudad('Valencia',5,5)

 b = Ciudad('Maracay',5,15)

 print(a)

 print(b)

 print(Ciudad.cont_ciudad)

 a.mover_a(4,3)

 b.mover_a(7,12)

 print(a.info())

 print(a)

 print(b)

```


The info method uses a decorator called `staticmethod` that defines it as a static method, since self is not passed to it in order to work with methods or variables of the object itself.

The result of running the script is the following:
```python
Ciudad: Valencia,id= 1,x= 5,y=5
Ciudad: Maracay,id= 2,x= 5,y=15
2
Desarrollado por Seraph
Ciudad: Valencia,id= 1,x= 9,y=8
Ciudad: Maracay,id= 2,x= 12,y=27
('class\t', 'Ciudad', 'destroyed')
('class\t', 'Ciudad', 'destroyed')
```


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)