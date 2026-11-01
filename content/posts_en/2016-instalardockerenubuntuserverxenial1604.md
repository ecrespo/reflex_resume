Title: Installing Docker on Ubuntu Server Xenial 16.04  
Date: 2016-09-09 09:00  
Category: Tutorial de Linux
Tags: Docker, Linux, Ubuntu
lang: en  
translation: true 

This guide is for Ubuntu users who want to install Docker.

The installation will be done on Ubuntu Server Xenial:

This tutorial is based on the [official documentation in English](https://docs.docker.com/install/linux/docker-ee/ubuntu/).

Installation  
We will work as superuser:  
```
sudo -s
```

The first thing to check is which Kernel version you have:
```
uname -r 
4.4.0-31-generic
```

For Ubuntu Xenial 16.04 it is recommended to have the kernel packages: `linux-image-extra-* .`
```
sudo apt-get update

sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual
```


To be able to use the docker repositories on ubuntu, you need `https` support for the repos:
```
sudo apt-get install apt-transport-https ca-certificates
```

Add the Docker repository key on Ubuntu:
```
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
```

Create the `docker.list` file to add the Docker repositories on Ubuntu:
```
sudo vim /etc/apt/sources.list.d/docker.list
```
For Ubuntu Xenial, the line to add to the file is the following:
```
deb https://apt.dockerproject.org/repo ubuntu-xenial main
```
Run an update:
```
apt-get update
```
Remove any ubuntu package for docker:
```
sudo apt-get purge lxc-docker 
```

Verify that the Docker packages are being looked up in the right repositories:
```
sudo apt-cache policy docker-engine
docker-engine:
  Instalados: (ninguno)
  Candidato:  1.12.1-0~xenial
  Tabla de versión:
     1.12.1-0~xenial 500
        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
     1.12.0-0~xenial 500
        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
     1.11.2-0~xenial 500
        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
     1.11.1-0~xenial 500
        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
     1.11.0-0~xenial 500
        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
```

Docker installation:  
```
sudo apt-get install docker-engine
```
Start the docker service:
```
sudo service docker start
```
Verify that docker was installed correctly:
```
docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
c04b14da8d14: Pull complete 
Digest: sha256:0256e8a36e2070f7bf2d0b0763dbabdd67798512411de4cdcf9431a1feb60fd9
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker Hub account:
 https://hub.docker.com

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/
```

Additional configuration
Create the Docker group:
```
sudo groupadd docker
```

Add the machine's user to the Docker group:  
```
sudo usermod -aG docker $USER
```

Restart the docker service:
```
service docker restart
```
Now, as an unprivileged user, test that you can use docker:
```
docker run hello-world
docker: Cannot connect to the Docker daemon. Is the docker daemon running on this host?.
See 'docker run --help'.
```
If the message above appears, you need to restart the machine:

Test again:  
```
$ docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker Hub account:
 https://hub.docker.com

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/
```

Start docker when the machine boots:
```
systemctl enable docker
```

For more additional configuration such as firewall and DNS, or other versions of Ubuntu, you can check the link at the beginning of the article to the official Docker documentation for Ubuntu.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)



