Title: Crear una imagen Docker de RethinkDB  
Date: 2016-06-10 09:00   
Category: Tutorial de Docker
Tags: Canaima,Linux,Python,Ubuntu,Docker, RethinkDB
lang: es   
translation: true   

RethinkDB es una base de datos NoSQL, opensource, es una base de datos que almacena documentos en formato JSON, facilita la inserción, actualización y busqueda en tiempo real (más info en el sitio de [rethinkDB](https://www.rethinkdb.com/) y en [wikipedia](https://en.wikipedia.org/wiki/RethinkDB)).

La idea es construir una imagen de Docker por medio de un archivo Dockerfile, tomando como base Debian Jessie. Aunque se puede usar directamente la imagen de RethinkDB que se encuentra en el [hub de docker](https://hub.docker.com/_/rethinkdb/).

Los artículos anteriores sobre Docker son:

1. [Instalar Docker en Debian Jessie](/blog/instalardockerendebianjessie)  

2. [Uso de Docker en Debian Jessie (parte 1) (enlace roto)](https://www.seraph.to/uso-de-docker-en-debian-jessie-parte-1.html)  

3. [Uso de Docker en Debian Jessie (parte 2) (enlace roto)](https://www.seraph.to/uso-de-docker-en-debian-jessie-parte-2.html)  

4. [Crear una imagen Docker a partir de un archivo Dockerfile](/blog/crearunaimagendockerapartirdeunarchivodockerfile)  

5. [Iniciando Django usando Docker](/blog/iniciandodjangousandodocker)  

6. [Instalar Gitlab por medio de Docker](/blog/instalargitlabpormediodedocker)  

7. [Ejecutando microservicios con docker usando docker-compose](/blog/ejecutandomicrosservicioscondockerusandodockercompose)  

8. [Docker en Docker (DinD)](/blog/dockerendockerdind)

9. [Iniciando Django con docker usando docker-compose con postgresql como microservicio.](/blog/iniciandodjangocondockerusandodockercomposeconpostgresqlcomomicroservicio)

10. [Importar un contenedor Docker en Python.](/blog/importaruncontenedordockerenpython) 

11. [Compartir imagenes Docker por medio de archivos tar](/blog/compartirimagenesdockerpormediodearchivostar).

12. [Crear un registro de imagenes Docker privado.](/blog/crearunregistrodeimagenesdockerprivado)

13. [Usar Anaconda desde un contenedor Docker.](/blog/usaranacondadesdeuncontenedordocker)  

14. [Crear un entorno de Integración y Despligue continue con Docker para node.js. (enlace roto)](https://www.seraph.to/crear-un-entorno-de-integracion-y-despligue-continue-con-docker-para-nodejs.html#crear-un-entorno-de-integracion-y-despligue-continue-con-docker-para-nodejs)  

15. [Usar Jupyter Notebook desde un contenedor Docker.](/blog/usarjupyternotebookdesdeuncontenedordedocker)  

16. [Ejecutar una prueba de doctest con un contenedor Docker](/blog/ejecutarunapruebadedoctestconuncontenedordocker).

17. [Ejecutar una prueba de unittest en Python con un contenedor Docker.](/blog/ejecutarunapruebadeunittestenpythonconuncontenedordocker) 

18. [Montar una Plataforma como servicio (PaaS) con Dokku (docker)](/blog/montarunaplataformacomoserviciopaascondokkudocker).  

19. [Uso de docker-machine.  ](/blog/usodedockermachine)

20. [Proveer un cluster con docker swarm y docker-machine.](/blog/proveerunclustercondockerswarmydockermachine)

21. [Instalar Jenkins por medio de Docker y crear una imagen Docker de Jenkins](/blog/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins) 

22. [Automatizar la construcción de imágenes Docker con github.](/blog/automatizarlaconstrucciondeimagenesdockercongithub) 

23. [Crear una imagen Docker para MongoDB3.](/blog/crearunaimagendockerparamongodb-3)

24. [Crear un contenedor Docker como entorno de desarrollo para Sails.js.](/blog/crearuncontenedordockercomoentornodedesarrolloparasailsjs)

25. [Correr aplicaciones de escritorio desde un contenedor Docker.](/blog/correraplicacionesdeescritoriodesdeuncontenedordocker)

26. [Usar dockerui para la gestión de imágenes y contenedores de Docker](/blog/usardockeruiparalagestiondeimagenesycontenedoresdedocker) 

El archivo Dockerfile toma parte del archivo oficial del sitio de RethinkDB, la idea es crear la imagen a partir de Debian Jessie (el dockerfile lo pueden ver en el siguiente [enlace](https://github.com/rethinkdb/rethinkdb-dockerfiles/blob/d129775a6b33cb9e9a3ced40edda31ba9016a647/jessie/2.3.4/Dockerfile)). 

El archivo `Dockerfile` es el siguiente:
```
#Base de Debian Jessie
FROM debian
#Mantenedor
MAINTAINER Ernesto Crespo <ecrespo@gmail.com>


# instalar RethinkDB
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get install -y wget 
RUN sh -c 'echo "deb http://download.rethinkdb.com/apt `lsb_release -cs` main" | tee /etc/apt/sources.list.d/rethinkdb.list'
RUN sh -c 'wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | apt-key add -'
RUN apt-get update
RUN apt-get install -y rethinkdb

#Se define el volumen donde se almacena los datos
VOLUME ["/data"]

#Se define el directorio de trabajo
WORKDIR /data

#Se ejecuta rethinkdb asociando todas las interfaces existentes en el contenedor
CMD ["rethinkdb", "--bind", "all"]

#   proceso, cluster webui
EXPOSE 28015 29015 8080
```

Para construir la imagen se ejecuta:
```
docker build -t debian-rethinkdb . 
```
Y para correr el contenedor (se asocia el volumen `/data` al directorio donde se ejecuta el contenedor):
```
docker run --name some-rethink -v "$PWD:/data" -d debian-rethinkdb
```
Para ver la interfaz administrativa vía web de rethingDB se ejecuta (caso chromium):
```
chromium "http://$(docker inspect --format  '{{ .NetworkSettings.IPAddress }}' some-rethink):8080"
```
A continuación se muestra una captura de pantalla de la aplicación web:

![](./images/crearunaimagendockerderethinkdb-1.png)

##  ##
¡Haz tu donativo!
Si te gustó el artículo puedes realizar un donativo con Bitcoin (BTC)
usando la billetera digital de tu preferencia a la siguiente
dirección: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

O Escaneando el código QR desde la billetera:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)



