Title: Back to basics, OOP in Python (part 3)
Date: 2015-12-31 9:00  
Category: Tutorial Python  
Tags: Python,POO  
lang: en
translation: true  

Continuing with some OOP concepts in Python, here are the previous articles:

1. [Back to basics, OOP in Python (part 1)](/blog/volviendoalobasicopooenpython-1)
2. [Back to basics, OOP in Python (part 2)](/blog/volviendoalobasicopooenpython-2)

This article shows the use of  __ `getattr`__  (executed when accessing an attribute that does not exist), how to get and modify values, and how this is simplified with the `@property` decorator.

The class Punto will be created to show the use of __`getattr` __ :
```python
class Punto(object):

 def __init__(self,x=3,y=5):

  self._x = x

  self._y = y


 def __getattr__(self,attr):

  print "No se puede acceder a un atributo invalido"


if __name__ == "__main__":

 punto = Punto(5,5)

 punto.var

```

When the program is run you get:
```python
$ python ej6.py
```
No se puede acceder a un atributo inválido

When trying to access a non-existent attribute, the __ `getattr`__ method is executed, which prints the message that an invalid attribute cannot be accessed.

The following code shows the Punto class again but this time with two methods, one that shows the value of the point and another that modifies the value of the point, and the built-in `property` function will be used.
The syntax of the `property` function is:  

```python
property(getter,setter,delete,doc).
```  

The code below:

```python
class Punto(object):

 def __init__(self,x,y):

  self._x = x

  self._y = y



 def get_punto(self):

  return (self._x, self._y)



 def set_punto(self,punto):



  self._x, self._y = punto



 punto = property(get_punto,set_punto)





if __name__ == "__main__":

 punto = Punto(4,6)

 print(punto.punto)

 punto.punto = (10,15)

 print(punto.punto)


```


When the program is run you get:
```python
$ python ej7.py
(4, 6)
(10, 15)
```

As a last example of using `getter` and `setter`, the use of the `@property` decorator is shown, and how it simplifies the use of `property` compared to the previous code:

```python

#!/usr/bin/env python3


# -*- coding: utf-8 -*-





class Punto(object):





 def __init__(self,punto):


  self._x,self._y = punto





 @property


 def punto(self):


  return (self._x,self._y)





 @punto.setter


 def punto(self,punto):


  self._x,self._y = punto








if __name__ == "__main__":


 cordenada = Punto((4,6))


 print(cordenada.punto)


 cordenada.punto = (10,15)


 print(cordenada.punto)

```



When the program is run you get:
```python
$ python ej8.py
(4, 6)
(10, 15)
```
The first thing done is to define a method punto that returns a tuple with the value of x and y; the property decorator is applied to this method. Then another method, also called punto, is created that takes a point and assigns it to x and y, but defining a @punto.setter decorator. The first method does the job of the getter and the second that of the setter.

Reference:

1. [Advanced Python (broken link)](https://magmax.org/blog/2013/9/30/python-avanzado/)
2. [Reference examples (modules and tasks)](http://www.sromero.org/wiki/programacion/tutoriales/python/ref_ejemplos)

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
