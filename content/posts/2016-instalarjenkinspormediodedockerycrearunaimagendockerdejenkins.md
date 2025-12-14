Title: Instalar Jenkins por medio de Docker y crear una imagen Docker de Jenkins.  
Date: 2016-05-10 09:00  
Category: Tutorial de Docker
Tags: Canaima,Debian,Linux,Ubuntu,Docker, Jenkins, CI/CD, DevOps  
lang: es  
translation: true

Tal como se hizo en el artículo de gitlab ahora se procede a explicar la instalación de Jenkins, la diferencia es que aparte del procedimiento vía una imagen de Docker, se creará una imagen propia de Jenkins.

Los artículos anteriores sobre Docker son:  

1. [Instalar Docker en Debian Jessie (enlace roto)](/blog/instalardockerendebianjessie)  

2. [Uso de Docker en Debian Jessie (parte 1) (enlace roto)](https://www.seraph.to/uso-de-docker-en-debian-jessie-parte-1.html)  

3. [Uso de Docker en Debian Jessie (parte 2) (enlace roto)](https://www.seraph.to/uso-de-docker-en-debian-jessie-parte-2.html)  

4. [Crear una imagen Docker a partir de un archivo Dockerfile (enlace roto)](/blog/crearunaimagendockerapartirdeunarchivodockerfile)  

5. [Iniciando Django usando Docker (enlace roto)](/blog/iniciandodjangousandodocker)  

6. [Instalar Gitlab por medio de Docker (enlace roto)](/blog/instalargitlabpormediodedocker)  

7. [Ejecutando microservicios con docker usando docker-compose (enlace roto)](/blog/ejecutandomicrosservicioscondockerusandodockercompose)  

8. [Docker en Docker (DinD) (enlace roto)](/blog/dockerendockerdind)

9. [Iniciando Django con docker usando docker-compose con postgresql como microservicio. (enlace roto)](/blog/iniciandodjangocondockerusandodockercomposeconpostgresqlcomomicroservicio)

10. [Importar un contenedor Docker en Python. (enlace roto)](/blog/importaruncontenedordockerenpython) 

11. [Compartir imagenes Docker por medio de archivos tar (enlace roto)](/blog/compartirimagenesdockerpormediodearchivostar).

12. [Crear un registro de imagenes Docker privado. (enlace roto)](/blog/crearunregistrodeimagenesdockerprivado)

13. [Usar Anaconda desde un contenedor Docker. (enlace roto)](/blog/usaranacondadesdeuncontenedordocker)  

14. [Crear un entorno de Integración y Despligue continue con Docker para node.js. (enlace roto)](https://www.seraph.to/crear-un-entorno-de-integracion-y-despligue-continue-con-docker-para-nodejs.html#crear-un-entorno-de-integracion-y-despligue-continue-con-docker-para-nodejs)  

15. [Usar Jupyter Notebook desde un contenedor Docker. (enlace roto)](/blog/usarjupyternotebookdesdeuncontenedordedocker)  

16. [Ejecutar una prueba de doctest con un contenedor Docker (enlace roto)](/blog/ejecutarunapruebadedoctestconuncontenedordocker).

17. [Ejecutar una prueba de unittest en Python con un contenedor Docker. (enlace roto)](/blog/ejecutarunapruebadeunittestenpythonconuncontenedordocker) 

18. [Montar una Plataforma como servicio (PaaS) con Dokku (docker) (enlace roto)](/blog/montarunaplataformacomoserviciopaascondokkudocker).  

19. [Uso de docker-machine.   (enlace roto)](/blog/usodedockermachine)

20. [Proveer un cluster con docker swarm y docker-machine. (enlace roto)](/blog/proveerunclustercondockerswarmydockermachine)

Este artículo se basa en una parte en el procedimiento del [repositorio oficial de Jenkins en Docker Hub](https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page=1&pullCount=0&q=jenkins&starCount=0). 

Basicamente para instalar jenkins de la imagen Docker oficial se ejecuta:
```
docker run -p 8080:8080 -p 50000:50000 jenkins
```
Pero en este caso se va a usar un archivo `Dockerfile` donde se instalará maven2, openjdk, docker, ant y jenkins. A fin de tener un soporte suficiente para los plugins que trae jenkins.

El archivo `Dockerfile` es el siguiente:
```
FROM debian
MAINTAINER Ernesto Crespo <ecrespo@gmail.com>
RUN apt-get update
RUN apt-get install -y apt-transport-https
RUN apt-get install -y git
RUN apt-get install -y openssh-server openssh-client
RUN apt-get install -y openjdk-7-jdk maven2 ant 
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys  58118E89F3A912897C070ADBF76221572C52609D
RUN sh -c 'echo "deb https://apt.dockerproject.org/repo debian-jessie main" > /etc/apt/sources.list.d/docker.list'
RUN apt-get install -y wget 
RUN wget -q -O - https://jenkins-ci.org/debian/jenkins-ci.org.key | apt-key add -
RUN sh -c 'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
RUN apt-get update
RUN apt-get install -y docker-engine
RUN apt-get install -y jenkins 
RUN apt-get install -y vim less locate
RUN sh -c 'service docker start'
RUN sh -c 'service jenkins start'
RUN apt-get clean
EXPOSE 8080 50000 22
ENTRYPOINT ["java","-jar","/usr/share/jenkins/jenkins.war"]
CMD [""]
```
Como se ve, se está usando una imagen Debian y se le instala lo necesario para tener jenkins con algunas herramientas adicionales como Docker, maven2, ant y jenkins. 

Para construir la imagen se ejecuta:
```
docker build -t docker-jenkins . 
```
Esto genera la imagen como se ve a continuación:
```
docker images
REPOSITORY             TAG                 IMAGE ID            CREATED             SIZE
docker-jenkins         latest              844985a7b6ad        54 minutes ago      855.3 MB
```
Para crear el contenedor se ejecuta:
```
docker run -p 8080:8080 -p 50000:50000 -p 8022:22 -P  -d docker-jenkins
```
Esto genera la siguiente figura abriendo el navegador en localhost:8080:

![](./images/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins-1.png)

Acá se ejecuta docker exec a fin de ver el contenido del archivo que contiene la llave para autenticar el jenkins:
```
docker exec -ti naughty_darwin /bin/bash
```
Se busca el archivo dentro del contenedor:
```
cd /root/.jenkins/secrets/
cat initialAdminPassword 
4280c91df94a43308a731c008c6abb3d
```
Ya con eso se pregunta si se quiere seleccionar los plugins o si se instalan los recomendados:

![](./images/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins-2.png)

Luego se muestra la ventana del proceso de instalación de plugins:

![](./images/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins-3.png)

Al terminar este proceso se pide crear un usuario administrador:

![](./images/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins-4.png)

Luego de esto ya se muestra la página de que se terminó el proceso de configuración:

![](./images/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins-5.png)

A continuación se muestra la página inicial de Jenkins:

![](./images/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins-6.png)

Para terminar se instalarán unos plugins adicionales necesarios para próximo artículo (git, gitlab y docker):

![](./images/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins-7.png)

El archivo Dockerfile utilizado para el artículo se encuentra en github en el siguiente [enlace](https://github.com/ecrespo/docker-jenkins).

Para terminar se suben los cambios a docker hub:

Primero se hace login en docker hub:
```
docker login 
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: ecrespo
Password: 
Login Succeeded
```
Luego se hace commit:
```
docker commit 91594bea7711 ecrespo/docker-jenkins
sha256:561e411227e6c0d5e74ef85f6d533c44cb1e66b68ef2da6eec66d228de173fc2
```
Se hace push:
```
docker push ecrespo/docker-jenkins
```
A continuación se muestra una imagen del sitio ecrespo/jenkins de docker hub:

![](./images/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins-8.png)

La configuración del Jenkins con Gitlab se tocará en el siguiente artículo. 


##  ##
¡Haz tu donativo!
Si te gustó el artículo puedes realizar un donativo con Bitcoin (BTC)
usando la billetera digital de tu preferencia a la siguiente
dirección: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

O Escaneando el código QR desde la billetera:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
