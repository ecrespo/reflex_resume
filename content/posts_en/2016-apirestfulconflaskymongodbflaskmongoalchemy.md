Title: RESTful API with Flask and MongoDB (Flask-MongoAlchemy)
Date: 2016-10-06 09:00
Category: Tutorial de Python
Tags: Python,API restful,Flask,MongoDB,Flask-restful,Flask-MongoAlchemy,Docker,Docker-compose
lang: en
translation: true

In the [previous](/blog/crudusandoflaskymongodbconormflaskmongoalchemy-4) article a CRUD was built for Flask with MongoDB using Mongo-Alchemy; in that article several URLs were used to do the CRUD.

In this article REST will be handled through the URLs and with Flask only; in upcoming articles Flask-RESTful and Flask-Restless will be used.  

#### HTTP methods 
In this case the CRUD will be standardized through a RESTful API, using the same URL with the GET, POST, PUT and DELETE methods.

The methods will be used as follows:

- Add Employee: POST method, URL /empleado, no parameters.  
- Find Employee: GET method, URL /empleado, parameter <string:nombre>.  
- List Employees: GET method, URL /empleado. 
- Edit/Update Employee: PUT method, URL /empleado, parameter <string:nombre>.  
- Delete Employee: DELETE method, URL /empleado, parameter <string:nombre>.  

As can be seen, with a single URL we get the CRUD actions using the HTTP methods; this allows us to standardize and simplify the use of URLs, and above all to make correct use of HTTP:

