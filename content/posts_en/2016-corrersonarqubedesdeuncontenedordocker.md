Title: Running sonarqube from a Docker container   
Date: 2016-07-08 09:00  
Category: Tutorial de Docker
Tags: Linux, Debian, Docker, Sonarqube, QA
lang: en
translation: true  


Continuing with the Docker articles, this time I show how to start SonarQube connected to a PostgreSQL database, passing the database settings through environment variables.

Sonarqube is a platform for evaluating source code ([taken from wikipedia](https://es.wikipedia.org/wiki/SonarQube)).  

The previous articles about Docker are:

1. [Installing Docker on Debian Jessie (broken link)](/blog/instalardockerendebianjessie)  

2. [Using Docker on Debian Jessie (part 1)](/blog/usodedockerendebianjessie-1)  

3. [Using Docker on Debian Jessie (part 2)](/blog/usodedockerendebianjessie-2)  

4. [Creating a Docker image from a Dockerfile (broken link)](/blog/crearunaimagendockerapartirdeunarchivodockerfile)  

5. [Starting Django using Docker (broken link)](/blog/iniciandodjangousandodocker)  

6. [Installing Gitlab with Docker (broken link)](/blog/instalargitlabpormediodedocker)  

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

17. [Running a unittest test in Python with a Docker container. (broken link)](/blog/ejecutarunapruebadeunittestenpythonconuncontenedordocker) 

18. [Setting up a Platform as a Service (PaaS) with Dokku (docker) (broken link)](/blog/montarunaplataformacomoserviciopaascondokkudocker).  

19. [Using docker-machine.   (broken link)](/blog/usodedockermachine)

20. [Provisioning a cluster with docker swarm and docker-machine. (broken link)](/blog/proveerunclustercondockerswarmydockermachine)

21. [Installing Jenkins with Docker and creating a Jenkins Docker image (broken link)](/blog/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins) 

22. [Automating the build of Docker images with github. (broken link)](/blog/automatizarlaconstrucciondeimagenesdockercongithub) 

23. [Creating a Docker image for MongoDB3. (broken link)](/blog/crearunaimagendockerparamongodb-3)

24. [Creating a Docker container as a development environment for Sails.js. (broken link)](/blog/crearuncontenedordockercomoentornodedesarrolloparasailsjs)

25. [Running desktop applications from a Docker container. (broken link)](/blog/correraplicacionesdeescritoriodesdeuncontenedordocker)

26. [Using dockerui to manage Docker images and containers (broken link)](/blog/usardockeruiparalagestiondeimagenesycontenedoresdedocker) 

27. [Creating a RethinkDB Docker image (broken link)](/blog/crearunaimagendockerderethinkdb)

28. [Analyzing python code with pylint from Docker (broken link)](/blog/analizarcodigopythonconpylintdesdedocker)

29. [Installing gitlab-runner for gitlab-ci with Docker (broken link)](/blog/ejecutarunapruebadeintegracioncontinuacongitlabciygitlabrunner)

30. [Creating JSON data from a dictionary in Flask (part 1) (update - Docker)](/blog/creardatosjsonapartirdeundiccionarioenflaskactualizaciondocker-1)

The configuration and usage guide for the sonarqube Docker containers can be seen at the [Docker hub](https://hub.docker.com/_/sonarqube/).

The first thing to do is start a postgreSQL container:
```
docker run -d --name postgres2 --restart always  -e POSTGRES_PASSWORD=sonar -e POSTGRES_USER=sonar postgres
```

The database user is defined as sonar and its password is sonar.


Now start the sonarqube container:
```
docker run -d --name sonarqube --restart always -p 9000:9000 -p 9092:9092 -e SONARQUBE_JDBC_USERNAME=sonar -e SONARQUBE_JDBC_PASSWORD=sonar -e SONARQUBE_JDBC_URL=jdbc:postgresql://postgres2/sonar --link postgres2:postgres sonarqube
```

The ports where sonarqube will be (9000 and 9092) are passed, the database configuration is passed to sonarqube (user, password and connection url, which will use the name of the postgres container) and it is linked to the postgres container.

Below is a screenshot of the container running:

![](./images/corrersonarqubedesdeuncontenedordocker-1.png)

Finally, the running containers are shown:
```
docker ps 
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS              PORTS                                                          NAMES
e20d4108f54f        sonarqube                 "./bin/run.sh"           29 minutes ago      Up 29 minutes       0.0.0.0:9092->9092/tcp, 0.0.0.0:49000->9000/tcp                sonarqube
e3387c2754d1        postgres                  "/docker-entrypoint.s"   6 hours ago         Up 6 hours          5432/tcp                                                       postgres2
```

##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)



