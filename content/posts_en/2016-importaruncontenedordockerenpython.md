Title: Importing a Docker container in Python.
Date: 2016-02-24 09:00  
Category: Tutorial de Docker 
Tags: Linux,Python, Docker  
lang: en  
translation: true  

![](./images/importaruncontenedordockerenpython-1.png)

The previous articles about Docker have covered image handling; now we will explain how to import a container from Python. This article is based on the [following article in English](https://blog.deepgram.com/import-a-docker-container-in-python/).

1. [Installing Docker on Debian Jessie](/blog/instalardockerendebianjessie)  
2. [Using Docker on Debian Jessie (part 1)](/blog/usodedockerendebianjessie-1)  
3. [Using Docker on Debian Jessie (part 2)](/blog/usodedockerendebianjessie-2)  
4. [Creating a Docker image from a Dockerfile](/blog/crearunaimagendockerapartirdeunarchivodockerfile)  
5. [Starting Django using Docker](/blog/iniciandodjangousandodocker)  
6. [Installing Gitlab through Docker](/blog/instalargitlabpormediodedocker)  
7. [Running microservices with docker using docker-compose](/blog/ejecutandomicrosservicioscondockerusandodockercompose)  
8. [Docker in Docker (DinD)](/blog/dockerendockerdind)
9. [Starting Django with docker using docker-compose with postgresql as a microservice.](/blog/iniciandodjangocondockerusandodockercomposeconpostgresqlcomomicroservicio)

There is the [Sidomo](https://github.com/deepgram/sidomo) module, which lets you manage containers.

To install `sidomo`, run the `pip` command:
```
pip install -e git+https://github.com/deepgram/sidomo.git#egg=sidomo
```
Download the Ubuntu Docker image:
```
docker pull ubuntu
```
The example code from the `sidomo` site is at the following [link](https://github.com/deepgram/sidomo/blob/master/examples/hello_world.py).


The modified code is the following:

```python
#!/usr/bin/env python

from sidomo import Container

def say_hello(to):


    """Just say it."""


    with Container(


        'ubuntu',


        stderr=False


    ) as c:


        for line in c.run(


            'echo Hola Mundo  %s' % to


        ):


            yield line



if __name__ == '__main__':


    for line in say_hello("desde un contenedor Docker"):


        print line

```


Running the code gives:
```python
python ejemplo.py 
Hola Mundo desde un contenedor Docker
```

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
