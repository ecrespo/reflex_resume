Title: Installing Docker on Debian Jessie
Date: 2015-12-25 8:00
Category: Tutorial Linux
Tags: canaima,Debian,Linux,Ubuntu,Docker
lang: en
translation: true

A while ago I had to teach a Debian packaging course and a colleague prepared a Virtualbox virtual machine with [vagrant](https://www.vagrantup.com/) (you can check a tutorial at the following [link](https://styde.net/como-crear-un-entorno-de-desarrollo-virtual-con-vagrant/)).

At one point we broke some packages and quickly restored the image to continue with the course.

In my case, since my personal machine cannot handle several virtual machines with virtualbox, I preferred to move to container technology with [Docker](https://www.docker.com/). [You can check wikipedia to learn more about docker. (broken link)](https://es.wikipedia.org/wiki/Docker_(software))

The installation guide for Debian Jessie in English can be found at the following [link](https://docs.docker.com/config/daemon/); and the user guide at the following [link](https://docs.docker.com/config/daemon/). The repository where images are hosted can be checked at this [link](https://hub.docker.com/).

0. Install https support for the repositories:
```
#apt-get install apt-transport-https
```
1. Remove old or lxc packages:
```
#apt-get purge lxc-docker*
#apt-get purge docker.io*
```
2. Add the docker.io gpg key:
```
#apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys  58118E89F3A912897C070ADBF76221572C52609D
```
3. Add the repository to `sources.list.d`:
```
vim /etc/apt/sources.list.d/docker.list

deb https://apt.dockerproject.org/repo debian-jessie main

```
4. Update the repository list:
```
#apt-get update
```
5. Verify that the package is downloaded from the correct repository:
```
#apt-cache policy docker-engine
```
6. Install docker:
```
#apt-get install docker-engine
```
7. Start the docker daemon:
```
#service docker start
```
8. Verify that it was installed correctly:
```
# docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
b901d36b6f2f: Pull complete
0a6ba66e537a: Pull complete
Digest: sha256:8be990ef2aeb16dbcb9271ddfe2610fa6658d13f6dfb8bc72074cc1ca36966a7
Status: Downloaded newer image for hello-world:latest

Hello from Docker.
This message shows that your installation appears to be working correctly.
```
9. Give non-root users access to docker:

9.1 Add the docker group if it does not exist:
```
$sudo groupadd docker
```
9.2 Add the user to the docker group:
```
$ sudo gpasswd -a ${USER} docker
```
9.3 Restart the docker daemon:
```
$sudo service docker restart
```
In upcoming articles I will show how to use docker, how to create images and, finally, an environment for packaging for Debian will be created.
I will leave the references here to use them in the future:


1. [Installing docker on Debian.](https://docs.docker.com/install/linux/docker-ce/debian/)    
2. [Packaging with docker.](https://wiki.debian.org/PackagingWithDocker?highlight=%28%28Docker%29%29)  
3. [Docker intro and installation.](https://wiki.debian.org/PackagingWithDocker?highlight=%28%28Docker%29%29)  
4. [Docker image building.](https://docs.google.com/document/d/1f8iflnFSZxAU9FhoLQPEVlSKhVPXbtCaqTVPTTJb9yo/edit)  
5. [Docker Advanced volumes.](https://docs.google.com/document/d/1tgzbbc76tV82nxJCpHTSb-Y5tns8Uim8sLDExy12e5k/edit)  
6. [Debian/Ubuntu Package Developing with Docker.](https://sfxpt.wordpress.com/2013/11/10/debianubuntu-package-developing-with-docker/)    
7. [Debian/Ubuntu Package Developing with Docker, Continued.](https://sfxpt.wordpress.com/2013/11/17/debianubuntu-package-developing-with-docker-continued/)  
8. [Create docker image. (broken link)](https://wiki.debian.org/Cloud/CreateDockerImage)  
9. [Article in Spanish about docker and how to change docker deployments. ](https://magmax.org/blog/docker/)
10. Some articles from Javier Garzas' blog:   
10.1 [What is Docker? What is it used for? Explained simply](http://www.javiergarzas.com/2015/07/que-es-docker-sencillo.html)  
10.2 [Understanding Docker. Basic concepts: Images, Containers, Links… ](http://www.javiergarzas.com/2015/07/entendiendo-docker.html)  
10.3 [For beginners: create and run your own image in a Docker container (1/2)](http://www.javiergarzas.com/2015/11/para-los-que-empiezan-crear-y-ejecutar-una-imagen-propia-en-un-contenedor-docker-12.html)
10.4 [For beginners: create and run your own image in a Docker container (2/2)](http://www.javiergarzas.com/2015/11/para-los-que-empiezan-crear-y-ejecutar-una-imagen-propia-en-un-contenedor-docker-22.html)  
10.5 [What if we want to orchestrate several Docker containers? Microservices, Docker Compose, Yaml… What a mess! (1/2)](http://www.javiergarzas.com/2015/11/y-si-queremos-orquestar-varios-contenedores-docker-microservicios-docker-compose-yaml-que-jaleo-12.html)  
10.6 [What if we want to orchestrate several Docker containers? Microservices, Docker Compose, Yaml… What a mess! (2/2)](http://www.javiergarzas.com/2015/12/y-si-queremos-orquestar-varios-contenedores-docker-microservicios-docker-compose-yaml-que-jaleo-22.html)  
11. [CONTAINERIZE YOUR WEB DEVELOPMENT: HOW DOCKER IS SOLVING REAL WORLD PROBLEMS FOR WEB DEVELOPERS!](https://usersnap.com/blog/docker-for-web-developers/?utm_source=quora&utm_medium=referral&utm_campaign=quora_docker)  
12. [Continuous Inspection in Java](https://sites.google.com/site/practicadesarrollosoft/temario/continuous-inspection/continuous-inspection-en-java)  
13. [sonarqube docker image](https://hub.docker.com/_/sonarqube/)  
14. [Jenkins docker image](https://hub.docker.com/_/jenkins/)  
15. [docker image for debian jessie](https://hub.docker.com/_/debian/)  
16. [AUDITING AND VULNERABILITY ANALYSIS IN DOCKER](http://www.securitybydefault.com/2015/12/auditoria-y-analisis-de.html)  
17. [Docker for running integration tests in NodeJS](http://abirtone.com/docker/2015/07/28/uso-de-docker-en-aplicacion-de-nodejs/)  
18. [Docker Explained: How to create Docker Containers running Memcached](https://www.digitalocean.com/community/tutorials/docker-explicado-como-crear-contenedores-de-docker-corriendo-en-memcached-es)

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
