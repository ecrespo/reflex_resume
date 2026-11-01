Title: Working with a docker container in Python using docker-py  
Date: 2016-08-21 09:00  
Category: Tutorial de Docker
Tags: Linux,Python, docker-py
lang: en  
translation: true  


This article will use the docker-py library to access Docker images and containers from python.

The docker-py documentation can be found on its [official](https://docker-py.readthedocs.io/en/stable/) site.


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

24. [Creating a Docker container as a development environment for Sails.js.](/blog/crearuncontenedordockercomoentornodedesarrolloparasailsjs)

25. [Running desktop applications from a Docker container.](/blog/correraplicacionesdeescritoriodesdeuncontenedordocker)

26. [Using dockerui to manage Docker images and containers](/blog/usardockeruiparalagestiondeimagenesycontenedoresdedocker) 

27. [Creating a Docker image of RethinkDB](/blog/crearunaimagendockerderethinkdb)

28. [Analyzing python code with pylint from Docker](/blog/analizarcodigopythonconpylintdesdedocker)

29. [Installing gitlab-runner of gitlab-ci through Docker](/blog/ejecutarunapruebadeintegracioncontinuacongitlabciygitlabrunner)

30. [Creating JSON data from a dictionary in Flask (part 1) (update - Docker)](/blog/creardatosjsonapartirdeundiccionarioenflaskactualizaciondocker-1)

31. [Running sonarqube from a Docker container](/blog/corrersonarqubedesdeuncontenedordocker)

32. [Creating a docker image of Redis.](/blog/crearunaimagendockerderedis)

33. [Introduction to Redis with Python](/blog/introduccionderedisconpython)

The first script contains the following:

```python

#!/usr/bin/python


#Se importa el cliente docker.

from docker import Client


#Se asocia la instancia cliente de docker con el socket.

cli = Client(base_url='unix://var/run/docker.sock')



print ("Se muestra la imagen docker de debian")

print (cli.images(name="debian"))



#Se crea un contenedor basandose en la imagen de debian y ejecuta sleep por 30 seg

container = cli.create_container(image="debian",command='/bin/sleep 30')



print  ("se imprime la informacion del contenedor")

print(container)

print ("Se muestra la información de los contenedores que están corriendo.")

print (cli.containers())

```

When the script is run you get:
```
python app.py
```
The debian docker image is shown
```
[{u'Created': 1449257280, u'Labels': None, u'VirtualSize': 125090240, u'ParentId': u'sha256:2e4b1470911604ccb99e3d2a9db8487661bb1d6db5b7aa9e4cf54a4b8bc7e33e', u'RepoTags': [u'debian:latest'], u'RepoDigests': None, u'Id': u'sha256:87b7eb6de0a6def7be27d485caf243354f8b5e19f41b0222b19f6f02b102dc61', u'Size': 125090240}]
se imprime la informacion del contenedor
{u'Id': u'766563f15d12562ff8fc6ff1a89ed76b1ebd914bfa9b8f753a4acf925778e720', u'Warnings': None}
Se muestra la informacion de los contenedores que estan corriendo.
[{u'Status': u'Up 43 minutes', u'Created': 1459285417, u'Image': u'jupyter/notebook', u'Labels': {}, u'NetworkSettings': {u'Networks': {u'bridge': {u'NetworkID': u'', u'MacAddress': u'02:42:ac:11:00:02', u'GlobalIPv6PrefixLen': 0, u'Links': None, u'GlobalIPv6Address': u'', u'IPv6Gateway': u'', u'IPAMConfig': None, u'EndpointID': u'ec791d0a8b52fee4fc46447b43304ce626629790e3a525cd4ae03e6a25bda3d5', u'IPPrefixLen': 16, u'IPAddress': u'172.17.0.2', u'Gateway': u'172.17.0.1', u'Aliases': None}}}, u'HostConfig': {u'NetworkMode': u'default'}, u'ImageID': u'sha256:1c02aa25b7b817d8b7a7557b4b62250db6c735da3e7fabb4b3a157e55256e2d4', u'State': u'running', u'Command': u'tini -- jupyter notebook', u'Names': [u'/berserk_darwin'], u'Mounts': [{u'RW': True, u'Source': u'/home/ernesto/dockers/notebook/notebook', u'Destination': u'/notebooks', u'Mode': u'', u'Propagation': u'rprivate'}], u'Id': u'dfcc1bd19dab02580cce30d1719d8514eb0af2ab1dec8b01e42b95376ce5e608', u'Ports': [{u'IP': u'0.0.0.0', u'Type': u'tcp', u'PublicPort': 8888, u'PrivatePort': 8888}]}]

```

The `app2.py` script contains the following:

```
#!/usr/bin/python

#Se importa el cliente docker.

from docker import Client

#Se import io para el manejo del texto en la salida.

from io import BytesIO

#Se crea el archivo dockerfile

dockerfile = '''

 # Shared Volume

 FROM busybox

 MAINTAINER Ernesto Crespo, ecrespo@gmail.com

 VOLUME /data

 CMD ["/bin/sh"]

 '''

 #Se define el encode como utf-8

f = BytesIO(dockerfile.encode('utf-8'))

#Se crea la instancia del cliente docker al socket.

cli = Client(base_url='unix://var/run/docker.sock')



#Se construye la imagen y devuelve la salida de la misma.

response = [line for line in cli.build(

 fileobj=f, rm=True, tag='ecrespo/data'

 )]



print ("Se muestra la respuesta")

for i in response:

 print (i)



print ("Se muestra los contenedores que estan corriendo, en este caso uno de jupyter")

print (cli.containers())

```

The result of running the `app2.py` script is the following:

The response is shown
```
{"stream":"Step 1 : FROM busybox\n"}

{"stream":" ---\u003e 8c9d515b3079\n"}

{"stream":"Step 2 : MAINTAINER Ernesto Crespo, ecrespo@gmail.com\n"}

{"stream":" ---\u003e Using cache\n"}

{"stream":" ---\u003e 5efdc0a317b7\n"}

{"stream":"Step 3 : VOLUME /data\n"}

{"stream":" ---\u003e Using cache\n"}

{"stream":" ---\u003e b0132c6c3a87\n"}

{"stream":"Step 4 : CMD /bin/sh\n"}

{"stream":" ---\u003e Using cache\n"}

{"stream":" ---\u003e a7c85281e78c\n"}

{"stream":"Successfully built a7c85281e78c\n"}
```
The running containers are shown, in this case a jupyter one
```
[{u'Status': u'Up 56 minutes', u'Created': 1459285417, u'Image': u'jupyter/notebook',
 u'Labels': {}, u'NetworkSettings': {u'Networks': {u'bridge': {u'NetworkID': u'',
 u'MacAddress': u'02:42:ac:11:00:02', u'GlobalIPv6PrefixLen': 0, u'Links': None, 
u'GlobalIPv6Address': u'', u'IPv6Gateway': u'', u'IPAMConfig': None, 
u'EndpointID': u'ec791d0a8b52fee4fc46447b43304ce626629790e3a525cd4ae03e6a25bda3d5',
 u'IPPrefixLen': 16, u'IPAddress': u'172.17.0.2', u'Gateway': u'172.17.0.1',
u'Aliases': None}}}, u'HostConfig': {u'NetworkMode': u'default'},
 u'ImageID': u'sha256:1c02aa25b7b817d8b7a7557b4b62250db6c735da3e7fabb4b3a157e55256e2d4',
 u'State': u'running', u'Command': u'tini -- jupyter notebook', 
u'Names': [u'/berserk_darwin'], u'Mounts': [{u'RW': True,
 u'Source': u'/home/ernesto/dockers/notebook/notebook',
 u'Destination': u'/notebooks', u'Mode': u'', u'Propagation': u'rprivate'}],
 u'Id': u'dfcc1bd19dab02580cce30d1719d8514eb0af2ab1dec8b01e42b95376ce5e608',
 u'Ports': [{u'IP': u'0.0.0.0', u'Type': u'tcp', u'PublicPort': 8888,
 u'PrivatePort': 8888}]}]
```
As you can see in the documentation and in the scripts that were run, you can create
 an application that accesses the docker API or work with images and containers 
from python. 

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)


