Title: Querying MongoDB from Flask (part 1)
Date: 2016-09-27 
Category: Tutorial Python
Tags: Python, Docker, Flask
lang: en
translation: true 

In this article Docker will be used to build the image that contains the Flask script with its dependencies, and docker-compose.yml will be used to link that image, as a container, with a mongoDB container.

To check the articles related to this one, see:

- [Articles about Docker](/blog/tags)
- [Articles about MongoDB](/blog/tags)
- [Articles about Flask](/blog/tags) 

There is a collection empleados in a database empleados  with the following data:
```
[{"_id": {"$oid": "57eb0887c535b9e290a6386d"}, "nombre": "Jane Doe", "sexo": "femenino", "edad": 29.0}, {"_id": {"$oid": "57eb0892c535b9e290a6386e"}, "nombre": "John Doe", "sexo": "masculino", "edad": 39.0}, {"_id": {"$oid": "57eb1c16c535b9e290a6386f"}, "nombre": "Pedro Perez", "sexo": "masculino", "edad": 55.0}, {"_id": {"$oid": "57eb1c66c535b9e290a63870"}, "nombre": "Petra", "sexo": "femenino", "edad": 65.0}]
```

### File and directory structure
The file and directory structure of the article's project is the following:
```
tutorial-flask
├── app
│   └── run.py
├── docker-compose.yml
├── Dockerfile
├── README.md
└── tmp
```

###Dockerfile file

The Dockerfile uses Python as the base system and will install the following dependencies:  

- pip upgrade  
- pymongo  
- Flask  
- Flask-PyMongo  
- 
It also exposes port 5000 and runs the script `run.py`.

Below is the content of the Dockerfile:

```python
FROM python


WORKDIR /code/


RUN pip3 install --upgrade pip


RUN pip3 install  pymongo


RUN pip3 install Flask


RUN pip3 install Flask-PyMongo


EXPOSE 5000

ADD ./app/* /code/


COPY ./app/* /code/


CMD python run.py
```

### docker-compose.yml file  

The docker-compose.yml file defines the build of the Docker image from the Dockerfile, the port to expose and the volume to expose, and it links with the mongo container, which uses the mongo image, exposes port 27017 and, finally, exposes the volume.

Below is the content of the file:

```
flask-mongo:


  build: .


  ports:


    - "5000:5000"


  volumes:


    - "./app/:/code"


  links:


    - mongo


mongo:


  image: mongo


  ports:


    - "27017:27017"


  volumes:


    - "/srv/data/db:/data/db:rw"

```


If you want the mongodb database to be public, expose the ports; if not, do not define the ports. To keep data persistent in the database, it is necessary to define the volume. 

### run.py script

This script is shown below: 
 
```python
#!/usr/bin/env python


#Se importa Flask


from flask import Flask


#Se importa PyMongo


from flask_pymongo import  PyMongo



#Se importa dumps de bson.json_util


from bson.json_util import dumps



#Se crea la instancia Flask


app = Flask(__name__)


#Se configura el acceso a la base de datos mongodb


app.config['MONGO_DBNAME'] = 'empleados'


app.config['MONGO_URI'] = 'mongodb://mongo:27017/empleados'





#Se asocia la configuración pasando la app


mongo = PyMongo(app)





#Se define la ruta raiz con metodo POST


@app.route('/',methods=['POST'])


def index():


    #Se realiza la conexion a la coleccion empleados


    empleados = mongo.db.empleados


    #Se hace la consulta y se devuelve  en formato json_util


    resultados = empleados.find()


    return dumps(resultados)



if __name__ == "__main__":


    #Se corre la aplicacion en modo debug


    app.run(host="0.0.0.0",debug=True)

```

### Create the Docker image and run the containers

To create the Docker image, run:
```
docker-compose build
```

To run the two containers, run:
```
docker-compose up
```

Below are the documents of the collection seen from robomongo:

![](./images/consultaamongodbdesdeflask1-1.png)


To make the query, postman (an application for google chrome) will be used; below is the image of the query result:

![](./images/consultaamongodbdesdeflask1-2.png)


Querying via POST to 127.0.0.1 port 5000 returns the json with all the employees in the mongodb database.

You can see the source code of this article in the [mongo1 branch on gitlab.](https://gitlab.com/ecrespo/tutorial-flask/tree/mongo1)

##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)


