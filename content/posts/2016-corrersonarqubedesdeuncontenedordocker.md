Title: Correr sonarqube desde un contenedor Docker   
Date: 2016-07-08 09:00  
Category: Tutorial de Docker
Tags: Linux, Debian, Docker, Sonarqube, QA
lang: es  
translation: true  


Continuando con los artículos de Docker, en este caso se muestra como iniciar SonarQube conectado a una base de datos PostgreSQL y pasando los datos de la base de datos por medio de variables de ambiente.

Sonarqube es una plataforma para evaluar código fuente ([tomado de wikipedia](https://es.wikipedia.org/wiki/SonarQube)).  

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

21. [Instalar Jenkins por medio de Docker y crear una imagen Docker de Jenkins (enlace roto)](/blog/instalarjenkinspormediodedockerycrearunaimagendockerdejenkins) 

22. [Automatizar la construcción de imágenes Docker con github. (enlace roto)](/blog/automatizarlaconstrucciondeimagenesdockercongithub) 

23. [Crear una imagen Docker para MongoDB3. (enlace roto)](/blog/crearunaimagendockerparamongodb-3)

24. [Crear un contenedor Docker como entorno de desarrollo para Sails.js. (enlace roto)](/blog/crearuncontenedordockercomoentornodedesarrolloparasailsjs)

25. [Correr aplicaciones de escritorio desde un contenedor Docker. (enlace roto)](/blog/correraplicacionesdeescritoriodesdeuncontenedordocker)

26. [Usar dockerui para la gestión de imágenes y contenedores de Docker (enlace roto)](/blog/usardockeruiparalagestiondeimagenesycontenedoresdedocker) 

27. [Crear una imagen Docker de RethinkDB (enlace roto)](/blog/crearunaimagendockerderethinkdb)

28. [Analizar código python con pylint desde Docker (enlace roto)](/blog/analizarcodigopythonconpylintdesdedocker)

29. [Instalar gitlab-runner de gitlab-ci por medio de Docker (enlace roto)](/blog/ejecutarunapruebadeintegracioncontinuacongitlabciygitlabrunner)

30. [Crear datos JSON a partir de un diccionario en Flask (parte 1) (actualización- Docker) (enlace roto)](https://www.seraph.to/crear-datos-json-a-partir-de-un-diccionario-en-flask-parte-1-actualizacion-docker.html#crear-datos-json-a-partir-de-un-diccionario-en-flask-parte-1-actualizacion-docker)

La guía de configuración y uso de  contenedores Docker para sonarqube lo pueden ver en el enalce de [Docker hub](https://hub.docker.com/_/sonarqube/).

Lo primero que se hará es iniciar un contenedor de postgreSQL:
```
docker run -d --name postgres2 --restart always  -e POSTGRES_PASSWORD=sonar -e POSTGRES_USER=sonar postgres
```

Se define que el usuario de la base de datos es sonar y su clave es sonar.


Ahora se inicia el contenedor de sonarqube:
```
docker run -d --name sonarqube --restart always -p 9000:9000 -p 9092:9092 -e SONARQUBE_JDBC_USERNAME=sonar -e SONARQUBE_JDBC_PASSWORD=sonar -e SONARQUBE_JDBC_URL=jdbc:postgresql://postgres2/sonar --link postgres2:postgres sonarqube
```

Se le pasan los puertos donde estará sonarqube (9000 y 9092), se le pasa la configuración de la base de datos a sonarqube (usuario, clave y url de conexión que usará el nombre del contenedor de postgres) y se enlace con el contenedor de postgres.

A continuación se muestra una captura de pantalla del contenedor corriendo:

![](./images/corrersonarqubedesdeuncontenedordocker-1.png)

Para terminar se muestran los contenedores corriendo:
```
docker ps 
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS              PORTS                                                          NAMES
e20d4108f54f        sonarqube                 "./bin/run.sh"           29 minutes ago      Up 29 minutes       0.0.0.0:9092->9092/tcp, 0.0.0.0:49000->9000/tcp                sonarqube
e3387c2754d1        postgres                  "/docker-entrypoint.s"   6 hours ago         Up 6 hours          5432/tcp                                                       postgres2
```

##  ##
¡Haz tu donativo!
Si te gustó el artículo puedes realizar un donativo con Bitcoin (BTC)
usando la billetera digital de tu preferencia a la siguiente
dirección: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

O Escaneando el código QR desde la billetera:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)



