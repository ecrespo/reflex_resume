Title: Profiling a Python script with the cProfile tool
Date: 2016-06-13 12:00 
Category: Tutorial Python
Tags: Python,Profiling,cProfile
lang: en  
translation: true  
  
A while ago I covered profiling tools for Python ([see link](/blog/tags)).

There are other tools like cProfile that can be used and are less invasive than those in the previous articles; I mean, they do not require modifying the application code in order to be used.

As a test script I will use the same square root one found in my repo on [github](https://github.com/ecrespo/raizcuadrada), the same one from the articles on [unit tests](/blog/pruebasunitariasenpythonconunittest), [unit tests with docker](/blog/ejecutarunapruebadeunittestenpythonconuncontenedordocker), [documentation tests](/blog/separarcodigodepruebasdeladocumentaciondoctest2), [documentation tests with docker](/blog/ejecutarunapruebadedoctestconuncontenedordocker)  and the one on [pylint with docker](/blog/analizarcodigopythonconpylintdesdedocker).

Nothing needs to be installed to use `cProfile`.

The code of the square root module is the following:
```python
#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""

Se importa el módulo math para calcular la raiz cuadrada.

"""

import math



#Función raiz cuadrada.

def Raiz(a):

    """Si a es mayor o igual a cero se calcula la raiz cuadrada"""

    if a >= 0:

        return math.sqrt(a)

    #Si es menor a cero se genera una excepción donde se informa que a debe ser mayor o igual a cero.

    else:

        raise ValueError("a debe ser >= 0")



if __name__ == '__main__':

    #Se importa el módulo doctest

    #import doctest

    #Se realiza la prueba al archivo raizcuadra.txt

    #doctest.testfile("raizcuadrada.txt")

    Raiz(5)

    Raiz(9)

    Raiz(25)

    #Raiz(-1)

```

To run cProfile:
```python
python -m cProfile -s cumtime raizcuadrada.py

         8 function calls in 0.000 seconds



   Ordered by: cumulative time



   ncalls  tottime  percall  cumtime  percall filename:lineno(function)

        1    0.000    0.000    0.000    0.000 raizcuadrada.py:6(<module>)

        3    0.000    0.000    0.000    0.000 raizcuadrada.py:10(Raiz)

        3    0.000    0.000    0.000    0.000 {math.sqrt}

        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

```


The same can be run from the container used in the `pyLint` article:
```
docker run  -v "$PWD:/app" -ti prueba-python  python -m cProfile -s cumtime raizcuadrada.py
```

A figure of the command's execution is shown below:

![](./images/profilingdeunscriptpythonconcprofile-1.png)




For more information you can check the [official python documentation](https://docs.python.org/2/library/profile.html), [an article in English about cProfile (broken link)](https://julien.danjou.info/guide-to-python-profiling-cprofile-concrete-case-carbonara/) and a [performance analysis guide for python (broken link)](https://www.huyng.com/posts/python-performance-analysis). 


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
