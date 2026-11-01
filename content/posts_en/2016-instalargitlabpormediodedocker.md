Title: Installing Gitlab through Docker
Date: 2016-01-20 09:00
Category: Tutorial de Docker
Tags: Canaima,Debian,Ubuntu,Linux,Gitlab,Docker
lang: en
translation: true

The previous docker articles are the following:

1. [Installing Docker on Debian Jessie](/blog/instalardockerendebianjessie)  
2. [Using Docker on Debian Jessie (part 1)](/blog/usodedockerendebianjessie-1)  
3. [Using Docker on Debian Jessie (part 2)](/blog/usodedockerendebianjessie-2)  
4. [Creating a Docker image with a Dockerfile](/blog/crearunaimagendockerapartirdeunarchivodockerfile)  
5. [Starting Django using Docker](/blog/iniciandodjangousandodocker)  

The [first article on using Docker on Debian Jessie](/blog/usodedockerendebianjessie-1) shows at the end how to use SonarQube through Docker with two instances of the same image.


This article downloads the Gitlab community edition Docker image. The site where it is hosted is at the following [link](https://hub.docker.com/r/gitlab/gitlab-ce/) and the English documentation this article is based on is at the following link.

The `gitlab-ce` that will be downloaded from the dockerhub site will be run. The command is the following:
```
docker run --detach  --hostname pruebasgitlab --publish 443:443 --publish 80:80 --publish 22:22  --name gitlab   --restart always --volume /srv/gitlab/config:/etc/gitlab --volume /srv/gitlab/logs:/var/log/gitlab --volume /srv/gitlab/data:/var/opt/gitlab gitlab/gitlab-ce:latest
```

- hostname: The host name is pruebasgitlab.  
- publish: publishes ports 443, 80 and 22 of the container instance.  
- name: The name of the image is gitlab.  
- restart always: Always brings the instance back up.  
- volume: Some volumes are defined (they are directories of the host machine that are mounted in the containers); in this case there are 3 directories.  
- gitlab/gitlab-ce:latest: Fetches the latest version of the gitlab-ce image.  

The Gitlab container uses mounted volumes for persistent data:

- `/srv/gitlab/data` is mounted on `/var/opt/gitlab`
- `/srv/gitlab/logs` is mounted on `/var/log/gitlab`
- `/srv/gitlab/config` is mounted on `/etc/gitlab`


To configure Gitlab there is a file on the host at `/etc/gitlab/gitlab.rb`.

To access the configuration you can start bash in the running container, which lets you browse the directory structure and run any program:
```
docker exec -it gitlab /bin/bash
```
Now you can edit the `/etc/gitlab/gitlab.rb` file .

It can also be edited with the following command:
```
docker exec -it gitlab vi /etc/gitlab/gitla.rb
```
To enable https settings you can check the following [link](https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/doc/settings/nginx.md#enable-https), or the smtp settings at this [other one](https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/doc/settings/smtp.md).

To restart gitlab after changing the settings, run:
```
doker restart gitlab
```
A screenshot of gitlab running from Docker is shown below:

![](./images/instalargitlabpormediodedocker-1.png)

This article shows how to access several ports such as 80, 443 and 22, which allows connecting to that container remotely.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)