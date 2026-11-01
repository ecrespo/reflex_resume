Title: Automating the building of Docker images with github  
Date: 2016-05-11 09:00
Category: Linux,Desarrollo    
Tags: Canaima,Debian,Linux,Ubuntu,Docker, Github,CI/CD,DevOps
lang: en
translation: true


This article explains how to build a Docker image automatically using github with the docker hub.

This article is based on the existing documentation on the docker hub site for [automated builds.](https://docs.docker.com/docker-hub/builds/link-source/)

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

14. [Creating a continuous Integration and Deployment environment with Docker for node.js.](/blog/crearunentornodeintegracionydespliguecontinuocondockerparanodejs)  

15. [Using Jupyter Notebook from a Docker container.](/blog/usarjupyternotebookdesdeuncontenedordedocker)  

16. [Running a doctest test with a Docker container](/blog/ejecutarunapruebadedoctestconuncontenedordocker).

17. [Running a unittest test in Python with a Docker container.](/blog/ejecutarunapruebadeunittestenpythonconuncontenedordocker) 

18. [Setting up a Platform as a Service (PaaS) with Dokku (docker)](/blog/montarunaplataformacomoserviciopaascondokkudocker).  

19. [Using docker-machine.  ](/blog/usodedockermachine)

20. [Provisioning a cluster with docker swarm and docker-machine.](/blog/proveerunclustercondockerswarmydockermachine)

21. [Installing Jenkins through Docker and creating a Jenkins Docker image](/blog/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins) 

The first thing to do is go to your account on [docker hub](https://hub.docker.com/), click on linked accounts and services, and there select github, as the figure shows:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-1.png)


Selecting github takes you to the part of the github account where you grant permissions:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-2.png)

After accepting, the linked account will appear:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-3.png)


Now, in github, go to the settings of the repository you want to link, to the webhooks and services section as the figure shows:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-4.png)

Add the Docker service:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-5.png)

Test the service:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-6.png)

As can be seen, the configuration passes the test.

From now on, every time a git push is made to github, docker hub takes care of updating the image.

To finish, the content of the jenkins Dockerfile and the content of the updated github repository are shown:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-7.png)

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-8.png)




##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
