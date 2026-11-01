Title: CRUD using Flask for MongoDB (part 3).  
Date: 2016-09-28 11:00
Category: Tutorial Python
Tags: Python,MongoDB,Flask,Docker,CRUD
lang: en
translation: true  

Continuing with the series of articles on accessing mongodb from Flask. 

The previous articles are:

- [Querying MongoDB from Flask (part 1)](/blog/consultaamongodbdesdeflask-1) 
- [Querying MongoDB from Flask (part 2 - pagination)](/blog/consultaamongodbdesdeflask-2)

To check the articles related to this one, see:

- [Articles about Docker](/blog/tags)
- [Articles about MongoDB](/blog/tags)
- [Articles about Flask](/blog/tags)


The mongodb database contains the following employee data:
```
[{"edad": 29, "nombre": "Jane Doe", "dni": 8, "sexo": "Femenino", "_id": {"$oid": "57ebbce45fd2bbeffc51330b"}}, {"edad": 39, "nombre": "John Doe", "dni": 7, "sexo": "Masculino", "_id": {"$oid": "57ebbd195fd2bbeffc51330c"}}, {"edad": 55, "nombre": "Pedro Perez", "dni": 6, "sexo": "Masculino", "_id": {"$oid": "57ebbd505fd2bbeffc51330d"}}, {"edad": 65, "nombre": "Petra", "dni": 5, "sexo": "Femenino", "_id": {"$oid": "57ebbd6b5fd2bbeffc51330e"}}, {"edad": 18, "nombre": "Luis Gonzalez", "dni": 4, "sexo": "Masculino", "_id": {"$oid": "57ebc34d5fd2bbeffc51330f"}}, {"edad": 28, "nombre": "Carolina", "dni": 3, "sexo": "Femenino", "_id": {"$oid": "57ebc3715fd2bbeffc513310"}}, {"edad": 34, "nombre": "Luissana", "dni": 2, "sexo": "Femenino", "_id": {"$oid": "57ebc3935fd2bbeffc513311"}}, {"edad": 43, "nombre": "Neg", "dni": 1, "sexo": "Masculino", "_id": {"$oid": "57ebc4b85fd2bbeffc513312"}}]
```
For this article a CRUD will be developed and tested with Flask using mongodb as the database.

#### Insert an employee into the collection

The code to insert an employee is shown below:
```

#Se define la funcion add con metodo get


@app.route('/add',methods=['GET'])


def add():


    #Se toma el nombre, sexo, edad y dni como argumentos del url


    nombre = str(request.args['nombre'])


    sexo = str(request.args['sexo'])


    edad = int(request.args['edad'])


    dni = int(request.args['dni'])





    #Se usa la coleccin empleados.


    empleados = mongo.db.empleados


    #Se inserta el documento a la coleccion


    empleados.insert({'nombre':nombre,'sexo':sexo,'edad':edad,'dni':dni})


    #Se retorna que el usuario fue agregado.


    return jsonify({'resultado': 'Usuario agregado' })

```

#### Find an employee in the collection

The code to find an employee in the collection is shown below:
```
#Se crea la funcion find con metodo get. @app.route('/find',methods=['GET']) def find():     #Se obtiene el nombre como argumento del url.     nombre = str(request.args['nombre'])     #Se conecta a la coleccion empleados.     empleados = mongo.db.empleados     #Se busca el nombre en la coleccion.     resultado = empleados.find_one({'nombre':nombre})     #Y se devuelve el resultado.     return dumps(resultado)
```

#### Update an employee in the collection

The code to update an employee is shown below:

```
#Se define la funcion update con metodo get que actualiza un documento de la

#coleccion.

@app.route('/update',methods=['GET'])

def update():

    #Se toma el nombre,edad y dni como argumentos.

    nombre = str(request.args['nombre'])

    edad = int(request.args['edad'])

    dni = int(request.args['dni'])

    #Se conecta a la coleccion.

    empleados = mongo.db.empleados

    #Se busca el nombre en los documentos.

    empleado = empleados.find_one({'nombre':nombre})

    #Se actuliza la edad, el dni.

    empleado['edad'] = edad

    empleado['dni'] = dni

    #Se salva el empleado en la coleccion.

    empleados.save(empleado)

    #Se devuelve que el usuario ha sido actualizado.

    return dumps({'resultado': 'Usuario actualizado'})

```

#### Remove an employee from the collection


The code to remove an employee from the collection is the following:

```
#Se define la funcion delete.


#donde en el url se pasa el nombre del empleado a borrar


@app.route('/delete/<nombre>')


def delete(nombre):


    #Se conecta a la coleccion empleados.


    empleados = mongo.db.empleados


    #Se busca el documento del empleado por el nombre.


    empleado = empleados.find_one({'nombre':nombre})


    #Se remueve el empleado de la coleccion.


    empleados.remove(empleado)


    #Se devuelve el resultado.


    return dumps({'resultado': 'Usuario removido'})

```

Note that the way of passing arguments to the delete function is different from the other functions.


Building the Docker image and running the containers
The Dockerfile and docker-compose.yml files were explained in the first article of this section (the links are at the beginning of this article).

To build the docker image, run:
```
docker-compose build
```
To run the application and mongodb containers, run:
```
docker-compose up
```

Testing the CRUD

To create an employee, open the following URL in the browser:
``` 
http://localhost:5000/add?nombre=Ernesto&dni=33&edad=11&sexo=Masculino
```
It returns a json:
```
{
  "resultado": "Usuario agregado"
}
```

To find the employee added earlier, open the browser at the URL:
```
http://localhost:5000/find?nombre=Ernesto
```
It returns the following json:
```
{"_id": {"$oid": "57ec8714b7cd2f00565e8784"}, "sexo": "Masculino", "edad": 11, "nombre": "Ernesto", "dni": 33}
```

To update the employee Ernesto, open the browser at the following URL:
```
http://localhost:5000/update?nombre=Ernesto&edad=45&dni=50
```
Here the age and the dni are updated.

This returns the following json:
```
{"resultado": "Usuario actualizado"}
```
Finally, the employee will be deleted by opening the browser at the following URL:
```
http://localhost:5000/delete/Ernesto
```
This returns the following json:
```
{"resultado": "Usuario removido"}
```

Note that for delete the way of passing the URL is different from the others that have been run.



The source code of this article is in the [mongo3 branch on gitlab.com](https://gitlab.com/ecrespo/tutorial-flask/tree/mongo3/)

##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)


