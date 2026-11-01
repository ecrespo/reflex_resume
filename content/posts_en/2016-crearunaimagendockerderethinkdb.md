Title: Creating a Docker image for RethinkDB  
Date: 2016-06-10 09:00   
Category: Tutorial de Docker
Tags: Canaima,Linux,Python,Ubuntu,Docker, RethinkDB
lang: en
translation: true   

RethinkDB is an open source NoSQL database that stores documents in JSON format and makes real-time insertion, updating and searching easy (more info on the [rethinkDB](https://www.rethinkdb.com/) site and on [wikipedia](https://en.wikipedia.org/wiki/RethinkDB)).

The idea is to build a Docker image through a Dockerfile, using Debian Jessie as the base. Although you can directly use the RethinkDB image found on the [docker hub](https://hub.docker.com/_/rethinkdb/).

The previous articles about Docker are:

1. [Installing Docker on Debian Jessie](/blog/instalardockerendebianjessie)  

2. [Using Docker on Debian Jessie (part 1)](/blog/usodedockerendebianjessie-1)  

3. [Using Docker on Debian Jessie (part 2)](/blog/usodedockerendebianjessie-2)  

4. [Creating a Docker image from a Dockerfile](/blog/crearunaimagendockerapartirdeunarchivodockerfile)  

5. [Starting Django using Docker](/blog/iniciandodjangousandodocker)  

6. [Installing Gitlab through Docker](/blog/instalargitlabpormediodedocker)  

7. [Running microservices with docker using docker-compose](/blog/ejecutandomicrosservicioscondockerusandodockercompose)  

8. [Docker in Docker (DinD)](/blog/dockerendockerdind)

9. [Starting Django with docker using docker-compose with postgresql as a microservice.](/blog/iniciandodjangocondockerusandodockercomposeconpostgresqlcomomicroservicio)

10. [Importing a Docker container in Python.](/blog/importaruncontenedordockerenpython) 

11. [Sharing Docker images through tar files](/blog/compartirimagenesdockerpormediodearchivostar).

12. [Creating a private Docker image registry.](/blog/crearunregistrodeimagenesdockerprivado)

13. [Using Anaconda from a Docker container.](/blog/usaranacondadesdeuncontenedordocker)  

14. [Creating a Continuous Integration and Deployment environment with Docker for node.js.](/blog/crearunentornodeintegracionydespliguecontinuocondockerparanodejs)  

15. [Using Jupyter Notebook from a Docker container.](/blog/usarjupyternotebookdesdeuncontenedordedocker)  

16. [Running a doctest test with a Docker container](/blog/ejecutarunapruebadedoctestconuncontenedordocker).

17. [Running a unittest test in Python with a Docker container.](/blog/ejecutarunapruebadeunittestenpythonconuncontenedordocker) 

18. [Setting up a Platform as a Service (PaaS) with Dokku (docker)](/blog/montarunaplataformacomoserviciopaascondokkudocker).  

19. [Using docker-machine.  ](/blog/usodedockermachine)

20. [Provisioning a cluster with docker swarm and docker-machine.](/blog/proveerunclustercondockerswarmydockermachine)

21. [Installing Jenkins through Docker and creating a Jenkins Docker image](/blog/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins) 

22. [Automating the building of Docker images with github.](/blog/automatizarlaconstrucciondeimagenesdockercongithub) 

23. [Creating a Docker image for MongoDB3.](/blog/crearunaimagendockerparamongodb-3)

24. [Creating a Docker container as a development environment for Sails.js.](/blog/crearuncontenedordockercomoentornodedesarrolloparasailsjs)

25. [Running desktop applications from a Docker container.](/blog/correraplicacionesdeescritoriodesdeuncontenedordocker)

26. [Using dockerui to manage Docker images and containers](/blog/usardockeruiparalagestiondeimagenesycontenedoresdedocker) 

The Dockerfile takes part of the official file from the RethinkDB site; the idea is to create the image from Debian Jessie (you can see the dockerfile at the following [link](https://github.com/rethinkdb/rethinkdb-dockerfiles/blob/d129775a6b33cb9e9a3ced40edda31ba9016a647/jessie/2.3.4/Dockerfile)). 

The `Dockerfile` file is the following:
```
#Base de Debian Jessie
FROM debian
#Mantenedor
MAINTAINER Ernesto Crespo <ecrespo@gmail.com>


# instalar RethinkDB
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get install -y wget 
RUN sh -c 'echo "deb http://download.rethinkdb.com/apt `lsb_release -cs` main" | tee /etc/apt/sources.list.d/rethinkdb.list'
RUN sh -c 'wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | apt-key add -'
RUN apt-get update
RUN apt-get install -y rethinkdb

#Se define el volumen donde se almacena los datos
VOLUME ["/data"]

#Se define el directorio de trabajo
WORKDIR /data

#Se ejecuta rethinkdb asociando todas las interfaces existentes en el contenedor
CMD ["rethinkdb", "--bind", "all"]

#   proceso, cluster webui
EXPOSE 28015 29015 8080
```

To build the image, run:
```
docker build -t debian-rethinkdb . 
```
And to run the container (the `/data` volume is bound to the directory where the container is run):
```
docker run --name some-rethink -v "$PWD:/data" -d debian-rethinkdb
```
To see the rethingDB web administration interface, run (chromium case):
```
chromium "http://$(docker inspect --format  '{{ .NetworkSettings.IPAddress }}' some-rethink):8080"
```
A screenshot of the web application is shown below:

![](./images/crearunaimagendockerderethinkdb-1.png)

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)



