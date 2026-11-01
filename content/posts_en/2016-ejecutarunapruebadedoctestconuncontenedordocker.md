Title: Run a doctest test with a Docker container.   
Date: 2016-03-27 10:00  
Category: Tutorial Python  
Tags: Python, Docker, Jupyter Notebook, DevOps, Doctest  
lang: en
translation: true  

Now I will show how to use a Docker container to run doctest tests; this article is based on a previous blog post called [Separating test code from the documentation (doctest, part 2)](/blog/separarcodigodepruebasdeladocumentaciondoctest2).

The previous articles about docker are:  
1. [Install Docker on Debian Jessie](/blog/instalardockerendebianjessie)  

2. [Using Docker on Debian Jessie (part 1)](/blog/usodedockerendebianjessie-1)  

3. [Using Docker on Debian Jessie (part 2)](/blog/usodedockerendebianjessie-2)  

4. [Create a Docker image from a Dockerfile](/blog/crearunaimagendockerapartirdeunarchivodockerfile)  

5. [Starting Django using Docker](/blog/iniciandodjangousandodocker)  

6. [Install Gitlab through Docker](/blog/instalargitlabpormediodedocker)  

7. [Running microservices with docker using docker-compose](/blog/ejecutandomicrosservicioscondockerusandodockercompose)  

8. [Docker in Docker (DinD)](/blog/dockerendockerdind)

9. [Starting Django with docker using docker-compose with postgresql as a microservice.](/blog/iniciandodjangocondockerusandodockercomposeconpostgresqlcomomicroservicio)

10. [Import a Docker container in Python.](/blog/importaruncontenedordockerenpython) 

11. [Share Docker images through tar files](/blog/compartirimagenesdockerpormediodearchivostar).

12. [Create a private Docker image registry.](/blog/crearunregistrodeimagenesdockerprivado)

13. [Use Anaconda from a Docker container.](/blog/usaranacondadesdeuncontenedordocker)  

14. [Create a Continuous Integration and Deployment environment with Docker for node.js.](/blog/crearunentornodeintegracionydespliguecontinuocondockerparanodejs)  

15. [Use Jupyter Notebook from a Docker container.](/blog/usarjupyternotebookdesdeuncontenedordedocker)  


There will be 3 files in a directory called `pruebas-doctest` with the following:
```
pruebas-doctest
├── Dockerfile
├── raizcuadrada.py
└── raizcuadrada.txt
```
The `Dockerfile` will contain the following:
```
FROM python:3.4
MAINTAINER Ernesto Crespo

WORKDIR /app
COPY . /app
```
Python 3.4 will be used, the maintainer is Ernesto Crespo, the working directory will be app and everything in the directory will be copied to the working directory.

The `raizcuadrada.py` file has the following:

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


    import doctest


    #Se realiza la prueba al archivo raizcuadra.txt


    doctest.testfile("raizcuadrada.txt")


```


And the last of the files is `raizcuadrada.txt`, which will have the doctest tests:

```python


Modulo raiz cuadrada


=====================


Usando  'raizcuadrada'


------------------------------


Primero se importa la función:





>>> from raizcuadrada import Raiz





Ejemplos de calculo de raiz cuadrada:





>>> Raiz(4)


2.0





>>> Raiz(9)


3.0





>>> Raiz(25)


5.0





>>> Raiz(0)


0.0





>>> Raiz(16)


5.0





>>> Raiz(-1)


Traceback (most recent call last):


...


ValueError: a debe ser >= 0

```


The file has an intentional error in the square root of 16, which should give 4, and it says 5.


Now build the image named `pruebas-doctest`:
```
docker build -t pruebas-doctest .
Sending build context to Docker daemon  5.12 kB
Step 1 : FROM python:3.4
3.4: Pulling from library/python
fdd5d7827f33: Downloading 11.35 MB
fdd5d7827f33: Pull complete 
a3ed95caeb02: Pull complete 
0f35d0fe50cc: Pull complete 
7b40647e93b7: Pull complete 
ce5207842c4c: Pull complete 
da7994e536a7: Pull complete 
09482b8dda8a: Pull complete 
5ba79222c836: Pull complete 
Digest: sha256:8bcba46a3dbf4803c80074c0e543d98eeb3cb4f9cc35ff52f88c53cc0a1c30c3
Status: Downloaded newer image for python:3.4
 ---> c40d327867e9
Step 2 : MAINTAINER Ernesto Crespo
 ---> Running in de81df2565f3
 ---> 3b1aced33b5e
Removing intermediate container de81df2565f3
Step 3 : WORKDIR /app
 ---> Running in f1901c2490d7
 ---> 7dd09842cf61
Removing intermediate container f1901c2490d7
Step 4 : COPY . /app
 ---> 788ad6d153ed
Removing intermediate container b32ba65862d9
Successfully built 788ad6d153ed
```

Now run the test by passing `python -m doctest -v raizcuadrada.txt`:
```
docker run pruebas-doctest python -m doctest -v raizcuadrada.txt
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
    Raiz(16)
Expecting:
    5.0
**********************************************************************
File "raizcuadrada.txt", line 23, in raizcuadrada.txt
Failed example:
    Raiz(16)
Expected:
    5.0
Got:
    4.0
Trying:
    Raiz(-1)
Expecting:
    Traceback (most recent call last):
    ...
    ValueError: a debe ser >= 0
ok
**********************************************************************
1 items had failures:
   1 of   7 in raizcuadrada.txt
7 tests in 1 items.
6 passed and 1 failed.
***Test Failed*** 1 failures.
```

The result is that 6 tests passed and one did not; fix the value it should return in the `raizcuadrada.txt` file and run the build and execution again:
```
docker build -t pruebas-doctest .
Sending build context to Docker daemon 4.608 kB
Step 1 : FROM python:3.4
 ---> c40d327867e9
Step 2 : MAINTAINER Ernesto Crespo
 ---> Using cache
 ---> 3b1aced33b5e
Step 3 : WORKDIR /app
 ---> Using cache
 ---> 7dd09842cf61
Step 4 : COPY . /app
 ---> 47a9b0467413
Removing intermediate container 8a375d3abc0c
Successfully built 47a9b0467413

docker run pruebas-doctest python -m doctest -v raizcuadrada.txt
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
    Raiz(16)
Expecting:
    4.0
ok
Trying:
    Raiz(-1)
Expecting:
    Traceback (most recent call last):
    ...
    ValueError: a debe ser >= 0
ok
1 items passed all tests:
   7 tests in raizcuadrada.txt
7 tests in 1 items.
7 passed and 0 failed.
Test passed.
```

Now all the doctest tests have passed.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
