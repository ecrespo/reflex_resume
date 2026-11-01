Title: CRUD using Flask and MongoDB with the Flask-MongoAlchemy ORM (part 4)  
Date: 2016-09-29 09:00  
Category: Tutorial Python  
Tags: Python,MongoDB,Flask,Docker,CRUD
lang: en  
translation: true  

Continuing with the series of articles on accessing mongodb from Flask. 

The previous articles are:  

- [Querying MongoDB from Flask (part 1)](/blog/consultaamongodbdesdeflask-1) 
- [Querying MongoDB from Flask (part 2 - pagination)](/blog/consultaamongodbdesdeflask-2)
- [CRUD using Flask for MongoDB  (part 3)](/blog/crudusandoflaskparamongodb-3) 

To see the articles related to this one, you can check:

- [Articles about Docker](/blog/tags)
- [Articles about MongoDB](/blog/tags)
- [Articles about Flask](/blog/tags)


The database keeps the format of the previous articles.

In this case I will insert the employee "Ernesto", then look him up in the database, update his information and delete him from the database.

### Dockerfile ###
This file has small changes: pymongo and Flask-PyMongo were removed, although mongoalchemy ends up using it. 

Here is the Dockerfile:

```python

FROM python

WORKDIR /code/

RUN pip3 install --upgrade pip


RUN pip3 install Flask


RUN pip3 install Flask-MongoAlchemy


EXPOSE 5000


ADD ./app/* /code/


COPY ./app/* /code/


CMD python run.py 

```

The `docker-compose.yml` file stays the same as in the previous articles.


### app/run.py file ###

In this case the crud is done with `mongoalchemy`. 

Here is the code of `run.py` : 

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





#Se define la funcion add con metodo get

@app.route('/add',methods=['GET'])

def add():

    #Se crea la instancia empleado de la clase empleados donde se

    #logra hacer la inserción de un empleado con el metodo save.

    empleado = empleados(nombre=str(request.args['nombre']),

                            sexo = str(request.args['sexo']),

                            edad = int(request.args['edad']),

                            dni = int(request.args['dni']))

    empleado.save()



    #Se retorna que el usuario fue agregado.

    return jsonify({'resultado': 'Usuario agregado' })



#Se crea la funcion find con metodo get.

@app.route('/find',methods=['GET'])

def find():

    #Se realiza la busqueda y se devuelve el resultado, si existe un error de atributo (que el empleado no existe)

    #Se devuelve empleado no encontrado.

    try:

        resultado = empleados.query.filter(empleados.nombre == str(request.args['nombre'])).first()

        return dumps({'resultado':{'nombre':resultado.nombre,'sexo':resultado.sexo,'edad':resultado.edad,'dni':resultado.dni}})

    except (AttributeError):

        return dumps({'resultado': 'Empleado no encontrado'})





@app.route('/update',methods=['GET'])

def update():

    #Se intenta buscar al empleado, si existe se toma los argumentos para actualizar sus

    #datos y devolver que se actualizo, si no devuelve usuario no encontrado.

    try:

        resultado = empleados.query.filter(empleados.nombre == str(request.args['nombre'])).first()

        resultado.sexo = str(request.args['sexo'])

        resultado.edad = int(request.args['edad'])

        resultado.dni = int(request.args['dni'])

        resultado.save()

        return dumps({'resultado':'Empleado actualizado'})

    except (AttributeError):

        return dumps({'resultado': 'Empleado no encontrado'})





@app.route('/delete/<nombre>')

def remove(nombre):

    #Se busca el empleado, si existe se borra de la base de datos y se devuelve

    #mensaje de empleado borrado, si no, se devuelve el mensaje de empleado no

    #encontrado.

    try:

        resultado = empleados.query.filter(empleados.nombre == str(nombre)).first()

        resultado.remove()

        return dumps({'resultado':'empleado borrado'})

    except (AttributeError):

        return dumps({'resultado':'Empleado no encontrado'})







if __name__ == "__main__":

    #Se corre la aplicacion en modo debug

    app.run(host="0.0.0.0",debug=True)


```

### Building the Docker image and running the containers ###

To build the image, run:
```
docker-compose build
```
To run the docker containers, run:
```
docker-compose up
```
Testing the CRUD
#### Create an employee:
When you open the browser at the following URL, the employee is inserted:
```
http://localhost:5000/add?nombre=Ernesto&dni=33&edad=11&sexo=Masculino
```
The result is shown in a JSON:
```
{
  "resultado": "Usuario agregado"
}
```
#### Find an employee
When you open the browser at the following URL, the employee is looked up:
```
http://localhost:5000/find?nombre=Ernesto
```
The result of the search is shown in a JSON:
```
{"resultado": {"nombre": "Ernesto", "sexo": "Masculino", "dni": 33, "edad": 11}}
```
#### Update an employee
When you open the browser at the following URL, a user's information is updated:
```
http://localhost:5000/update?nombre=Ernesto&edad=45&dni=50&sexo=Masculino
```

The result is shown in a JSON:
```
{"resultado": "Empleado actualizado"}
```

#### Delete an employee
Now what remains is to delete a document from the database; open the following URL:
```
http://localhost:5000/delete/Ernesto
```
The result is shown in a JSON:
```
{"resultado": "empleado borrado"}
```
If you query the user again, the JSON returned will say user not found:
```
http://localhost:5000/find?nombre=Ernesto

{"resultado": "Empleado no encontrado"}
```
This indicates that the employee's document has been deleted from the database.

With this, the whole CRUD process has been tested on documents of a collection in the MongoDB database.

The source code of this article's application is in the [tutorial-flask repository on the mongo4 branch on gitlab.](https://gitlab.com/ecrespo/tutorial-flask/tree/mongo4)

##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)


