Title: RESTful API with Flask and MongoDB (Flask-MongoAlchemy and Flask-restful)
Date: 2016-10-12 09:00
Category: Tutorial de Python
Tags: Python,API restful,Flask,MongoDB,Flask-restful,Flask-MongoAlchemy,Docker,Docker-compose
lang: en
translation: true

The [previous](/blog/apirestfulconflaskymongodbflaskmongoalchemy) article explained how to build the RESTful API using HTTP with the GET, POST, PUT and DELETE methods, without using a library for REST. 

This article will use the Flask-RestFul library; you can check its documentation [here (broken link)](https://flask-restful-cn.readthedocs.io/en/0.3.5/index.html). 

### Project file and directory structure

The file and directory structure remains the same as in the previous article:
```
tutorial-flask/
├── app
│   └── run.py
├── docker-compose.yml
├── Dockerfile
└── README.md

```

`Dockerfile` and `docker-compose.yml` files

The Dockerfile now also installs `flask-restful`; the file is shown below:

```python
FROM python


WORKDIR /code/

RUN pip3 install --upgrade pip


RUN pip3 install  pymongo


RUN pip3 install Flask


RUN pip3 install Flask-PyMongo


RUN pip3 install Flask-MongoAlchemy


RUN pip3 install Flask-restful


EXPOSE 5000


ADD ./app/* /code/


COPY ./app/* /code/


CMD python run.py


```

The `docker-compose.yml` file is the same as in the previous article:

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

### Application code

The same HTTP methods as in the previous article (GET, POST, PUT and DELETE) will be used; the url for the queries will be /empleados and the way to pass arguments through the url is by passing the employee's name /empleados/<string:nombre>  . 

Two classes are created:

- EmpleadoList: This class receives no arguments through the URL; it has two methods, GET and POST:
    - GET: Lists the employees that exist in the database.
    - POST: Inserts an employee into the database by passing a json with the data.
- Empleado: whose methods receive the name of an employee. The GET, PUT and DELETE methods are defined:
    - GET: Looks up an employee by passing their name; a json with their data is returned.
    - PUT: Updates an employee's information by passing their name and the json with the data to modify; it returns a json with all the employees.
    - DELETE: Deletes an employee from the database; the employee's name is passed in, and it returns a json with all the employees.



The code of `app/run.py` is shown below:

```python


#!/usr/bin/env python


#Se importa Flask, reqest y jsonify


from flask import Flask, request,jsonify, Response



#Se importa MongoAlchemy


from flask_mongoalchemy import MongoAlchemy


#Se importa dumps


from bson.json_util import dumps


#rom flask_restful import Resource, Api


from flask_restful import reqparse, abort, Api, Resource




#Se instancia la clase de Flask, se configura el acceso


#a la base de datos mongodb a empleados


app = Flask(__name__)


app.config['MONGOALCHEMY_DATABASE'] = 'empleados'


app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://mongo:27017/empleados'



#Se instancia mongoalchemy pasando la app.


db = MongoAlchemy(app)



#Se asocia el API a la aplicacion


api = Api(app)



#Se crea la clase empleados la cual manejara los documentos.


class empleados(db.Document):


    nombre = db.StringField()


    sexo = db.StringField()


    edad = db.IntField()


    dni = db.IntField()


#Se define la funcion de pagina no encontrada.


@app.errorhandler(404)


def not_found(error=None):


    mensaje = {


            'status': 404,


            'message': 'Not Found: ' + request.url,


    }


    resp = Response(jsonify(mensaje),status=404,mimetype='application/json')





    return resp





#Clase EmpleadosList que permite listar los empleados o insertar un empledo.


#Se definen los metdos get y post


class EmpleadosList(Resource):


    #Se define el metodo get el cual devuelve un json con todos los empleados.


    def get(self):


        #Se realiza la busqueda y se devuelve el resultado, si existe un error de atributo (que el empleado no existe)


        #Se devuelve empleado no encontrado.


        try:


            consulta = empleados.query.all()


            resultado = []


            for i in consulta:


                resultado.append(i.wrap())


            resp =  Response(dumps(resultado),status=200,mimetype='application/json')


            resp.headers['Link'] = 'http://blog.crespo.org.ve'


            return resp


        except (AttributeError):


            return not_found



    #Se define el metodo post para agregar un empleado por medio de un json a la


    #base de datos mongoDB.


    def post(self):


        #args = parser.parse_args()


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


        resp =  Response(dumps(listado),status=201,mimetype='application/json')


        resp.headers['Link'] = 'http://blog.crespo.org.ve'


        return resp


#Se crea la Clase Empleado que hereda de Resource


#Tiene los metodos get, put y delete


class Empleado(Resource):


    #Se define el metodo get, permite buscar un empleado por su nombre


    def get(self,nombre):


        #Se realiza la busqueda y se devuelve el resultado, si existe un error de atributo (que el empleado no existe)


        #Se devuelve empleado no encontrado.


        try:


            resultado = empleados.query.filter(empleados.nombre == nombre).first()


            return dumps({'nombre':resultado.nombre,'sexo':resultado.sexo,'edad':resultado.edad,'dni':resultado.dni}),200,{'Content-Type':'application/json'}


        except (AttributeError):


            return not_found

    #Se define el metodo put que permite actualizar la informacion de un empleado


    #pasando su nombre, los datos a modificar se pasan en un json.


    def put(self,nombre):


        #Se intenta buscar al empleado en la base de datos, si no esta devuelve error


        try:


            #Se consulta en la base de datos, donde devuelve el primer elemento encontrado


            resultado = empleados.query.filter(empleados.nombre == nombre).first()


            #Se toma los datos de un json y se guardan en sus variables, salvando luego


            #en la base de datos.


            resultado.sexo = str(request.json['sexo'])


            resultado.edad = int(request.json['edad'])


            resultado.dni = int(request.json['dni'])


            resultado.save()


            #Se realiza la consulta desplegando los empleados


            consulta = empleados.query.all()


            listado = []


            for i in consulta:


                listado.append(i.wrap())


            #Se devuelve la nueva lista de empleados en un json.


            resp =  Response(dumps(listado),status=201,mimetype='application/json')


            resp.headers['Link'] = 'http://blog.crespo.org.ve'


            return resp


        except (AttributeError):


            return not_found


    #Se define el metodo delete que permite borrar un empleado de la base de datos


    #pasando el nombre del empleado.


    def delete(self,nombre):


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


            resp =  Response(dumps(listado),status=200,mimetype='application/json')


            resp.headers['Link'] = 'http://blog.crespo.org.ve'


            return resp


        except (AttributeError):


            return not_found


#Se define las rutas para los recursos con las clases asociadas:


#/empleado


#/empleado/<string:nombre>


api.add_resource(EmpleadosList,'/empleado')


api.add_resource(Empleado,'/empleado/<string:nombre>')


if __name__ == "__main__":


    #Se corre la aplicacion en modo debug


    app.run(host="0.0.0.0",debug=True)

```

### Building the image and running the container

Building the Docker image:
```
docker-compose build
```

Running the Docker container:
```
docker-compose up
```

### Testing the RESTful API
Postman will be used to query the API.
#### List all the employees
Open postman at the url http://localhost:5000/empleado with the GET method; a screenshot is shown below:

![](./images/apirestfulconflaskymongodb-1.png)

The JSON that is returned is the following:
```
[{"edad": 29, "sexo": "Femenino", "nombre": "Jane Doe", "dni": 8, "_id": {"$oid": "57ebbce45fd2bbeffc51330b"}}, {"edad": 39, "sexo": "Masculino", "nombre": "John Doe", "dni": 7, "_id": {"$oid": "57ebbd195fd2bbeffc51330c"}}, {"edad": 55, "sexo": "Masculino", "nombre": "Pedro Perez", "dni": 6, "_id": {"$oid": "57ebbd505fd2bbeffc51330d"}}, {"edad": 65, "sexo": "Femenino", "nombre": "Petra", "dni": 5, "_id": {"$oid": "57ebbd6b5fd2bbeffc51330e"}}, {"edad": 18, "sexo": "Masculino", "nombre": "Luis Gonzalez", "dni": 4, "_id": {"$oid": "57ebc34d5fd2bbeffc51330f"}}, {"edad": 34, "sexo": "Femenino", "nombre": "Luissana", "dni": 2, "_id": {"$oid": "57ebc3935fd2bbeffc513311"}}, {"edad": 42, "sexo": "Masculino", "nombre": "Neg", "dni": 1, "_id": {"$oid": "57ebc4b85fd2bbeffc513312"}}, {"edad": 29, "sexo": "Femenino", "nombre": "Dayana", "dni": 1050, "_id": {"$oid": "57f64d7d557e3f00086651e8"}}]
```
Add an employee

Open postman at the URL http://localhost:5000/empleado with the POST method and pass the following JSON:
```
{
 "nombre": "Nadir",
 "sexo": "Masculino",
 "edad": 45,
 "dni": 11059
}
```

The screenshot of the data entry is shown below:

![](./images/apirestfulconflaskymongodb-2.png)

When the action is executed, the following result is obtained (as the next screenshot shows):

![](./images/apirestfulconflaskymongodb-3.png)

The JSON that is returned is the following:
```
[{"edad": 29, "sexo": "Femenino", "nombre": "Jane Doe", "dni": 8, "_id": {"$oid": "57ebbce45fd2bbeffc51330b"}}, {"edad": 39, "sexo": "Masculino", "nombre": "John Doe", "dni": 7, "_id": {"$oid": "57ebbd195fd2bbeffc51330c"}}, {"edad": 55, "sexo": "Masculino", "nombre": "Pedro Perez", "dni": 6, "_id": {"$oid": "57ebbd505fd2bbeffc51330d"}}, {"edad": 65, "sexo": "Femenino", "nombre": "Petra", "dni": 5, "_id": {"$oid": "57ebbd6b5fd2bbeffc51330e"}}, {"edad": 18, "sexo": "Masculino", "nombre": "Luis Gonzalez", "dni": 4, "_id": {"$oid": "57ebc34d5fd2bbeffc51330f"}}, {"edad": 34, "sexo": "Femenino", "nombre": "Luissana", "dni": 2, "_id": {"$oid": "57ebc3935fd2bbeffc513311"}}, {"edad": 42, "sexo": "Masculino", "nombre": "Neg", "dni": 1, "_id": {"$oid": "57ebc4b85fd2bbeffc513312"}}, {"edad": 29, "sexo": "Femenino", "nombre": "Dayana", "dni": 1050, "_id": {"$oid": "57f64d7d557e3f00086651e8"}}, {"edad": 45, "sexo": "Masculino", "nombre": "Nadir", "dni": 11059, "_id": {"$oid": "57fe2800d76747000b2ef40f"}}]
```

### Find an employee  
To find an employee, pass the following URL http://localhost:5000/empleado/Nadir with the GET method to postman; a screenshot of the result is shown below:

![](./images/apirestfulconflaskymongodb-3.png)

The JSON that is returned is the following:
```
"{\"edad\": 45, \"sexo\": \"Masculino\", \"nombre\": \"Nadir\", \"dni\": 11059}"
```

#### Update an employee

To update the employee Nadir, pass the following url to postman http://localhost:5000/empleado/Nadir with the PUT method, and pass the following json:
```
{
 "sexo": "Masculino",
 "edad": 35,
 "dni": 11059
}
```
The screenshot shows the data that was loaded into postman:

![](./images/apirestfulconflaskymongodb-4.png)

When the action is executed, the following screenshot is obtained:

![](./images/apirestfulconflaskymongodb-5.png)

The JSON that is returned is the following:
```
[{"edad": 29, "sexo": "Femenino", "nombre": "Jane Doe", "dni": 8, "_id": {"$oid": "57ebbce45fd2bbeffc51330b"}}, {"edad": 39, "sexo": "Masculino", "nombre": "John Doe", "dni": 7, "_id": {"$oid": "57ebbd195fd2bbeffc51330c"}}, {"edad": 55, "sexo": "Masculino", "nombre": "Pedro Perez", "dni": 6, "_id": {"$oid": "57ebbd505fd2bbeffc51330d"}}, {"edad": 65, "sexo": "Femenino", "nombre": "Petra", "dni": 5, "_id": {"$oid": "57ebbd6b5fd2bbeffc51330e"}}, {"edad": 18, "sexo": "Masculino", "nombre": "Luis Gonzalez", "dni": 4, "_id": {"$oid": "57ebc34d5fd2bbeffc51330f"}}, {"edad": 34, "sexo": "Femenino", "nombre": "Luissana", "dni": 2, "_id": {"$oid": "57ebc3935fd2bbeffc513311"}}, {"edad": 42, "sexo": "Masculino", "nombre": "Neg", "dni": 1, "_id": {"$oid": "57ebc4b85fd2bbeffc513312"}}, {"edad": 29, "sexo": "Femenino", "nombre": "Dayana", "dni": 1050, "_id": {"$oid": "57f64d7d557e3f00086651e8"}}, {"edad": 35, "sexo": "Masculino", "nombre": "Nadir", "dni": 11059, "_id": {"$oid": "57fe2800d76747000b2ef40f"}}]
```

As you can see, the data of the employee Nadir, as far as their age is concerned, has changed.

#### Delete an employee
Finally, the employee Nadir will be deleted from the database; pass the url http://localhost/empleado/Nadir with the DELETE method; the result in postman is shown below:

![](./images/apirestfulconflaskymongodb-6.png)

The JSON that is returned is the following:
```
[{"edad": 29, "sexo": "Femenino", "nombre": "Jane Doe", "dni": 8, "_id": {"$oid": "57ebbce45fd2bbeffc51330b"}}, {"edad": 39, "sexo": "Masculino", "nombre": "John Doe", "dni": 7, "_id": {"$oid": "57ebbd195fd2bbeffc51330c"}}, {"edad": 55, "sexo": "Masculino", "nombre": "Pedro Perez", "dni": 6, "_id": {"$oid": "57ebbd505fd2bbeffc51330d"}}, {"edad": 65, "sexo": "Femenino", "nombre": "Petra", "dni": 5, "_id": {"$oid": "57ebbd6b5fd2bbeffc51330e"}}, {"edad": 18, "sexo": "Masculino", "nombre": "Luis Gonzalez", "dni": 4, "_id": {"$oid": "57ebc34d5fd2bbeffc51330f"}}, {"edad": 34, "sexo": "Femenino", "nombre": "Luissana", "dni": 2, "_id": {"$oid": "57ebc3935fd2bbeffc513311"}}, {"edad": 42, "sexo": "Masculino", "nombre": "Neg", "dni": 1, "_id": {"$oid": "57ebc4b85fd2bbeffc513312"}}, {"edad": 29, "sexo": "Femenino", "nombre": "Dayana", "dni": 1050, "_id": {"$oid": "57f64d7d557e3f00086651e8"}}]
```
As you can see, the employee Nadir no longer exists in the database.

Finally, the screenshot of the running container is shown:

![](./images/apirestfulconflaskymongodb-7.png)

The Flask execution output is kept highlighted (the text is shown below):
```
flask-rest1_1 | 172.17.0.1 - - [12/Oct/2016 12:02:56] "GET /empleado HTTP/1.1" 200 -
mongo_1       | 2016-10-12T12:09:37.175+0000 I COMMAND  [conn2] update empleados.empleados query: { _id: ObjectId('57fe2800d76747000b2ef40f') } update: { _id: ObjectId('57fe2800d76747000b2ef40f'), edad: 45, sexo: "Masculino", nombre: "Nadir", dni: 11059 } keysExamined:0 docsExamined:0 nMatched:1 nModified:1 upsert:1 keyUpdates:0 writeConflicts:0 numYields:1 locks:{ Global: { acquireCount: { r: 2, w: 2 } }, Database: { acquireCount: { w: 2 } }, Collection: { acquireCount: { w: 2 } } } 326ms
flask-rest1_1 | 172.17.0.1 - - [12/Oct/2016 12:09:37] "POST /empleado HTTP/1.1" 201 -
flask-rest1_1 | 172.17.0.1 - - [12/Oct/2016 12:12:40] "GET /empleado/Nadir HTTP/1.1" 200 -
flask-rest1_1 | 172.17.0.1 - - [12/Oct/2016 12:18:23] "POST /empleado/Nadir HTTP/1.1" 405 -
mongo_1       | 2016-10-12T12:20:00.777+0000 I COMMAND  [conn2] update empleados.empleados query: { _id: ObjectId('57fe2800d76747000b2ef40f') } update: { _id: ObjectId('57fe2800d76747000b2ef40f'), edad: 35, sexo: "Masculino", nombre: "Nadir", dni: 11059 } keysExamined:1 docsExamined:1 nMatched:1 nModified:1 keyUpdates:0 writeConflicts:0 numYields:2 locks:{ Global: { acquireCount: { r: 3, w: 3 } }, Database: { acquireCount: { w: 3 } }, Collection: { acquireCount: { w: 3 } } } 124ms
flask-rest1_1 | 172.17.0.1 - - [12/Oct/2016 12:20:00] "PUT /empleado/Nadir HTTP/1.1" 201 -
flask-rest1_1 | 172.17.0.1 - - [12/Oct/2016 12:23:19] "DELETE /empleado/Nadir HTTP/1.1" 200 -
```

This improves how to create a REST API, in this case using flask-restful. 

The project repository is in the gitlab repository tutorial-flask on the branch [mongo-flask-restful](https://gitlab.com/ecrespo/tutorial-flask/tree/mongo-flask-restful).


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)