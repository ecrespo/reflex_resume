Title: Using Jupyter Notebook from a Docker container  
Date: 2016-03-26 11:00  
Category: Tutorial Python  
Tags: Python, Docker, Jupyter Notebook, DevOps
lang: en
translation: true  

Jupyter Notebook is a web application that lets you create and share documents that contain code, plots and text. Its uses include data cleaning and transformation, numerical simulation, statistical modeling, machine learning and much more. You can find more information at this [link](https://jupyter.org/).

The idea is to run `jupyter notebook` from a docker container, where the generated files will be saved in the directory defined through a volume.

The previous articles on docker are:  
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

14. [Creating a Continuous Integration and Deployment environment with Docker for node.js.](/blog/crearunentornodeintegracionydespliguecontinuocondockerparanodejs)  

There are several Docker images from the jupyter team; the one that will be used is the [jupyter notebook (broken link)](https://hub.docker.com/r/jupyter/notebook/) one.  

To run the container we run the following commands:
```
$docker run --rm -it -p 8888:8888 -v "$(pwd):/notebooks" jupyter/notebook
```
Running the command gives what the following image shows:

![](./images/usarjupyternotebookdesdeuncontenedordedocker-1.png)

The port outside the container will be 8888, the same as the internal one; the volume is taken from the directory where the previous command is run. 

From a browser, open the following link: http://localhost:8888/ .

![](./images/usarjupyternotebookdesdeuncontenedordedocker-2.png)

A document is created with a series of python instructions and saved with the name prueba-python:

![](./images/usarjupyternotebookdesdeuncontenedordedocker-3.png)

Running `ls -l` in the directory where the container was started shows the file `prueba-python.ipynb`:
```
 ls -l notebooks/
total 4
-rw-r--r-- 1 root root 1390 mar 26 20:04 prueba-python.ipynb
```
With the volume option, the container's notebooks directory is being shared on the host machine.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
