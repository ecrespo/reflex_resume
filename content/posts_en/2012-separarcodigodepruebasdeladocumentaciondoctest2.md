Title: Separating test code from the documentation (doctest, part 2)
Date: 2012-12-14 9:00
Category: 
Tags: Canaima,Linux,Python,Ubuntu
lang: en
translation: true

The [previous article](/blog/probarcodigocondoctest) explained how to use `doctest` inside code to run tests on the documentation of each function.

Now I will explain how to run those documentation tests from a file separate from the program code. The same example from the previous article will be used, but adapted so that the documentation is in a separate text file.

The code is shown below:
```python
#!/usr/bin/env python

# -*- coding: utf-8 -*-

#Se importa el módulo math para calcular la raiz cuadrada.

import math

#Función raiz cuadrada.

def Raiz(a):

    #Si a es mayor o igual a cero se calcula la raiz cuadrada

    if a >= 0:

        return math.sqrt(a)

    #Si es menor a cero se genera una excepción donde se informa que a debe ser mayor o igual a cero.

    else:

        raise ValueError("a debe ser >= 0")

if __name__ == '__main__':

    #Se importa el módulo doctest

    import doctest

    #Se realiza la prueba al archivo raizcuadra.txt

    doctest.testfile("raizcuadrada.txt")
```

As you can see, the test is run on the file raizcuadrada.txt. The file contains the following:

```python
Modulo raiz cuadrada

=====================

Usando  'raizcuadrada'

------------------------------

Primero se importa la función:

>>> from raizcuadrada import Raiz
```

Examples of square root calculation:

```python
>>> Raiz(4)

2.0

>>> Raiz(9)

3.0

>>> Raiz(25)

5.0

>>> Raiz(0)

0.0

>>> Raiz(-1)

Traceback (most recent call last):

...

ValueError: a debe ser >= 0
```
Now comes running the command that returns the test results:
```
python -m doctest -v raizcuadrada.txt

Trying:

    from raizcuadrada import Raiz

Expecting nothing

ok

Trying:

    Raiz(4)

Expecting:

    2.0

ok

Trying:

    Raiz(9)

Expecting:

    3.0

ok

Trying:

    Raiz(25)

Expecting:

    5.0

ok

Trying:

    Raiz(0)

Expecting:

    0.0

ok

Trying:

    Raiz(-1)

Expecting:

    Traceback (most recent call last):

    ...

    ValueError: a debe ser >= 0

ok

1 items passed all tests:

   6 tests in raizcuadrada.txt

6 tests in 1 items.

6 passed and 0 failed.


Test passed.
```

As you can see, in this case the program is imported first and then the tests begin.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)