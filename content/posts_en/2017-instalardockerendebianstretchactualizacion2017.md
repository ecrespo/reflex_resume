Title: Installing Docker on Debian Stretch (2017 update).
Date: 2017-07-09 09:00
Category: Tutorial de Linux
Tags: Linux,Debian,Ubuntu, Docker
lang: en
translation: true

The first article of the [series of articles about Docker](/blog/tags) was the one on [Installing Docker on Debian Jessie](/blog/instalardockerendebianjessie); now I will explain the installation process of Docker CE for Debian Stretch. The English installation guide for docker on Debian can be found at the following [link](https://docs.docker.com/engine/installation/linux/docker-ce/debian/).

The procedure is the following:

1. Install the packages required for https support in `apt-get`:
```
#apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common
```

2. Add Docker's official `gpg` key:
```
# curl -fsSL https://download.docker.com/linux/debian/gpg |  apt-key add -
OK
```
If it returns "OK", the key was downloaded and added without problems.

3. Verify the key:
```
# apt-key fingerprint 0EBFCD88
pub   rsa4096 2017-02-22 [SCEA]
      9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
uid           Docker Release (CE deb) <docker@docker.com>
sub   rsa4096 2017-02-22 [S]
```
4. Add the Stable repository for the Debian version on the machine:
```
add-apt-repository \
>    "deb [arch=amd64] https://download.docker.com/linux/debian \
>    $(lsb_release -cs) \
>    stable"
```
5. Update the package list:
```
#apt-get update
```
6. Install `docker-ce`:
```
# apt-get install docker-ce
```
7. Verify that `docker-ce` was installed correctly:
```
# docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
b04784fba78d: Pull complete 
Digest: sha256:f3b3b28a45160805bb16542c9531888519430e9e6d6ffc09d72261b0d26ff74f
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

Share images, automate workflows, and more with a free Docker ID:
 https://cloud.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/
```

8. Install docker-compose:
```
#apt-get install  docker-compose
```


Manage docker as a normal user:

1. Create the docker group:
```
$sudo groupadd docker
```
2. Add the user to the docker group:
```
$sudo usermod -aG docker $USER
```
3. Verify that docker can be used from the user:
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

Share images, automate workflows, and more with a free Docker ID:
 https://cloud.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/

```

Configure Docker to start at boot:

1. Enable Docker:
```
$ sudo systemctl enable docker
Synchronizing state of docker.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable docker
```

If you need configuration details you can see them in the [docker documentation](https://docs.docker.com/engine/installation/linux/linux-postinstall/#your-kernel-does-not-support-cgroup-swap-limit-capabilities).

Finally, cloud9 is started as already explained in a [previous article](/blog/entornodedesarrolloenlanubecloud9).
```
$docker run -it -d -p 9080:80 -v /home/ernesto/worksplace/:/workspace/ kdelfour/cloud9-docker
99cfe3af5bf4480ac456ec43916612317a49da111ab27e32a361639984eb2128
```
The following screenshot shows cloud9 running:

![](./images/instalardockerendebianstretchactualizacion2017-1.png)

The projects edited from cloud9 are saved in the worksplace directory.
```
$ tree worksplace
worksplace
├── hola.py
├── New Folder
│   ├── mvc1.py
│   ├── New Folder
│   └── usuario.py
└── trabajo.txt

2 directories, 4 files
```


##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
