Title: Unit tests in Python using mocking and docker
Date: 2017-03-11 09:00
Category: Tutorial Python
Tags: Numpy,Python,Mocking,Docker,Pruebas unitarias
lang: en
translation: true

A while ago I wrote an article on [unit testing with python using Docker (broken link)](/blog/pruebasunitariasconunitestenpythonusandonosetestsydockerdockercompose).  That article shows the different options for unit testing methods; this one focuses on mocking data (simulating data).

This article is based on the article from the [semaphoreci](http://semaphoreci.com/) site, called [Getting Started with Mocking in Python](http://semaphoreci.com/community/tutorials/getting-started-with-mocking-in-python).

Below is the initial code of the `Dockerfile`, of `calculadora.py` and of the test:

`Dockerfile` file:

```python
FROM python
WORKDIR /code/

RUN pip3 install --upgrade pip
RUN pip3 install nose
RUN pip3 install nose-cov
RUN pip3 install rednose
RUN pip3 install pytest
RUN pip3 install pytest-cov
RUN pip3 install mock


#EXPOSE 5000

ADD . /code/
COPY . /code/


#CMD nosetests  --with-coverage
#CMD nosetests -sv --rednose
CMD python -m unittest

```

`docker-compose.yml` file:
```python
pruebas:
  build: .

  volumes:
    - ".:/code"
```

`calculadora.py` file:
```python
#!/usr/bin/env python
#Se importa sqrt de math
from math import sqrt


#Clase calculadora
class Calculadora:
    #Metodo suma de x y y, se evalua si son enteros si no, devuelve error.
    def suma(self,x,y):
        if type(x) == int and type(y) == int:
            return x + y
        else:
            raise TypeError("Invalid type: {} and {}".format(type(x),type(y)))
```
`calculadora_test.py` file:
```python
#!/usr/bin/env python3

from unittest import TestCase
from app.calculadora import Calculadora





class TestCalculadora(TestCase):
    def setUp(self):
        self.calc = Calculadora()

    def test_suma_retorna_resultado_correcto(self):
        ##Asegura que sea igual la operacion de suma 2+2 a 4
        respuesta = self.calc.suma(2,4)
        self.assertEqual(respuesta, 6)

```

When you run `docker-compose up` you get:
```python
docker-compose up 
Starting tutorialespruebas_pruebas_1
Attaching to tutorialespruebas_pruebas_1
pruebas_1 | .
pruebas_1 | Name                 Stmts   Miss  Cover
pruebas_1 | ----------------------------------------
pruebas_1 | app.py                   0      0   100%
pruebas_1 | app/calculadora.py       6      0   100%
pruebas_1 | unit.py                  0      0   100%
pruebas_1 | ----------------------------------------
pruebas_1 | TOTAL                    6      0   100%
pruebas_1 | ----------------------------------------------------------------------
pruebas_1 | Ran 1 test in 0.022s
pruebas_1 | 
pruebas_1 | OK
tutorialespruebas_pruebas_1 exited with code 0
```
Now a change will be made. Instead of calling suma from the calculator, the result will be simulated using `mocking`. For that, the only change will be to `calculadora_test.py`.

Here is the code of the file:
```python
#!/usr/bin/env python3

from unittest import TestCase
from app.calculadora import Calculadora
from unittest.mock import patch



class TestCalculadora(TestCase):
    

    @patch('app.calculadora.Calculadora.suma', return_value=9)
    def test_suma_retorna_resultado_correcto(self,suma):
        self.assertEqual(suma(2,3), 9)
```

`patch` is imported from `mock`, and the `patch` decorator is called, passing the calculadora suma method as an argument, where it is defined to return the value 9 regardless of the input arguments of that method.  Then the `test_suma_retorna_resultado_correcto` method is run, passing it suma, and it asserts that the sum of 2 and 3 gives 9. 

When you run `docker-compose up` you get the following result:
```python
docker-compose up 
Starting tutorialespruebas_pruebas_1
Attaching to tutorialespruebas_pruebas_1
pruebas_1 | .
pruebas_1 | Name                 Stmts   Miss  Cover
pruebas_1 | ----------------------------------------
pruebas_1 | app.py                   0      0   100%
pruebas_1 | app/calculadora.py       7      0   100%
pruebas_1 | unit.py                  0      0   100%
pruebas_1 | unittest/mock.py      1278   1278     0%
pruebas_1 | ----------------------------------------
pruebas_1 | TOTAL                 1285   1278     1%
pruebas_1 | ----------------------------------------------------------------------
pruebas_1 | Ran 1 test in 0.100s
pruebas_1 | 
pruebas_1 | OK
```

As shown, the test passes without problems; the reason is that the value the sum has to return is being passed via mocking, regardless of the input data of the method being run.

You can see the code of the various files in the [gitlab repository on the mocking branch](http://gitlab.com/ecrespo/tutoriales-pruebas/tree/mocking).

##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
