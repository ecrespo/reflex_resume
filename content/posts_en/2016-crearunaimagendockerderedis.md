Title: Creating a Redis Docker image 
Date: 2016-07-16 11:00
Category: Tutorial de Docker
Tags: Linux,Python,Ubuntu,Docker, Redis
lang: en
translation: true

Redis is an in-memory database engine based on hash table (key/value) storage ([taken from wikipedia](https://es.wikipedia.org/wiki/Redis)).

This article builds the Redis image from a Debian base image; it is based on an [article in English on the Docker site (broken link)](https://docs.docker.com/engine/examples/running_redis_service/). 

To push the image to docker hub, follow the article on [using docker on debian jessie part 1](/blog/usodedockerendebianjessie-1).

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

27. [Creating a RethinkDB Docker image](/blog/crearunaimagendockerderethinkdb)

28. [Analyzing python code with pylint from Docker](/blog/analizarcodigopythonconpylintdesdedocker)

29. [Installing gitlab-runner for gitlab-ci through Docker](/blog/ejecutarunapruebadeintegracioncontinuacongitlabciygitlabrunner)

30. [Creating JSON data from a dictionary in Flask (part 1) (update - Docker)](/blog/creardatosjsonapartirdeundiccionarioenflaskactualizaciondocker-1)

31. [Running sonarqube from a Docker container](/blog/corrersonarqubedesdeuncontenedordocker)


The `Dockerfile` will contain the following:
```
#Se usa debian como imagen base
FROM debian
#Se define el mantenedor de la imagen
MAINTAINER Ernesto Crespo <ecrespo@gmail.com>
#Se actualiza la lista de paquetes
RUN apt-get update
#Se instala redis-server y redis-tools
RUN apt-get install -y redis-server redis-tools 
#Se limpia la cache de paquetes deb
RUN apt-get clean

#Se expone el puerto 6379
EXPOSE      6379
#Inicio del servicio redis
ENTRYPOINT  ["/usr/bin/redis-server"]
```

Now build the image (tying it to my docker hub account):
```
docker build -t ecrespo/redis .
```
List the images: 
```
docker images 
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ecrespo/redis       latest              841b6e9266f8        3 minutes ago       136.9 MB
redis               latest              4465e4bcad80        4 weeks ago         185.7 MB
debian              latest              1b088884749b        5 weeks ago         125.1 MB
```

Run the service by executing:
```
docker run --name redis -d --restart always -p 6379:6379 ecrespo/redis 
```

Listing the processes shows redis running:
```
docker ps 
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
0af1cdf134d7        ecrespo/redis       "/usr/bin/redis-serve"   9 seconds ago       Up 4 seconds        0.0.0.0:6379->6379/tcp   redis
```
To test redis, install `redis-tools` on the computer:
```
#apt-get install redis-tools
```
From the command line run `redis-cli`; a figure of the example is shown below: 

![](./images/crearunaimagendockerderedis-1.png)

Make a commit of the running redis container:
```
docker commit 0af1cdf134d7 ecrespo/redis
```
Then push it to docker hub:
```
docker push   ecrespo/redis
```

Now a container for the application will be created, linking the redis container with the client container: 
```
docker run --link redis:db -i -t debian /bin/bash
```
Inside the container run the following commands:
```
apt-get update  
apt-get install redis-tools  
service redis-server stop  
```
Since the current container was linked with the redis container, it contains some environment variables; to view them run the following command:
```
env | grep DB_
DB_NAME=/tiny_poincare/db
DB_PORT_6379_TCP_PORT=6379
DB_PORT=tcp://172.17.0.2:6379
DB_PORT_6379_TCP=tcp://172.17.0.2:6379
DB_PORT_6379_TCP_ADDR=172.17.0.2
DB_PORT_6379_TCP_PROTO=tcp
```

To connect from the container running Debian to the redis one, run:
```
redis-cli -h $DB_PORT_6379_TCP_ADDR
172.17.0.2:6379> set docker "Conectandose desde un contenedor debian al contenedor redis"
OK
172.17.0.2:6379> get docker
"Conectandose desde un contenedor debian al contenedor redis"
172.17.0.2:6379> 
```
A figure of the execution is shown below:

![](./images/crearunaimagendockerderedis-2.png)


And the running containers are listed:

![](./images/crearunaimagendockerderedis-3.png)


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)


