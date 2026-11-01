Title: Back to basics, OOP in Python (difference between `__init__` and `__new__`) (part 10)
Date: 2017-02-05 09:00
Category: Tutorial Python
Tags: Python,POO
lang: en
translation: true

Continuing with the series of [back to basics OOP articles](/blog/tags), this article covers the differences between `__init__` and `__new__`.

This article is based on an article in [English, understanding new and init (broken link)](http://spyhce.com/blog/understanding-new-and-init) .

Many people who have done object-oriented programming in Python have never used the `__new__` method; the one they use as a constructor is `__init__`.

The reality is that the `__init__` method creates the object and then initializes it; it is not the constructor as such, whereas the `__new__` method only constructs the object.

This article will work with Python 3.

We have the following class:

```python
class A(object):

    pass
```

So Class A inherits from object in Python 3.


Now a class that uses `__new__` and `__init__` is created:

```python


class A(object):


    def __new__(cls):


        print "A.__new__ es llamado"


        return super(A, cls).__new__(cls)





    def __init__(self):


        print "A.__init__ es llamado"





A()

```


The output is the following:
```
A.__new__ es llamado
A.__init__ es llamado
```

Now let's look at an example where `__init__` will not be called:

```
class A(object):
    def __new__(cls):
        print "A.__new__ es llamado"

    def __init__(self):
        print "A.__init__ es llamado"

print ("Solo llamando el objeto A() o instanciandolo")

A()
a = A()
print ("*"*40)
print ("Ejecutando un print con el objeto A()")
print (A())

```

As you can see, a print is executed in the `__init__` method and also in the `__new__` method.

The output is the following:
```
Solo llamando el objeto A() o instanciandolo
A.__new__ es llamado
A.__new__ es llamado
****************************************
Ejecutando un print con el objeto A()
A.__new__ es llamado
None
```

As you can see, when calling A() or instantiating it, only the output of the `__new__` method is shown, and not that of `__init__`; only when print(A()) is executed does it return the output of the `__new__` method, and the `__init__` method returns `None`.

Now the class with only the `__new__` method will be shown, where a print is executed and a number is returned:

```python
class A(object):

    def __new__(cls):


        print "A.__new__ es llamado"


        return 29


print ("Solo llamando al objeto")


A()


print ("*"*30)


print ("Llamando al objeto desde un print")


print A()
```

The output is the following:

Solo llamando al objeto
A.__new__ es llamado
******************************
Llamando al objeto desde un print
A.__new__ es llamado
29


When only calling the object it just shows the print, but when running the print it shows the method's print and the integer it returns.

Now the same will be done but with the __init__ method:



class A(object):



    def __init__(self):

        print "A.__init__ es llamado"

        return 33





try:

    print ("Solo llamando al objeto")

    A()

except (TypeError):

    print ("Error de tipo")



The output is the following:
```
Solo llamando al objeto
A.__init__ es llamado
Error de tipo
```

In this case the `return` gives `error de tipo`. The only way for the `__init__` method to return something is for it to be of type `None`.

Now the use of an alternative class called `Ejemplo` is shown:

```python
class Ejemplo(object):


    def __str__(self):


        return "Ejemplo"


class A(object):


    def __new__(cls):


        return Ejemplo()


class B(object):


    def __new__(cls):


        return super(B, cls).__new__(Ejemplo)


print ("Prueba con A")


print A()


print ("Prueba con B")


print B()
``` 


The output returns the following:
```
Prueba con A
Ejemplo
Prueba con B
Ejemplo
```

As can be seen, there are cases where using `__new__` is useful and others where `__init__` can still be used.

The `__new__` method is used in design patterns with python, which will be the next series of articles in this blog.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
