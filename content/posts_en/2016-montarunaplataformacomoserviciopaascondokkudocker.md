Title: Setting up a Platform as a Service (PaaS) with Dokku (docker).  
Date: 2016-05-05 09:00  
Category: Tutorial de Docker 
Tags: Canaima,Debian,Linux,Ubuntu,Docker, Dokku, PaaS,DevOps  
lang: en  
translation: true


Continuing with the articles about Docker.

In this case I will explain how to set up and use [Dokku](https://github.com/dokku/dokku), a tool that makes it easy to set up a Platform as a Service ([PaaS](https://es.wikipedia.org/wiki/Computaci%C3%B3n_en_la_nube#Plataforma_como_servicio)) in the style of [Heroku](https://www.heroku.com/) on Linux (in this case Debian Jessie).

In this case there is no DNS server or hostname for the machine, so the IP 192.168.1.102 will be used.

The previous articles about docker are:  
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

15. [Using Jupyter Notebook from a Docker container.](/blog/usarjupyternotebookdesdeuncontenedordedocker)  

16. [Running a doctest test with a Docker container](/blog/ejecutarunapruebadedoctestconuncontenedordocker).

17. [Running a unittest test in Python with a Docker container.](/blog/ejecutarunapruebadeunittestenpythonconuncontenedordocker) 


To install and use `Dokku` I will be working with a virtual machine (so as not to use my own machine directly); for that, docker was installed in that virtual machine ([see article 1](/blog/instalardockerendebianjessie)).

You can find the `Dokku` installation procedure in its project on [github](https://github.com/dokku/dokku) or at the following [link (broken link)](http://dokku.viewdocs.io/dokku/getting-started/advanced-installation/).

Installation (for this procedure `docker-engine` is installed):
```
wget https://raw.githubusercontent.com/dokku/dokku/v0.5.6/bootstrap.sh
chmod a+x bootstrap.sh
sudo DOKKU_TAG=v0.5.6 bash bootstrap.sh
```
Another installation option is to download the `dokku` repository:
```
git clone https://github.com/progrium/dokku.git
cd dokku
sudo make install ; #es necesario tener make instalado; sudo apt-get install make
```

To see which version you have:
```
dokku version
v0.5.6-7-g851ca59
```

Configure the ssh key:  
1. Go to the local machine, go to the `.ssh` directory, and if you do not have an RSA key generated, generate one:  
```
cd .ssh
ssh-keygen -t rsa
```  
2. View the public key:
```
cat id_rsa.pub
```  
3. Copy the content of the key.  
4. On the server, as a user, run the following:  
```
echo "ssh-rsa ..... ernesto@crespo.org.ve"| sudo sshcommand acl-add dokku ernesto
```

Deploying a `node.js` and `express.js` application:
For this there is a github repository with a node.js and express.js application that has a hello world page.

Clone the repo (from the local machine):
```
git clone https://github.com/ecrespo/prueba-nodeexpress.git
```

The file and directory structure is:
```
prueba-nodeexpress/
├── app.json
├── index.js
├── LICENSE
└── package.json
```

The github repository is at the following [link](https://github.com/ecrespo/prueba-nodeexpress).

Add the remote `dokku` repo (192.168.1.102):
```
git remote add dokku dokku@192.168.1.102:prueba-nodeexpress
```
Edit the `index.html` file, and push it to the `dokku` repository:
```
git add public/index.html 
git commit -m"Agregado texto" 
git push dokku master 
```
Pushing produces the following output:
```
....
-----> Discovering process types
       Default types for  -> web
-----> Releasing prueba-nodeexpress (dokku/prueba-nodeexpress:latest)...
-----> Deploying prueba-nodeexpress (dokku/prueba-nodeexpress:latest)...
-----> Attempting to run scripts.dokku.predeploy from app.json (if defined)
-----> App Procfile file found (/home/dokku/prueba-nodeexpress/DOKKU_PROCFILE)
-----> DOKKU_SCALE file not found in app image. Generating one based on Procfile...
-----> New DOKKU_SCALE file generated
=====> web=1
-----> Running pre-flight checks
       For more efficient zero downtime deployments, create a file CHECKS.
       See http://dokku.viewdocs.io/dokku/checks-examples.md for examples
       CHECKS file not found in container: Running simple container check...
-----> Waiting for 10 seconds ...
-----> Default container check successful!
-----> Running post-deploy
-----> Attempting to run scripts.dokku.postdeploy from app.json (if defined)
=====> renaming container (2dacd928c2bb) clever_tesla to prueba-nodeexpress.web.1
=====> no global VHOST set. disabling vhost support
-----> Setting config vars
       NO_VHOST: 1
-----> no nginx port set. setting to random open high port
-----> Setting config vars
       DOKKU_NGINX_PORT: 53541
-----> Creating http nginx.conf
-----> Running nginx-pre-reload
       Reloading nginx
-----> Setting config vars
       DOKKU_APP_RESTORE: 1
=====> Application deployed:
       http://192.168.1.102:53541 (nginx)

To dokku@192.168.1.102:prueba-nodeexpress
 * [new branch]      master -> master

```
Opening the browser at http://192.168.1.102:53541 shows the following:


![](./images/montarunaplataformacomoserviciopaascondokkudocker-1.png)


For installing plugins you can check the following [link (broken link)](http://dokku.viewdocs.io/dokku/community/plugins/).

There are other tools similar to `dokku`:

- [flynn.io (enlace roto)](https://flynn.io/).  
- [deis.io (enlace roto)](https://azure.microsoft.com/en-us/services/kubernetes-service/).  
- [dokku-alt](https://github.com/dokku-alt/dokku-alt)

This is a small demonstration of how to have a deployment environment similar to Heroku.



##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
