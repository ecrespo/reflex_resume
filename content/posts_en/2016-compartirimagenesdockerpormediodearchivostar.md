Title: Sharing Docker images through tar files   
Date: 2016-02-24 10:00  
Category: Tutorial de Docker
Tags: Linux,Debian,Docker
lang: en
translation: true  

One of the most important points when working with Docker is sharing Docker images other than through Docker Hub.

Exporting and importing images is an option, storing them in and extracting them from `tar` files.

Here are the previous articles on Docker:

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

The first thing is to see which containers are running on the machine:
```
$docker ps 
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS              PORTS                                                                    NAMES
b0c1163d1668        gitlab/gitlab-ce:latest   "/assets/wrapper"        4 weeks ago         Up 4 hours          0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp, 0.0.0.0:8022->22/tcp           gitlab
b4d3c96f6dc9        jenkins                   "/bin/tini -- /usr/lo"   4 weeks ago         Up 4 hours          0.0.0.0:8080->8080/tcp, 0.0.0.0:50000->50000/tcp, 0.0.0.0:8122->22/tcp   jenkins
```

There are two containers running, one for gitlab and one for jenkins.

The gitlab container will be backed up using the `docker export` command, passing the gitlab container id, which is b0c1163d1668:
```
$docker export b0c1163d1668 > gitlab.tar
```
Running `ls` shows the file `gitlab.tar`:  
```
ls -l
total 2201820
-rw-r--r-- 1 ernesto ernesto 1409662976 feb 24 16:15 gitlab.tar
```

To use the image from the `tar` file, import the image: 
```
$ docker import - gitlab2 < gitlab.tar
sha256:020ea830b267080ce092f42b1b0f1a2d520b21b8a3393696f5271f42e4bd8d79
```
The image name is gitlab2. Now list the images on the machine:
```
$ docker images | grep gitlab
gitlab2                        latest              020ea830b267        About a minute ago   1.344 GB
gitlab/gitlab-ce               latest              db1c29be1030        6 weeks ago          1.326 GB
sameersbn/gitlab               latest              47d53c4a820a        10 weeks ago         675.7 MB
```
If you want to share the image with someone, you can upload the `tar` file to a web server, and they can download it from there.  

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
