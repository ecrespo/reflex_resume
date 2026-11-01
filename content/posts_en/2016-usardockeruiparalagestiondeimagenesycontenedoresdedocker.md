Title: Using dockerui to manage Docker images and containers  
Date: 2016-05-26 11:00  
Category: Tutorial de Docker  
Tags: Canaima,Debian,Linux,Ubuntu, Docker,Dockerui
lang: en
translation: true

Docker UI is a web interface that lets you manage Docker images and run containers.

The installation and use of dockerui will be explained.

This article is based on an English article that you can check at the following link.

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

14. [Creating a continuous Integration and Deployment environment with Docker for node.js.](/blog/crearunentornodeintegracionydespliguecontinuocondockerparanodejs)  

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

The installation process for Debian Jessie can be found in the first article, but if you use another distribution you can read the English link on which this article is based, which explains the installation for Fedora and other distros.

DockerUI can be downloaded as a Docker image; to run the container, execute the following command: 
```
docker run -d -p 9000:9000 --privileged -v /var/run/docker.sock:/var/run/docker.sock dockerui/dockerui
```
Note: The repository is on Docker Hub; another dockerui repository was used.
```
docker run -d -p 9000:9000 --privileged -v /var/run/docker.sock:/var/run/docker.sock abh1nav/dockerui
```
The web application runs on port 9000, is given all privileges, and accesses the docker socket running on the host machine. 


The main page of dockerui is shown below:


![](./images/usardockeruiparalagestiondeimagenesycontenedoresdedocker-1.png)

![](./images/usardockeruiparalagestiondeimagenesycontenedoresdedocker-2.png)


The images section lists all the images on the machine, and images can be removed from there:

![](./images/usardockeruiparalagestiondeimagenesycontenedoresdedocker-3.png)

Clicking on an image makes the create button appear:

![](./images/usardockeruiparalagestiondeimagenesycontenedoresdedocker-4.png)

Then a window appears where you define the command to run, the container name, how much memory and swap memory it will use, and the volume:

![](./images/usardockeruiparalagestiondeimagenesycontenedoresdedocker-5.png)

In the containers section you can start, restart, stop, kill or remove containers:

![](./images/usardockeruiparalagestiondeimagenesycontenedoresdedocker-6.png)


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
