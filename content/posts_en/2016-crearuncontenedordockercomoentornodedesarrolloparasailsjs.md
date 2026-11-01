Title: Creating a Docker container as a development environment for sails.js
Date: 2016-05-24 09:00
Category: Tutorial de Docker
Tags: Canaima,Debian,Linux,Ubuntu,Docker, Sails.js
lang: en
translation: true

This article covers using a Docker container as a Development environment.

The idea is to have the project's dependencies in the container and be able to develop the application outside the container through persistence as a volume.

This article is based on the information in the following [github](https://github.com/mwhahaha/docker-sails-test) repository.

This article uses the sails.js framework, but not in depth; I simply create the project and run it. For more information you can check the following [tutorial](https://code.tutsplus.com/tutorials/introduction-to-sailsjs--net-35390).

The previous articles about Docker are: 
 
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

18. [Setting up a Platform as a Service (PaaS) with Dokku (docker)](/blog/montarunaplataformacomoserviciopaascondokkudocker).  

19. [Using docker-machine.  ](/blog/usodedockermachine)

20. [Provisioning a cluster with docker swarm and docker-machine.](/blog/proveerunclustercondockerswarmydockermachine)

21. [Installing Jenkins through Docker and creating a Jenkins Docker image](/blog/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins) 

22. [Automating the building of Docker images with github.](/blog/automatizarlaconstrucciondeimagenesdockercongithub) 

23. [Creating a Docker image for MongoDB3.](/blog/crearunaimagendockerparamongodb-3)

There is a directory `ProyectoNuevo`, which is the `sails.js` project created with the command:
```
sails new ProyectoNuevo

ProyectoNuevo
├── api
│   ├── controllers
│   ├── models
│   ├── policies
│   │   └── sessionAuth.js
│   ├── responses
│   │   ├── badRequest.js
│   │   ├── created.js
│   │   ├── forbidden.js
│   │   ├── notFound.js
│   │   ├── ok.js
│   │   └── serverError.js
│   └── services
├── app.js
├── assets
│   ├── favicon.ico
│   ├── images
│   ├── js
│   │   └── dependencies
│   │       └── sails.io.js
│   ├── robots.txt
│   ├── styles
│   │   └── importer.less
│   └── templates
├── config
│   ├── blueprints.js
│   ├── bootstrap.js
│   ├── connections.js
│   ├── cors.js
│   ├── csrf.js
│   ├── env
│   │   ├── development.js
│   │   └── production.js
│   ├── globals.js
│   ├── http.js
│   ├── i18n.js
│   ├── locales
│   │   ├── de.json
│   │   ├── en.json
│   │   ├── es.json
│   │   ├── fr.json
│   │   └── _README.md
│   ├── local.js
│   ├── log.js
│   ├── models.js
│   ├── policies.js
│   ├── routes.js
│   ├── session.js
│   ├── sockets.js
│   └── views.js
├── Gruntfile.js
├── package.json
├── README.md
├── tasks
│   ├── config
│   │   ├── clean.js
│   │   ├── coffee.js
│   │   ├── concat.js
│   │   ├── copy.js
│   │   ├── cssmin.js
│   │   ├── jst.js
│   │   ├── less.js
│   │   ├── sails-linker.js
│   │   ├── sync.js
│   │   ├── uglify.js
│   │   └── watch.js
│   ├── pipeline.js
│   ├── README.md
│   └── register
│       ├── build.js
│       ├── buildProd.js
│       ├── compileAssets.js
│       ├── default.js
│       ├── linkAssetsBuild.js
│       ├── linkAssetsBuildProd.js
│       ├── linkAssets.js
│       ├── prod.js
│       └── syncAssets.js
└── views
    ├── 403.ejs
    ├── 404.ejs
    ├── 500.ejs
    ├── homepage.ejs
    └── layout.ejs
```
The directory where the project lives is called `sailsjs` with the following contents:
```
sailsjs
├── Dockerfile
├── ProyectoNuevo
└── run.sh
```
The contents of ProyectoNuevo were shown above.

The run.sh file contains a script to bring up sails through sails lift:
```
#!/bin/bash

cd /app/ProyectoNuevo
sails lift
```

The Dockerfile contains the following:

```
#Se usa la imagen de nodejs de google
FROM google/nodejs
#El mantenedor de la imagen
MAINTAINER Ernesto Crespo <ecrespo@gmail.com>
#El usuario del contenedor
USER root
#Se define el directorio de trabajo
WORKDIR /app
#Se copia el ProyectoNuevo a /app/
ADD ProyectoNuevo /app/
#Se instala sails en el contenedor
RUN npm -g install sails
#Se copia el script run.sh al directorio de trabajo
ADD run.sh /app/run.sh
#Se coloca el script con permiso de ejecución
RUN chmod a+x /app/run.sh

#Se expone el puerto 8080
EXPOSE 8080
#Se ejecuta el script
CMD ["/app/run.sh"] 
```

To build the image, run:
```
docker build -t sails-prueba . 
```
To run the image, run:
```
docker run -p 8080:8080 -v $PWD:/app  -ti sails-prueba
```
Below is an image after running the command:

![](./images/crearuncontenedordockercomoentornodedesarrolloparasailsjs-1.png)

The containers are listed:

![](./images/crearuncontenedordockercomoentornodedesarrolloparasailsjs-2.png)

The sails container is running alongside the mongodb one already explained in the [previous](/blog/crearunaimagendockerparamongodb-3) chapter.

Now open the browser on localhost at port 8080:

![](./images/crearuncontenedordockercomoentornodedesarrolloparasailsjs-3.png)

The idea of making the directory persistent is that you can keep modifying the project directory and bring up the container without having to rebuild its image. 

##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)