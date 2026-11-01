Title: Using Anaconda from a Docker container.   
Date: 2016-03-26 09:00    
Category: Tutorial Python   
Tags: Python,Docker,Anaconda,Ingeniería de Datos,Ciencia de Datos,Dockerhub  
lang: en
translation: true 

Continuing with articles related to Docker. This time I will show how to run Anaconda from a Docker image.

Here are the previous articles:
1. [Installing Docker on Debian Jessie (broken link)](/blog/instalardockerendebianjessie)  

2. [Using Docker on Debian Jessie (part 1)](/blog/usodedockerendebianjessie-1)  

3. [Using Docker on Debian Jessie (part 2)](/blog/usodedockerendebianjessie-2)  

4. [Creating a Docker image from a Dockerfile (broken link)](/blog/crearunaimagendockerapartirdeunarchivodockerfile)  

5. [Starting Django using Docker (broken link)](/blog/iniciandodjangousandodocker)  

6. [Installing Gitlab through Docker (broken link)](/blog/instalargitlabpormediodedocker)  

7. [Running microservices with docker using docker-compose (broken link)](/blog/ejecutandomicrosservicioscondockerusandodockercompose)  

8. [Docker in Docker (DinD) (broken link)](/blog/dockerendockerdind)

9. [Starting Django with docker using docker-compose with postgresql as a microservice. (broken link)](/blog/iniciandodjangocondockerusandodockercomposeconpostgresqlcomomicroservicio)

10. [Importing a Docker container in Python. (broken link)](/blog/importaruncontenedordockerenpython) 

11. [Sharing Docker images through tar files (broken link)](/blog/compartirimagenesdockerpormediodearchivostar).

12. [Creating a private Docker image registry. (broken link)](/blog/crearunregistrodeimagenesdockerprivado)




The first thing you are probably wondering is, what is Anaconda?. 

You can find the answer at the official [continuum](http://abirtone.com/docker/2015/07/28/uso-de-docker-en-aplicacion-de-nodejs/) site link:

Anaconda is a package manager (free and easy to install), environment manager, Python distribution, and a collection of over 720 opensource packages with community support. In addition, you can install over a thousand packages with the command `conda install <paquete>`, and it works on Linux, Windows and OSX.  Anaconda is the tool made for data scientists.  

Who else uses anaconda? 
- Data Scientists.  
- Developers.  
- Data Engineers.  
- DevOps.  
- Business analysts.   
- 
The procedure for using anaconda is explained at this [link](https://docs.continuum.io/new-anaconda-start-here).

You can see the existing anaconda images at this [link](https://hub.docker.com/).

To see the continuum team's images, do a search with docker:
```
$docker search continuumio

NAME                                   DESCRIPTION                                           STARS     OFFICIAL   AUTOMATED
continuumio/anaconda                 Powerful and flexible python distribution    27                   [OK]
continuumio/miniconda                Powerful and flexible package manager     14                   [OK]
continuumio/anaconda3                                                                               10                   [OK]
continuumio/miniconda3                                                                                5                    [OK]
continuumio/memex_explorer      memex explorer app                                   1                    
continuumio/solr                          solr 10.4.2 + tika                                       0                    
continuumio/tika                          Tika 1.9                                                     0                    
continuumio/binstar-build-linux64                                                                  0                    [OK]
continuumio/kibana                                                                                       0                    
continuumio/imagecat                   Docker Container for ImageCat                0                    
continuumio/banana                                                                                      0
```
Then the miniconda image will be downloaded:
```
$ docker pull continuumio/miniconda

Using default tag: latest
latest: Pulling from continuumio/miniconda
a3ed95caeb02: Pull complete 
79362e2488a1: Pull complete 
41938770486e: Pull complete 
1c66b99d17cb: Pull complete 
33e1cf31bc39: Pull complete 
Digest: sha256:5d27e59a93068184fc6dd63043746ad35aa15dd2862ff0babd391bc3c05a5fc4
Status: Downloaded newer image for continuumio/miniconda:latest
```
Now you can start a container from the image that was downloaded:
```
$ docker run -t -i continuumio/miniconda /bin/bash
root@f7115572fad4:/# 
```
Test that conda is installed in that container:
```
ernesto@jewel:~/dockerfiles$ docker run -t -i continuumio/miniconda /bin/bash
root@f7115572fad4:/# conda info
Current conda install:

             platform : linux-64
        conda version : 3.19.0
  conda-build version : not installed
       python version : 2.7.11.final.0
     requests version : 2.9.0
     root environment : /opt/conda  (writable)
  default environment : /opt/conda
     envs directories : /opt/conda/envs
        package cache : /opt/conda/pkgs
         channel URLs : https://repo.continuum.io/pkgs/free/linux-64/
                        https://repo.continuum.io/pkgs/free/noarch/
                        https://repo.continuum.io/pkgs/pro/linux-64/
                        https://repo.continuum.io/pkgs/pro/noarch/
          config file : None
    is foreign system : False

```

Now `scipy` will be installed via the `conda` command:
```
root@f7115572fad4:/# conda install scipy
Fetching package metadata: ....
Solving package specifications: ....................
Package plan for installation in environment /opt/conda:

The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    libgfortran-3.0            |                0         261 KB
    mkl-11.3.1                 |                0       121.2 MB
    openssl-1.0.2g             |                0         3.2 MB
    sqlite-3.9.2               |                0         3.9 MB
    numpy-1.10.4               |           py27_1         6.0 MB
    requests-2.9.1             |           py27_0         605 KB
    setuptools-20.3            |           py27_0         452 KB
    wheel-0.29.0               |           py27_0          81 KB
    conda-4.0.5                |           py27_0         185 KB
    pip-8.1.1                  |           py27_0         1.5 MB
    scipy-0.17.0               |      np110py27_2        30.1 MB
    ------------------------------------------------------------
                                           Total:       167.3 MB

The following NEW packages will be INSTALLED:

    libgfortran: 3.0-0             
    mkl:         11.3.1-0          
    numpy:       1.10.4-py27_1     
    scipy:       0.17.0-np110py27_2

The following packages will be UPDATED:

    conda:       3.19.0-py27_0 --> 4.0.5-py27_0      
    openssl:     1.0.2d-0      --> 1.0.2g-0          
    pip:         7.1.2-py27_0  --> 8.1.1-py27_0      
    requests:    2.9.0-py27_0  --> 2.9.1-py27_0      
    setuptools:  18.8.1-py27_0 --> 20.3-py27_0       
    sqlite:      3.8.4.1-1     --> 3.9.2-0           
    wheel:       0.26.0-py27_1 --> 0.29.0-py27_0     

Proceed ([y]/n)? y
```
Another option is to download continuumio/anaconda, which has the base packages:
```
$ docker pull continuumio/anaconda
```
And run the container:
```
ernesto@jewel:~/dockerfiles$ docker run -t -i continuumio/anaconda /bin/bash
root@f7115572fad4:/#
```
##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
