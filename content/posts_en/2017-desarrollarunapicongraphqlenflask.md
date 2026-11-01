Title: Developing an API with GraphQL in Flask
Date: 2017-06-25 9:00
Category: Tutorial de Python
Tags: Python,Debian,Linux,Ubuntu,GraphQL,Flask,Flask-graphql
lang: en
translation: true

Continuing with the articles about [Flask](/blog/tags), where the last article was about how to [create a Restful API with Flask and MongoDB](/blog/apirestfulconflaskymongodb) .

This article covers the use of GraphQL to create an API. GraphQL is a data query language developed by Facebook and is an alternative to Rest (more information on [wikipedia](https://en.wikipedia.org/wiki/GraphQL)).

You can see the GraphQL library for Flask at the following [link](https://pypi.python.org/pypi/Flask-GraphQL). The article will explain the example that appears on the [official graphQL page for Flask (broken link)](https://bcb.github.io/graphql/flask) .

Installation:
```
#pip3 install flask graphene flask-graphql
```

Server script (`server.py`):

```python
#!/usr/bin/env python3

#Se importa flask, graphene y graphql.

from flask import Flask

from graphene import ObjectType, String, Schema

from flask_graphql import GraphQLView



#Se crea la clase Query que hereda de graphene ObjectType.

class Query(ObjectType):

    #Se define la descripcion

    hello = String(description='Hello')

    #Se define la funcion resolve_hello, se le pasa args, context e info.

    def resolve_hello(self, args, context, info):

        return 'World'



#Se define la funcion de la vista.

#que se le pasa el esquema con la clase Query.

view_func = GraphQLView.as_view('graphql', schema=Schema(query=Query))



#Se crea la app como instancia de la clase Flask.

app = Flask(__name__)

#Se define el url donde se le pasa la funcion de la vista

app.add_url_rule('/', view_func=view_func)



if __name__ == '__main__':

    #Se ejecuta flask.

    app.run()

```

When the script is run:

![](./images/desarrollarunapicongraphqlenflask-1.png)


Query it using `curl`:
```
curl -H 'Content-type: application/graphql' -d '{hello}' http://localhost:5000/
```
And it returns:
```
{"data":{"hello":"World"}}
```

From a python script:

Installing the necessary libraries:
```
#pip3 install gql requests
```

The `cliente.py` script:

```python

#!/usr/bin/env python3



#Se importa json

import json

#se importa ggl

from gql import gql, Client

from gql.transport.requests import RequestsHTTPTransport



#Se define el transport, se conecta el cliente.

transport = RequestsHTTPTransport('http://localhost:5000/')

client = Client(transport=transport)

#Se realiza una consulta buscando la  variable hello

response = client.execute(gql('{hello}'))



#muestra en pantalla la respuesta como un json.

print(json.dumps(response))

```

Run the script:
```python
python3 cliente.py 
{"hello": "World"}
```
In an [article on genbetadev they compare Restful APIs with GraphQL and why we need to stop using Restful APIs.](https://www.genbetadev.com/desarrollo-aplicaciones-moviles/por-que-deberiamos-abandonar-rest-y-empezar-a-usar-graphql-en-nuestras-apis) 
Future articles will expand on the use of GraphQL.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
