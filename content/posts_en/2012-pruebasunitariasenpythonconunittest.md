Title: Unit Tests in Python with unittest
Date: 2012-12-26 9:00
Category: Tutorial Python
Tags: General,Linux,numpy,Python,TDD,unittest
lang: en
translation: true

Continuing with the tools that help ensure quality, unit tests will now be written for the square root function from the previous article ([Testing code with doctest](/blog/probarcodigocondoctest)).

[Test driven development](http://es.wikipedia.org/wiki/TDD) (TDD) is a programming practice that involves two practices: writing the tests first and continuously refactoring the code.

To write the tests first, [unit tests](http://es.wikipedia.org/wiki/Prueba_unitaria) are generally used. This is a way of testing that a module of code works correctly. It ensures that each module works correctly on its own, and then with [integration tests](https://es.wikipedia.org/wiki/Pruebas_de_integraci%C3%B3n) you can ensure that the system as a whole works correctly.

The test-driven development (TDD) cycle.
First a list of requirements must be defined, and then the following cycle is run:

1. Choose a requirement: From the list, choose the requirement you believe will give the most insight into the problem and that is also easy to implement.  

2. Write a test.  

3. Verify that the test fails: If the test does not fail, either the requirement was already implemented or the test is wrong.   

4. Run the automated tests: Verify that the whole set of tests works correctly.  

5. Remove duplication: Duplicated code is removed.   

6. Update the list of requirements: The list is updated by crossing out the implemented requirement.

For a unit test to be good it has to meet the following requirements:

- Automatable: It must not be run manually (useful for continuous integration).  

- Complete: They must cover as much code as possible.  

- Reusable: Do not create tests that can only be run once (useful for continuous integration).  

- Independent: Running one test must not affect the running of another test.

- Professional: Tests must be treated like code, with the same professionalism, documentation, etc. 

Unit tests are automated tests that test small pieces of code, usually a function or a method.

Python has the `PyUnit` API for unit tests. The module is called `unittest`, and it is based on the `XUnit` framework designed by Ken Beck and Erich Gamma.

The example code shows, on one side, the Raiz function and, on the other, the RaizTest class that inherits from `unittest.TestCase`. This class will have 3 methods: the first calculates the root of 9 and returns 3, the second calculates the root of 0 and returns 0, and the last calculates the root of a negative value and returns an exception or error message.

The code is shown below:

```python
#!/usr/bin/env python

# -*- coding: utf-8 -*-

#Se importa el módulo unittest y math

import unittest

import math

#Función raiz cuadrada.

def Raiz(a):

    #Si a es mayor o igual a cero se calcula la raiz cuadrada

    if a >= 0:

        return math.sqrt(a)

    #Si es menor a cero se genera una excepción donde se informa que a debe ser mayor o igual a cero.

    else:

        raise ValueError,"a debe ser >= 0"

class RaizTest(unittest.TestCase):

    def test_Raiz(self):

        #Test para la raiz de nueve que devuelve 3 que debe pasar.

        self.assertEqual(3, Raiz(9))

    def test_zero(self):

        #Test para la raiz de 0 que devuelve 0, que debe pasar.

        self.assertEqual(0, Raiz(0))    

    def test_negative(self):

        #Test para la raiz de un número negativo, que debe fallar.

        # Este debe devolver un ValueError, pero se espera un IndexError.

        self.assertRaises(IndexError, Raiz(-10))

if __name__ == '__main__':

    #Se ejecuta la prueba unitaria

    unittest.main()

```

When the code is run, you get the following:  
```
ecrespo@jewel:~/proyectos/ernesto-ecrespo.blogspot/timeit$ python test-raiz.py 
.E.
======================================================================
ERROR: test_negative (__main__.RaizTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test-raiz.py", line 40, in test_negative
    self.assertRaises(IndexError, Raiz(-10))
  File "test-raiz.py", line 24, in Raiz
    raise ValueError,"a debe ser >= 0"
ValueError: a debe ser >= 0

----------------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (errors=1)
```

As you can see, the test with a negative value fails. 
If the negative-value test method is commented out, the run reports no errors:
```
ecrespo@jewel:~/proyectos/ernesto-ecrespo.blogspot/timeit$ python test-raiz.py 
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

The `unittest` functions used are:  

- `assertEqual`: Tests that two values are equal.
- `assertRaises`: Tests that an exception is raised.  

For more methods of the unittest module, see the [documentation](https://docs.python.org/2/library/unittest.html#unittest.TestCase).



##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)