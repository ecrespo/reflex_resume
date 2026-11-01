Title: Running a unittest test in Python with a Docker container.  
Date: 2016-03-27 11:00  
Category: Tutorial Python  
Tags: Python,unittest,Docker  
lang: en
translation: true

This article will do practically the same as the [previous (broken link)](/blog/ejecutarunapruebadedoctestconuncontenedordocker) article, but a file will be created that defines a class that will run the unit tests.

The unit testing part is based on a previous post called [Unit tests with unittest in Python (broken link)](/blog/pruebasunitariasenpythonconunittest).

The previous articles about docker are:  
1. [Installing Docker on Debian Jessie (broken link)](/blog/instalardockerendebianjessie)  

2. [Using Docker on Debian Jessie (part 1)](/blog/usodedockerendebianjessie-1)  

3. [Using Docker on Debian Jessie (part 2)](/blog/usodedockerendebianjessie-2)  

4. [Creating a Docker image from a Dockerfile (broken link)](/blog/crearunaimagendockerapartirdeunarchivodockerfile)  

5. [Starting Django using Docker (broken link)](/blog/iniciandodjangousandodocker)  

6. [Installing Gitlab through Docker (broken link)](/blog/instalargitlabpormediodedocker)  

7. [Running microservices with docker using docker-compose (broken link)](/blog/ejecutandomicrosservicioscondockerusandodockercompose)  

8. [Docker in Docker (DinD) (broken link)](/blog/dockerendockerdind)

9. [Starting Django with docker using docker-compose with postgresql as a microservice. (broken link)](/blog/iniciandodjangocondockerusandodockercomposeconpostgresqlcomomicroservicio)

10. [Importing a Docker container in Python. (broken link)](/blog/importaruncontenedordockerenpython) 

11. [Sharing Docker images through tar files (broken link)](/blog/compartirimagenesdockerpormediodearchivostar).

12. [Creating a private Docker image registry. (broken link)](/blog/crearunregistrodeimagenesdockerprivado)

13. [Using Anaconda from a Docker container. (broken link)](/blog/usaranacondadesdeuncontenedordocker)  

14. [Creating a Continuous Integration and Deployment environment with Docker for node.js.](/blog/crearunentornodeintegracionydespliguecontinuocondockerparanodejs)  

15. [Using Jupyter Notebook from a Docker container. (broken link)](/blog/usarjupyternotebookdesdeuncontenedordedocker)  

16. [Running a doctest test with a Docker container (broken link)](/blog/ejecutarunapruebadedoctestconuncontenedordocker).

Now you will have the following files in the `pruebas-doctest` directory:
```
pruebas-doctest
├── Dockerfile
├── raizcuadrada.py
├── raizcuadrada_test.py
└── raizcuadrada.txt
```
The Dockerfile, `raizcuadrada.py` and `raizcuadrada.txt` are the same as in the [previous](/blog/ejecutarunapruebadedoctestconuncontenedordocker) article.

The `raizcuadrada_test.py` file has the following:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Se importa el módulo unittest y math
import unittest
#Se importa la funcion Raiz del modulo raizcuadrada
from raizcuadrada import Raiz

class RaizTest(unittest.TestCase):

    def test_Raiz(self):
        """Test para la raiz de nueve que devuelve 3 que debe pasar."""
        self.assertEqual(3, Raiz(9))

    def test_zero(self):
        """Test para la raiz de 0 que devuelve 0, que debe pasar."""
        self.assertEqual(0, Raiz(0))

        
    def test_negative(self):
        """Test para la raiz de un número negativo, que debe fallar."""
        # Este debe devolver un ValueError, pero se espera un IndexError.
        self.assertRaises(IndexError, Raiz(-10))


if __name__ == '__main__':
    #Se ejecuta la prueba unitaria
    unittest.main()

```
Now rebuild the Docker image:
```
docker build -t pruebas-doctest .
Sending build context to Docker daemon  7.68 kB
Step 1 : FROM python:3.4
 ---> c40d327867e9
Step 2 : MAINTAINER Ernesto Crespo
 ---> Using cache
 ---> 3b1aced33b5e
Step 3 : WORKDIR /app
 ---> Using cache
 ---> 7dd09842cf61
Step 4 : COPY . /app
 ---> 842cd3bd051f
Removing intermediate container 140eaaf7935f
Successfully built 842cd3bd051f

```
And run the test:
```
docker run pruebas-doctest python raizcuadrada_test.py
.E.
======================================================================
ERROR: test_negative (__main__.RaizTest)
Test para la raiz de un número negativo, que debe fallar.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "raizcuadrada_test.py", line 25, in test_negative
    self.assertRaises(IndexError, Raiz(-10))
  File "/app/raizcuadrada.py", line 22, in Raiz
    raise ValueError("a debe ser >= 0")
ValueError: a debe ser >= 0

----------------------------------------------------------------------
Ran 3 tests in 0.002s

FAILED (errors=1)

```
This first test was set up to fail. Now the negative test method is commented out, the image is rebuilt and it is run again:
```
docker build -t pruebas-doctest .
Sending build context to Docker daemon  7.68 kB
Step 1 : FROM python:3.4
 ---> c40d327867e9
Step 2 : MAINTAINER Ernesto Crespo
 ---> Using cache
 ---> 3b1aced33b5e
Step 3 : WORKDIR /app
 ---> Using cache
 ---> 7dd09842cf61
Step 4 : COPY . /app
 ---> 609702415974
Removing intermediate container e2174beb4f7c
Successfully built 609702415974

docker run pruebas-doctest python raizcuadrada_test.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK

```

![](./images/ejecutarunapruebadeunittestenpythonconuncontenedordocker-1.png)


2 tests were run and they passed. 

This Docker image can now be reused on several computers, keeping the same development environment. 


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
