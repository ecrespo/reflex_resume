Title: Install gitlab-runner for gitlab-ci through Docker
Date: 2016-06-13 11:00 
Category: Tutorial de Docker
Tags: Canaima,Linux,General,Python,Ubuntu,gitlab,gitlab-ci,Docker
lang: en
translation: true  

A previous article explained how to install gitlab-ce through Docker ([link](/blog/instalargitlabpormediodedocker)).


The problem is that gitlab still needs Continuous Integration (CI) configured; for that you need to install gitlab-runner (on the same machine, on another machine or as a separate container). 


You can see the description of gitlab-ci features at the following [link](https://about.gitlab.com/product/continuous-integration/).


You can check the guide for installing gitlab-runner at the following [link](https://gitlab.com/gitlab-org/gitlab-runner#installation).

For the docker case you can see the [following](https://about.gitlab.com/2016/05/23/gitlab-container-registry/) documentation.


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

28. [Analyzing python code with pylint from Docker](/blog/analizarcodigopythonconpylintdesdedocker)

The first thing to do is pull the Docker image for gitlab-runner:
```
docker pull gitlab/gitlab-runner
```
Then start the gitlab-runner registration service:
```
docker run -d --name gitlab-runner --restart always -v /srv/gitlab-runner/config:/etc/gitlab-runner -v /var/run/docker.sock:/var/run/docker.sock gitlab/gitlab-runner
```
This way gitlab-runner will use the docker on the host machine, and you have access to the gitlab-runner configuration from the host machine.

Running `docker ps` gives the following:
```
docker ps 
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS              PORTS                                                            NAMES
13ffb573fadf        gitlab/gitlab-runner      "/entrypoint run --us"   3 hours ago         Up 3 hours                                                                           gitlab-runner
b483b38fe29e        gitlab/gitlab-ce:latest   "/assets/wrapper"        12 days ago         Up 4 hours          0.0.0.0:22->22/tcp, 0.0.0.0:443->443/tcp, 0.0.0.0:9080->80/tcp   gitlab1
```
As you can see, gitlab-ce and gitlab-runner are now both active.

To register a project, run the following command on the machine:
```
docker exec -ti  13ffb573fadf  gitlab-runner register 
```
What comes next is registering a project that is in gitlab. In this case a project will be created in gitlab-ce and we go to its settings, where the runners section is selected:

We have the project `prueba-nodejs`:

![](./images/instalargitlabrunnerdegitlabcipormediodedocker-1.png)

The important data are:
```
URL:http://192.168.0.60:9080/ci
TOKEN:6kN_Uo_j2YitsJkh7q94
```
Next, run the register:
```
docker exec -ti  13ffb573fadf  gitlab-runner register 
```
And pass the data it asks for (the following figure shows the project registration configuration):

![](./images/instalargitlabrunnerdegitlabcipormediodedocker-2.png)

I passed the url, the token, then it asks for the project description, in this case `prueba-nodejs`, then some tags for it, docker will be used, and finally the base Docker image to use.

Finally, an image of the runner configuration is shown, which indicates that the runner and gitlab are connected:

![](./images/instalargitlabrunnerdegitlabcipormediodedocker-3.png)

And the information about that connection:

![](./images/instalargitlabrunnerdegitlabcipormediodedocker-4.png)

The next article will explain how to run a CI test. 

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
