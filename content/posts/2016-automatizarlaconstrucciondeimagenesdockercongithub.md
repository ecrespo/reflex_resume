Title: Automatizar la construcción de imágenes Docker con github  
Date: 2016-05-11 09:00
Category: Linux,Desarrollo    
Tags: Canaima,Debian,Linux,Ubuntu,Docker, Github,CI/CD,DevOps
lang: es  
translation: true


En esté artículo se explica como construir una imagen Docker automáticamente usando github con el hub de docker.

Este artículo se basa en la documentación existente en el sitio de docker hub para [construcción automatizada.](https://docs.docker.com/docker-hub/builds/link-source/)

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

Lo primero que se tiene que hacer es ir a la cuenta en [docker hub](https://hub.docker.com/), darle clic a cuentas enlazadas y servicios, ahí se selecciona github, como lo muestra la figura:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-1.png)


Al seleccionar github pasa a la parte de la cuenta de github de darle permisos:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-2.png)

Al darle aceptar ya aparecerá la cuenta asociada:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-3.png)


Ahora en github se va al setting del repositorio que se quiere asociar, a la parte de webhooks y service como lo muestra la figura:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-4.png)

Se agrega el servicio Docker:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-5.png)

Se prueba el servicio:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-6.png)

Por lo que se ve, la configuración pasa la prueba.

Ya de ahora en adelante cada vez que se haga un git push a github, docker hub se encarga de actualizar la imagen.

Para terminar se muestra el contenido del archivo Dockerfile de jenkins y el contenido del repositorio de github actualizado:

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-7.png)

![](./images/automatizarlaconstrucciondeimagenesdockercongithub-8.png)




##  ##
¡Haz tu donativo!
Si te gustó el artículo puedes realizar un donativo con Bitcoin (BTC)
usando la billetera digital de tu preferencia a la siguiente
dirección: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

O Escaneando el código QR desde la billetera:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
