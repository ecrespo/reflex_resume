Title: Usar dockerui para la gestión de imágenes y contenedores de Docker  
Date: 2016-05-26 11:00  
Category: Tutorial de Docker  
Tags: Canaima,Debian,Linux,Ubuntu, Docker,Dockerui
lang: es
translation: true

Docker UI es una interfaz web que permite administrar las imágenes de Docker, correr contenedores.

Se explicará el proceso de instalación y uso de dockerui.

Este artículo se basa de un artículo en inglés que lo pueden revisar en el siguiente enlace.

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

El proceso de instalación para Debian Jessie lo pueden ver en el primer artículo, pero, sí usa otra distribución puede leer el enlace en inglés del cual se basa este artículo que explican la instalación para Fedora u otras distros.

DockerUI se puede bajar como una imagen Docker, para correr el contenedor se ejecuta el siguiente comando: 
```
docker run -d -p 9000:9000 --privileged -v /var/run/docker.sock:/var/run/docker.sock dockerui/dockerui
```
Nota: El repositorio se encuentra en Docker Hub, se usó otro repositorio de dockerui.
```
docker run -d -p 9000:9000 --privileged -v /var/run/docker.sock:/var/run/docker.sock abh1nav/dockerui
```
La aplicación web corre en el puerto 9000, se le da todos los privilegios y se accede al socker del docker que corre en el equipo anfitrión. 


A continuación se muestra la página principal de dockerui:


![](./images/usardockeruiparalagestiondeimagenesycontenedoresdedocker-1.png)

![](./images/usardockeruiparalagestiondeimagenesycontenedoresdedocker-2.png)


Al darle a la sección de imágenes se listan todas las imágenes que se tienen en el equipo, allí se pueden remover imágenes:

![](./images/usardockeruiparalagestiondeimagenesycontenedoresdedocker-3.png)

Al darle click a una imagen aparecerá el botón crear:

![](./images/usardockeruiparalagestiondeimagenesycontenedoresdedocker-4.png)

Luego aparece una ventana donde se le define el comando a ejecutar, el nombre del contenedor, cuanta memoria y memoria swap va a usar, y el volumen:

![](./images/usardockeruiparalagestiondeimagenesycontenedoresdedocker-5.png)

En la sección de contenedores se puede, iniciar, reiniciar, detener, matar o remover los contenedores:

![](./images/usardockeruiparalagestiondeimagenesycontenedoresdedocker-6.png)


##  ##
¡Haz tu donativo!
Si te gustó el artículo puedes realizar un donativo con Bitcoin (BTC)
usando la billetera digital de tu preferencia a la siguiente
dirección: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

O Escaneando el código QR desde la billetera:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
