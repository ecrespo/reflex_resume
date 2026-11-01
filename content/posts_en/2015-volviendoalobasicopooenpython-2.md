Title: Back to basics, OOP in Python (part 2)
Date: 2015-12-25 9:00
Category: Tutorial Python  
Tags: Python,POO
lang: en
translation: true

Continuing the series of articles on object-oriented programming with python, here is the link to the [first article](/blog/volviendoalobasicopooenpython-1).

The following article is based on a blog article published at [www.toptal.com (broken link)](https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide).

The previous article shows the variables id_ciudad and cont_ciudad as class attributes. The following example will show that it is not always a good idea to use class attributes, because it breaks the OOP rule of encapsulation.

```python

#!/usr/bin/env python3


# -*- coding: utf-8 -*-



class Servicio(object):


 dato = []



 def __init__(self,otro_dato):


  self.otro_dato = otro_dato



if __name__ == "__main__":


 s1 = Servicio(["a","b"])


 s2 = Servicio(["c","d"])


 s1.dato.append(1)


 print "dato de S1: ",s1.dato


 print "dato de S2: ",s2.dato


 s2.dato.append(2)


 print "dato de s1: ",s1.dato


 print "dato de s2: ",s2.dato


 print "otro dato de s1: ", s1.otro_dato


 print "otro dato de s2: ", s2.otro_dato

```


Running the code gives:

```python
dato de S1:  [1]


dato de S2:  [1]


dato de s1:  [1, 2]


dato de s2:  [1, 2]


otro dato de s1:  ['a', 'b']


otro dato de s2:  ['c', 'd']
```


The first 4 lines of the output show that instance s1 and instance s2 practically have the same value: the data is added in s1 and it is reflected in s2, then the data is added in s2 and it is reflected in s1.

The English article mentions that the solution would be not to have an empty list as the class attribute but to set it to None.

Here is the code:

```python
#!/usr/bin/env python3


# -*- coding: utf-8 -*-


class Servicio(object):


 dato = None





 def __init__(self,otro_dato):


  self.otro_dato = otro_dato





if __name__ == "__main__":


 s1 = Servicio(["a","b"])


 s2 = Servicio(["c","d"])


 s1.dato = 1


 print "dato de S1: ",s1.dato


 print "dato de S2: ",s2.dato


 s2.dato = 2


 print "dato de s1: ",s1.dato


 print "dato de s2: ",s2.dato

```



The result of running it is the following:

```python
dato de S1:  1


dato de S2:  None


dato de s1:  1


dato de s2:  2

```

As you can see, it no longer shows equal values between the two instances of the class.

Now I show the code without the class attribute, creating dato as a private variable and some methods that access dato:

```python

#!/usr/bin/env python3


# -*- coding: utf-8 -*-


class Servicio(object):


 def __init__(self,otro_dato):


  self.__dato = []


  self.otro_dato = otro_dato





 def mostrar_dato(self):


  return self.__dato





 def agregar_dato(self,dato):


  self.__dato.append(dato)





 def inicializar_dato(self,):


  self.__dato = []





if __name__ == "__main__":


 s1 = Servicio(["a","b"])


 s2 = Servicio(["c","d"])


 try:


  s1.dato.append(1)


 except AttributeError:


  print "No se pudo agregar a dato de s1"


 finally:


  print s1.mostrar_dato()


  print s2.mostrar_dato()


  s1.agregar_dato(1)


  s1.agregar_dato(3)


  s2.agregar_dato(2)


  s2.agregar_dato(4)


  print s1.mostrar_dato()


  print s2.mostrar_dato()


```

Running the script gives the following:

```python

No se pudo agregar a dato de s1


[]


[]


[1, 3]


[2, 4]


```

Creating instance attributes is not a mistake; what you need to know is exactly what you need in the class to avoid these errors, and it is best to follow the object-oriented programming paradigm.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
