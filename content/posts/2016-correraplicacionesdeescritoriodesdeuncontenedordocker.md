Title: Correr aplicaciones de escritorio desde un contenedor Docker
Date: 2016-05-26 10:00  
Category: Tutorial de Docker
Tags: Canaima,Debian,Linux,Ubuntu,Docker,Desktop,Aplicaciones
lang: es
translation: true

Este artículo se muestra de manera sencilla como correr varias aplicaciones gráficas desde contenedores Docker.

El artículo se basa en un artículo en inglés sobre el tema, pueden verlo en el siguiente [enlace (enlace roto)](https://linoxide.com/how-tos/20-docker-containers-desktop-user/).

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


Lynx:
Es un navegador para la cónsola, muy usado hace mucho. 
Para ejecutarlo con Docker se tiene el siguiente comando:
```
docker run -it --name lynx1
```

Esto ejecuta la aplicación desde un contenedor como lo muestra la siguiente figura:

![](./images/correraplicacionesdeescritoriodesdeuncontenedordocker-1.png)

Se puede visitar el repositorio del contenedor en Docker hub y ver el archivo Dockerfile del repositorio que se encuentra en el siguiente [enlace](https://hub.docker.com/r/jess/lynx/):
```
# Run Lynx in a conatiner 
#
# docker run --rm -it \
# --name lynx \
# jess/lynx github.com/jfrazelle
#
FROM debian:jessie
MAINTAINER Jessica Frazelle <jess@docker.com>

RUN apt-get update && apt-get install -y \
 lynx \
 --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "lynx" ]

```

En el enlace que pasé al inicio del artículo hay otras aplicaciones de escritorio que se pueden ejecutar, y al ver los Dockerfile se tiene una idea de como crear nuestras propias aplicaciones que corran desde un contenedor Docker.

##  ##
¡Haz tu donativo!
Si te gustó el artículo puedes realizar un donativo con Bitcoin (BTC)
usando la billetera digital de tu preferencia a la siguiente
dirección: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

O Escaneando el código QR desde la billetera:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
