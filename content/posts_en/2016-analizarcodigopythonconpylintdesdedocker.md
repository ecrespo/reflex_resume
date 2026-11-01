Title: Analyzing python code with pylint from Docker  
Date: 2016-06-12 09:00  
Category: Tutorial de Docker
Tags: Canaima,Linux,Python,Ubuntu,pylint,Docker 
lang: en
translation: true  


Some time ago I wrote an article about [analyzing python code with pylint](/blog/analizandocodigopythonconpylint).

In this case, the article on [unit tests with Docker](/blog/ejecutarunapruebadeunittestenpythonconuncontenedordocker) and the pylint one will be combined to show how to run python code analysis with Docker.


The previous articles about Docker are:

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

16. [Run a doctest test with a Docker container](/blog/ejecutarunapruebadedoctestconuncontenedordocker).

17. [Run a unittest test in Python with a Docker container.](/blog/ejecutarunapruebadeunittestenpythonconuncontenedordocker) 

18. [Set up a Platform as a Service (PaaS) with Dokku (docker)](/blog/montarunaplataformacomoserviciopaascondokkudocker).  

19. [Using docker-machine.  ](/blog/usodedockermachine)

20. [Provision a cluster with docker swarm and docker-machine.](/blog/proveerunclustercondockerswarmydockermachine)

21. [Install Jenkins through Docker and create a Jenkins Docker image](/blog/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins) 

22. [Automate building Docker images with github.](/blog/automatizarlaconstrucciondeimagenesdockercongithub) 

23. [Create a Docker image for MongoDB3.](/blog/crearunaimagendockerparamongodb-3)

24. [Create a Docker container as a development environment for Sails.js.](/blog/crearuncontenedordockercomoentornodedesarrolloparasailsjs)

25. [Run desktop applications from a Docker container.](/blog/correraplicacionesdeescritoriodesdeuncontenedordocker)

26. [Use dockerui to manage Docker images and containers](/blog/usardockeruiparalagestiondeimagenesycontenedoresdedocker) 

27. [Create a RethinkDB Docker image](/blog/crearunaimagendockerderethinkdb)

The `Dockerfile` changed a bit compared to the one used for the unit tests: now Debian will be used as the base, pylint will be installed through apt-get, and everything else stays the same as in the unit tests article. 

Here is the `Dockerfile`:
```
FROM debian
MAINTAINER Ernesto Crespo

RUN apt-get update 
RUN apt-get install -y pylint
RUN apt-get clean 

WORKDIR /app
COPY . /app
```

The files used are the same ones used in the unit tests article, found in the [github](https://github.com/ecrespo/raizcuadrada) repository.
```
raizcuadrada
├── Dockerfile
├── LICENSE
├── raizcuadrada.py
├── raizcuadrada_test.py
└── README.md
```

The `raizcuadrada.py` module has the following:

```
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
The Docker image is built with the following command:
```
docker build -t prueba-python .
```
To run the analysis from docker, run:
```
docker run  -v "$PWD:/app" -ti prueba-python  pylint raizcuadrada.py
```
And the result is the following:

```

docker run  -v "$PWD:/app" -ti prueba-python  pylint raizcuadrada.py



No config file found, using default configuration



************* Module raizcuadrada


C: 16, 0: Line too long (101/80) (line-too-long)


C: 12, 0: Invalid function name "Raiz" (invalid-name)


C: 12, 0: Invalid argument name "a" (invalid-name)


Report


======


9 statements analysed.





Messages by category


--------------------





+-----------+-------+---------+-----------+


|type       |number |previous |difference |


+===========+=======+=========+===========+


|convention |3      |NC       |NC         |


+-----------+-------+---------+-----------+


|refactor   |0      |NC       |NC         |


+-----------+-------+---------+-----------+


|warning    |0      |NC       |NC         |


+-----------+-------+---------+-----------+


|error      |0      |NC       |NC         |


+-----------+-------+---------+-----------+



Messages


--------





+--------------+------------+


|message id    |occurrences |


+==============+============+


|invalid-name  |2           |


+--------------+------------+


|line-too-long |1           |


+--------------+------------+



Global evaluation


-----------------


Your code has been rated at 6.67/10





Raw metrics


-----------





+----------+-------+------+---------+-----------+


|type      |number |%     |previous |difference |


+==========+=======+======+=========+===========+


|code      |9      |36.00 |NC       |NC         |


+----------+-------+------+---------+-----------+


|docstring |4      |16.00 |NC       |NC         |


+----------+-------+------+---------+-----------+


|comment   |3      |12.00 |NC       |NC         |


+----------+-------+------+---------+-----------+


|empty     |9      |36.00 |NC       |NC         |


+----------+-------+------+---------+-----------+

Statistics by type


------------------



+---------+-------+-----------+-----------+------------+---------+


|type     |number |old number |difference |%documented |%badname |


+=========+=======+===========+===========+============+=========+


|module   |1      |NC         |NC         |100.00      |0.00     |


+---------+-------+-----------+-----------+------------+---------+


|class    |0      |NC         |NC         |0           |0        |


+---------+-------+-----------+-----------+------------+---------+


|method   |0      |NC         |NC         |0           |0        |


+---------+-------+-----------+-----------+------------+---------+


|function |1      |NC         |NC         |100.00      |100.00   |


+---------+-------+-----------+-----------+------------+---------+


Duplication


-----------



+-------------------------+------+---------+-----------+


|                         |now   |previous |difference |


+=========================+======+=========+===========+


|nb duplicated lines      |0     |NC       |NC         |


+-------------------------+------+---------+-----------+


|percent duplicated lines |0.000 |NC       |NC         |


+-------------------------+------+---------+-----------

```

This is how python code analysis with pylint can be run using Docker.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)

