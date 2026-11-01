Title: Docker in Docker (DinD)   
Date: 2016-01-27 09:00  
Category: Tutorial de Docker 
Tags: Canaima,Debian,Linux,Ubuntu,Docker  
lang: en
translation: true


![](./images/dockerendockerdind-1.jpg)

Docker in Docker is simply running a Docker inside a Docker container.

You can visit the DinD site at the following [link](https://github.com/jpetazzo/dind), and the official DinD docker image at the following [link](https://hub.docker.com/_/docker/).

The first thing to do is run docker with some options:
```
docker run --rm --privileged -t -i -e LOG=file jpetazzo/dind
```
The `privileged` mode allows negotiating some features of the file system.

After starting the container, another container is run, this time from `busyox`, which returns "Hello new World!".
```
docker run busybox echo "Hello New World!"
```
A figure of the execution result is shown below.

![](./images/dockerendockerdind-2.png)


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)