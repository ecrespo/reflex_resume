Title: Cloud9 Cloud Development Environment
Date: 2017-04-10 09:00
Category: Tutorial de Linux
Tags: Linux,Debian,Ubuntu,Nube,Cloud9,Docker
lang: en
translation: true

[Cloud9](http://en.wikipedia.org/wiki/Cloud9_IDE) is an online Integrated Development Environment, released as OpenSource since version 3.0.

Here are other links to articles about [docker](/blog/tags).

You can access the application at  [c9.io](http://c9.io/) .

An image of the site is shown below:

![](./images/entornodedesarrolloenlanubecloud9-1.png)

It is developed entirely in javascript, with ` node.js` as the backend, and the workspaces are built using Docker.

It supports several programming languages, the main ones being:  

- C/C++  
- PHP  
- Ruby  
- Perl  
- Python  
- Javascript  
- Go  

Since cloud9 is OpenSource, besides using it from its website you can set up a server; its source code is on [github](http://github.com/c9). You can find the installation procedure at the following [link](http://github.com/c9/core).

In this case a Docker image will be used to set it up as a local server. You can review the image that will be used at the following [link (broken link)](http://hub.docker.com/r/kdelfour/cloud9-docker/).

To run cloud9 as a container, run:
```
docker run -it -d -p 9080:80 -v /home/ernesto/worksplace/:/workspace/ kdelfour/cloud9-docker
```
In this case the application runs on port 9080 and workspace will be used as the working directory.

Running `docker ps` gives the following:
```
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS              PORTS                            NAMES
f4d06af60205        kdelfour/cloud9-docker   "supervisord -c /etc/"   38 seconds ago      Up 33 seconds       3000/tcp, 0.0.0.0:9080->80/tcp   condescending_gates
```
Now open the browser on port 9080; the image is shown below:

Image while cloud9 loads:

![](./images/entornodedesarrolloenlanubecloud9-2.png)

Working environment and a Hello world! example:

![](./images/entornodedesarrolloenlanubecloud9-3.png)

As you can see, it is no longer necessary to use the tool from the web; it can now be used from a local server using a Docker image.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
