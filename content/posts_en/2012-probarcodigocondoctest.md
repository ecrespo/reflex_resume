Title: Testing code with doctest
Date: 2012-12-13 9:00
Category: Tutorial Python
Tags: Canaima,Debian,General,Linux,Python,Ubuntu,doctest
lang: en
translation: true

`Doctest` is a framework that ships with Python and lets you develop applications using TDD ([Test-driven development](https://es.wikipedia.org/wiki/Desarrollo_guiado_por_pruebas)).

TDD requires writing the tests first and refactoring the code to reach the desired result.

Here `doctest` will be used, which runs tests based on the documentation written in the code. This means you need clear documentation for each function before developing it, so that the cases where the function works correctly and the cases where it can fail are well defined.

The example code is a function that calculates the square root of a number.

Here is the code:
```python
#!/usr/bin/env python

# -*- coding: utf-8 -*-

#Se importa el módulo math para calcular la raiz cuadrada.

import math

#Función raiz cuadrada.

def RaizCuadrada(a):

    """

    >>> RaizCuadrada(4)

    2.0

    >>> RaizCuadrada(9)

    3.0

    >>> RaizCuadrada(25)

    5.0

    >>> RaizCuadrada(0)

    0.0

    >>> RaizCuadrada(-1)

    Traceback (most recent call last):

        ...

    ValueError: a debe ser >= 0

    """

    #Si a es mayor o igual a cero se calcula la raiz cuadrada

    if a >= 0:

        return math.sqrt(a)

    #Si es menor a cero se genera una excepción donde se informa que a debe ser mayor o igual a cero.

    else:

        raise ValueError("a debe ser >= 0")
```

As shown, the documentation contains a series of execution cases for the function, where it must return a correct value, and if a value that cannot be calculated is passed, it raises the exception.

To run the test, execute the code by calling the `doctest` module in `verbose` mode:
```python
python -m doctest -v prueba-raizcuadrada.py
```
The result is the following:
```python
Trying:

    RaizCuadrada(4)

Expecting:

    2.0

ok

Trying:

    RaizCuadrada(9)

Expecting:

    3.0

ok

Trying:

    RaizCuadrada(25)

Expecting:

    5.0

ok

Trying:

    RaizCuadrada(0)

Expecting:

    0.0

ok

Trying:

    RaizCuadrada(-1)

Expecting:

    Traceback (most recent call last):

        ...

    ValueError: a debe ser >= 0

ok

1 items had no tests:

    prueba-raizcuadrada

1 items passed all tests:

   5 tests in prueba-raizcuadrada.RaizCuadrada

5 tests in 2 items.

5 passed and 0 failed.

Test passed.
```

As shown, all the cases passed the test.
You can check the following documentation and tutorials:
The official documentation can be found at the following [link](https://docs.python.org/2/library/doctest.html).  

- [How to write tests 1: Doctest](http://magmax9.blogspot.com/2011/09/python-como-hacer-pruebas-1.html).
- [Introduction to doctest (broken link)](http://pythontesting.net/framework/doctest/doctest-introduction/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A%20PythonTesting%20%28Python%20Testing%29).
- [Another Doctest tutorial](https://pymotw.com/3/doctest/)  

Another article will explain how to separate the different cases into a text file and keep the program in a separate script.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)