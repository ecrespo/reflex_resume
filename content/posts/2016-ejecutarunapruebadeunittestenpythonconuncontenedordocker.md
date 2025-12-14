Title: Ejecutar una prueba de unittest en Python con un contenedor Docker.  
Date: 2016-03-27 11:00  
Category: Tutorial Python  
Tags: Python,unittest,Docker  
lang: es  
translation: true

En este artículo prácticamente se hará lo mismo que el artículo [anterior (enlace roto)](/blog/ejecutarunapruebadedoctestconuncontenedordocker), pero se creará un archivo donde se define una clase la cual hará las pruebas unitarias.

La parte de pruebas unitarias se basa de un post anterior que se llama [Pruebas unitarias con unittest en Python (enlace roto)](/blog/pruebasunitariasenpythonconunittest).

Los artículos anteriores sobre docker son:  
1. [Instalar Docker en Debian Jessie (enlace roto)](/blog/instalardockerendebianjessie)  

2. [Uso de Docker en Debian Jessie (parte 1) (enlace roto)](https://www.seraph.to/uso-de-docker-en-debian-jessie-parte-1.html)  

3. [Uso de Docker en Debian Jessie (parte 2) (enlace roto)](https://www.seraph.to/uso-de-docker-en-debian-jessie-parte-2.html)  

4. [Crear una imagen Docker a partir de un archivo Dockerfile (enlace roto)](/blog/crearunaimagendockerapartirdeunarchivodockerfile)  

5. [Iniciando Django usando Docker (enlace roto)](/blog/iniciandodjangousandodocker)  

6. [Instalar Gitlab por medio de Docker (enlace roto)](/blog/instalargitlabpormediodedocker)  

7. [Ejecutando microservicios con docker usando docker-compose (enlace roto)](/blog/ejecutandomicrosservicioscondockerusandodockercompose)  

8. [Docker en Docker (DinD) (enlace roto)](/blog/dockerendockerdind)

9. [Iniciando Django con docker usando docker-compose con postgresql como microservicio. (enlace roto)](/blog/iniciandodjangocondockerusandodockercomposeconpostgresqlcomomicroservicio)

10. [Importar un contenedor Docker en Python. (enlace roto)](/blog/importaruncontenedordockerenpython) 

11. [Compartir imagenes Docker por medio de archivos tar (enlace roto)](/blog/compartirimagenesdockerpormediodearchivostar).

12. [Crear un registro de imagenes Docker privado. (enlace roto)](/blog/crearunregistrodeimagenesdockerprivado)

13. [Usar Anaconda desde un contenedor Docker. (enlace roto)](/blog/usaranacondadesdeuncontenedordocker)  

14. [Crear un entorno de Integración y Despligue continue con Docker para node.js. (enlace roto)](https://www.seraph.to/crear-un-entorno-de-integracion-y-despligue-continue-con-docker-para-nodejs.html#crear-un-entorno-de-integracion-y-despligue-continue-con-docker-para-nodejs)  

15. [Usar Jupyter Notebook desde un contenedor Docker. (enlace roto)](/blog/usarjupyternotebookdesdeuncontenedordedocker)  

16. [Ejecutar una prueba de doctest con un contenedor Docker (enlace roto)](/blog/ejecutarunapruebadedoctestconuncontenedordocker).

Ahora se tendrán los siguientes archivos en el directorio `pruebas-doctest`:
```
pruebas-doctest
├── Dockerfile
├── raizcuadrada.py
├── raizcuadrada_test.py
└── raizcuadrada.txt
```
El Dockerfile, `raizcuadrada.py` y `raizcuadrada.txt` son los mismos del artículo [anterior (enlace roto)](http://blog.crespo.org.ve/2016/03/ejecutar-una-prueba-de-doctest-con-un.html).

El archivo `raizcuadrada_test.py` tiene lo siguiente:
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
Ahora se reconstruye  la imagen de Docker:
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
Y se ejecuta la prueba:
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
Está primera prueba se preparó para que fallara, ahora se comenta el método de prueba negativa, se reconstruye la imagen y se vuelve a ejecutar:
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


Se ejecutaron 2 test y pasaron. 

Ya con esta imagen de Docker se puede reusar en varios computadores teniendo el mismo ambiente de desarrollo. 


##  ##
¡Haz tu donativo!
Si te gustó el artículo puedes realizar un donativo con Bitcoin (BTC)
usando la billetera digital de tu preferencia a la siguiente
dirección: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

O Escaneando el código QR desde la billetera:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