For more information about the REST API architectural style you can check [wikipedia](https://es.wikipedia.org/wiki/Representational_State_Transfer).

Directory and file structure
The same file and directory structure as in the CRUD article is kept:
```
tutorial-flask
├── app
│   └── run.py
├── docker-compose.yml
├── Dockerfile
└── README.md
```

`Dockerfile` and `docker-compose.yml` files

The `Docker` file contains the following:

```python
FROM python


WORKDIR /code/


RUN pip3 install --upgrade pip


RUN pip3 install  pymongo


RUN pip3 install Flask


RUN pip3 install Flask-PyMongo


RUN pip3 install Flask-MongoAlchemy



EXPOSE 5000



ADD ./app/* /code/


COPY ./app/* /code/


CMD python run.py

```

The `docker-compose.yml` file contains the following:

```
flask-rest1:

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

#### Application code

The code of `run.py` is shown below:

```python


#!/usr/bin/env python



#Se importa Flask, reqest y jsonify


from flask import Flask, request,jsonify



#Se importa MongoAlchemy


from flask_mongoalchemy import MongoAlchemy



#Se importa dumps


from bson.json_util import dumps



#Se instancia la clase de Flask, se configura el acceso


#a la base de datos mongodb a empleados


app = Flask(__name__)


app.config['MONGOALCHEMY_DATABASE'] = 'empleados'


app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://mongo:27017/empleados'



#Se instancia mongoalchemy pasando la app.


db = MongoAlchemy(app)


#Se crea la clase empleados la cual manejara los documentos.


class empleados(db.Document):


    nombre = db.StringField()


    sexo = db.StringField()


    edad = db.IntField()


    dni = db.IntField()


#Se define la funcion agregar con metodo get


@app.route('/empleado',methods=['POST'])


def agregar():


    #Se crea la instancia empleado de la clase empleados donde se


    #logra hacer la inserción de un empleado con el metodo save.


    nombre = str(request.json['nombre'])


    sexo = str(request.json['sexo'])


    edad = int(request.json['edad'])


    dni = int(request.json['dni'])


    empleado = empleados(nombre=nombre,sexo=sexo,edad=edad,dni=dni)


    empleado.save()





    #Se retorna que el usuario fue agregado.


    ###


    consulta = empleados.query.all()


    listado = []


    for i in consulta:


        listado.append(i.wrap())


    return dumps(listado)


#Se crea la funcion buscar con metodo get.


@app.route('/empleado/<string:nombre>',methods=['GET'])


def buscar(nombre):


    #Se realiza la busqueda y se devuelve el resultado, si existe un error de atributo (que el empleado no existe)


    #Se devuelve empleado no encontrado.


    try:


        resultado = empleados.query.filter(empleados.nombre == nombre).first()


        return dumps({'resultado':{'nombre':resultado.nombre,'sexo':resultado.sexo,'edad':resultado.edad,'dni':resultado.dni}})


    except (AttributeError):


        return dumps({'resultado': 'Empleado no encontrado'})


@app.route('/empleado',methods=['GET'])


def listar():


    #Se realiza la busqueda y se devuelve el resultado, si existe un error de atributo (que el empleado no existe)


    #Se devuelve empleado no encontrado.


    try:


        consulta = empleados.query.all()


        resultado = []


        for i in consulta:


            resultado.append(i.wrap())


        return dumps(resultado)


    except (AttributeError):


        return dumps({'resultado': 'Empleado no encontrado'})



#Se crea la funcion actualizar que tiene metodo put, con


#url /empleado y se le pasa el nombre a buscar


@app.route('/empleado/<string:nombre>',methods=['PUT'])


def actualizar(nombre):


    #Se intenta buscar al empleado en la base de datos, si no esta devuelve error


    try:


        #Se consulta en la base de datos, donde devuelve el primer elemento encontrado


        resultado = empleados.query.filter(empleados.nombre == nombre).first()


        #Se toma los datos de un json y se guardan en sus variables, salvando luego


        #en la base de datos.


        resultado.sexo = str(request.json['sexo'])


        resulado.edad = int(request.json['edad'])


        resultado.dni = int(request.json['dni'])


        resultado.save()


        #Se realiza la consulta desplegando los empleados


        consulta = empleados.query.all()


        listado = []


        for i in consulta:


            listado.append(i.wrap())


        #Se devuelve la nueva lista de empleados en un json.


        return dumps(listado)


    except (AttributeError):


        return dumps({'resultado': 'Empleado no encontrado'})


#Borrar un empleado de la base de datos, se pasa el url /empleado con el


#string nombre usando el metodo delete.


@app.route('/empleado/<string:nombre>',methods=['DELETE'])


def borrar(nombre):


    #Se busca el empleado, si existe se borra de la base de datos y se devuelve


    #mensaje de empleado borrado, si no, se devuelve el mensaje de empleado no


    #encontrado.


    try:


        resultado = empleados.query.filter(empleados.nombre == nombre).first()


        resultado.remove()


        ###


        consulta = empleados.query.all()


        listado = []


        for i in consulta:


            listado.append(i.wrap())


        return dumps(listado)


    except (AttributeError):


        return dumps({'resultado':'Empleado no encontrado'})


if __name__ == "__main__":


    #Se corre la aplicacion en modo debug


    app.run(host="0.0.0.0",debug=True)

```

#### Building the image and running the container

Building the Docker image:
```
docker-compose build
```

Running the container:
```
docker-compose up
```

### Testing the RESTful API

In this case POSTMAN will be used, an application for google chrome.

#### List Employees

In postman, enter 127.0.0.1:5000/empleados with the GET method; the following figure shows the list:

![](./images/apirestfulconflaskymongodbflaskmongoalchemy-1.png)

The JSON it returns is the following:
```
[{"edad": 29, "dni": 8, "sexo": "Femenino", "nombre": "Jane Doe", "_id": {"$oid": "57ebbce45fd2bbeffc51330b"}}, {"edad": 39, "dni": 7, "sexo": "Masculino", "nombre": "John Doe", "_id": {"$oid": "57ebbd195fd2bbeffc51330c"}}, {"edad": 55, "dni": 6, "sexo": "Masculino", "nombre": "Pedro Perez", "_id": {"$oid": "57ebbd505fd2bbeffc51330d"}}, {"edad": 65, "dni": 5, "sexo": "Femenino", "nombre": "Petra", "_id": {"$oid": "57ebbd6b5fd2bbeffc51330e"}}, {"edad": 18, "dni": 4, "sexo": "Masculino", "nombre": "Luis Gonzalez", "_id": {"$oid": "57ebc34d5fd2bbeffc51330f"}}, {"edad": 34, "dni": 2, "sexo": "Femenino", "nombre": "Luissana", "_id": {"$oid": "57ebc3935fd2bbeffc513311"}}, {"edad": 43, "dni": 1, "sexo": "Masculino", "nombre": "Neg", "_id": {"$oid": "57ebc4b85fd2bbeffc513312"}}, {"edad": 29, "dni": 1050, "sexo": "Femenino", "nombre": "Dayana", "_id": {"$oid": "57f64d7d557e3f00086651e8"}}]
```
#### Find an Employee  

In postman enter the following url with the GET method 127.0.0.1/empleado/Neg , the following figure shows the result:

![](./images/apirestfulconflaskymongodbflaskmongoalchemy-2.png)

The JSON it returns is the following:
```
{"resultado": {"edad": 43, "dni": 1, "sexo": "Masculino", "nombre": "Neg"}}
```

#### Add Employee
In postman enter the url with the POST method 127.0.0.1:5000/empleado and pass the following in JSON format:
```
{
 "nombre": "Fatima",
 "sexo": "Femenino",
 "edad": 24,
 "dni": 1052
}
```
The following figure shows the capture of the information entered in postman:

![](./images/apirestfulconflaskymongodbflaskmongoalchemy-3.png)

This returns the following JSON:
```
[{"edad": 29, "dni": 8, "sexo": "Femenino", "nombre": "Jane Doe", "_id": {"$oid": "57ebbce45fd2bbeffc51330b"}}, {"edad": 39, "dni": 7, "sexo": "Masculino", "nombre": "John Doe", "_id": {"$oid": "57ebbd195fd2bbeffc51330c"}}, {"edad": 55, "dni": 6, "sexo": "Masculino", "nombre": "Pedro Perez", "_id": {"$oid": "57ebbd505fd2bbeffc51330d"}}, {"edad": 65, "dni": 5, "sexo": "Femenino", "nombre": "Petra", "_id": {"$oid": "57ebbd6b5fd2bbeffc51330e"}}, {"edad": 18, "dni": 4, "sexo": "Masculino", "nombre": "Luis Gonzalez", "_id": {"$oid": "57ebc34d5fd2bbeffc51330f"}}, {"edad": 34, "dni": 2, "sexo": "Femenino", "nombre": "Luissana", "_id": {"$oid": "57ebc3935fd2bbeffc513311"}}, {"edad": 43, "dni": 1, "sexo": "Masculino", "nombre": "Neg", "_id": {"$oid": "57ebc4b85fd2bbeffc513312"}}, {"edad": 29, "dni": 1050, "sexo": "Femenino", "nombre": "Dayana", "_id": {"$oid": "57f64d7d557e3f00086651e8"}}, {"edad": 24, "dni": 1052, "sexo": "Femenino", "nombre": "Fatima", "_id": {"$oid": "57f68505557e3f000e1aa766"}}]
```
As can be seen, the employee Fátima appears at the end in the database.

####Delete Employee
In this case we will delete the employee Fátima; enter the following url in postman with the DELETE method: 127.0.0.1:5000/empleado/Fatima .

The following image shows the execution in postman:

![](./images/apirestfulconflaskymongodbflaskmongoalchemy-4.png)

This returns the following JSON:
```
[{"edad": 29, "dni": 8, "sexo": "Femenino", "nombre": "Jane Doe", "_id": {"$oid": "57ebbce45fd2bbeffc51330b"}}, {"edad": 39, "dni": 7, "sexo": "Masculino", "nombre": "John Doe", "_id": {"$oid": "57ebbd195fd2bbeffc51330c"}}, {"edad": 55, "dni": 6, "sexo": "Masculino", "nombre": "Pedro Perez", "_id": {"$oid": "57ebbd505fd2bbeffc51330d"}}, {"edad": 65, "dni": 5, "sexo": "Femenino", "nombre": "Petra", "_id": {"$oid": "57ebbd6b5fd2bbeffc51330e"}}, {"edad": 18, "dni": 4, "sexo": "Masculino", "nombre": "Luis Gonzalez", "_id": {"$oid": "57ebc34d5fd2bbeffc51330f"}}, {"edad": 34, "dni": 2, "sexo": "Femenino", "nombre": "Luissana", "_id": {"$oid": "57ebc3935fd2bbeffc513311"}}, {"edad": 43, "dni": 1, "sexo": "Masculino", "nombre": "Neg", "_id": {"$oid": "57ebc4b85fd2bbeffc513312"}}, {"edad": 29, "dni": 1050, "sexo": "Femenino", "nombre": "Dayana", "_id": {"$oid": "57f64d7d557e3f00086651e8"}}]
```

#### Modify employee
In this case we will modify the employee Neg, changing his age.

Open postman entering the url 127.0.0.1:5000/empleado/Neg with the PUT method. In addition, add the JSON:
```
{
 "sexo": "Masculino",
 "edad": 41,
 "dni": 1
}
```
The following image shows postman:

![](./images/apirestfulconflaskymongodbflaskmongoalchemy-5.png)


This returns the following JSON:
```
[{"sexo": "Femenino", "_id": {"$oid": "57ebbce45fd2bbeffc51330b"}, "nombre": "Jane Doe", "dni": 8, "edad": 29}, {"sexo": "Masculino", "_id": {"$oid": "57ebbd195fd2bbeffc51330c"}, "nombre": "John Doe", "dni": 7, "edad": 39}, {"sexo": "Masculino", "_id": {"$oid": "57ebbd505fd2bbeffc51330d"}, "nombre": "Pedro Perez", "dni": 6, "edad": 55}, {"sexo": "Femenino", "_id": {"$oid": "57ebbd6b5fd2bbeffc51330e"}, "nombre": "Petra", "dni": 5, "edad": 65}, {"sexo": "Masculino", "_id": {"$oid": "57ebc34d5fd2bbeffc51330f"}, "nombre": "Luis Gonzalez", "dni": 4, "edad": 18}, {"sexo": "Femenino", "_id": {"$oid": "57ebc3935fd2bbeffc513311"}, "nombre": "Luissana", "dni": 2, "edad": 34}, {"sexo": "Masculino", "_id": {"$oid": "57ebc4b85fd2bbeffc513312"}, "nombre": "Neg", "dni": 1, "edad": 41}, {"sexo": "Femenino", "_id": {"$oid": "57f64d7d557e3f00086651e8"}, "nombre": "Dayana", "dni": 1050, "edad": 29}]
```

The employee Neg, whose age changed in the database, is shown underlined.

Finally, the server output is shown:
```
flask-rest1_1 | 172.17.0.1 - - [06/Oct/2016 15:59:33] "GET /empleado HTTP/1.1" 200 -
flask-rest1_1 | 172.17.0.1 - - [06/Oct/2016 16:03:48] "GET /empleado/Neg HTTP/1.1" 200 -
flask-rest1_1 | 172.17.0.1 - - [06/Oct/2016 17:08:22] "POST /empleado HTTP/1.1" 200 -
flask-rest1_1 | 172.17.0.1 - - [06/Oct/2016 17:39:24] "DELETE /empleado/Fatima HTTP/1.1" 200 -
flask-rest1_1 | 172.17.0.1 - - [06/Oct/2016 17:47:59] "PUT /empleado/Neg HTTP/1.1" 200 -
```

As can be seen, the output shows the URL used and the methods used.

This shows the use of the REST API architectural style and the use of HTTP with its different methods. 

The source code of this article is in the repository [tutorial-flask on gitlab, branch mongo-restful](https://gitlab.com/ecrespo/tutorial-flask/tree/mongo-restful).


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)



