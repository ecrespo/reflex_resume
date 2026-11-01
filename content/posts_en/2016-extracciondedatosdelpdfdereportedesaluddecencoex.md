Title: Extracting data from the Cencoex health report PDF  
Date: 2016-02-08 09:00    
Category: Tutorial Python  
Tags: Python,Mongodb,Api restfull,Eve
lang: en
translation: true 


This article is a continuation of the articles on extracting data from a PDF, focused on the Cencoex report for the [health (broken link)](http://www.cencoex.gob.ve/images/stories/pdfs/estadisticas/Salud.pdf) area.

The following figure shows the aforementioned pdf:

![](./images/extracciondedatosdelpdfdereportedesaluddecencoex-1.png)

The previous PDF extraction articles are:  
1. [Extracting information from PDFs with Python (part 1).](/blog/extracciondeinformaciondepdfsconpython-1)  
2. [Extracting information from PDFs with Python (part 2).](/blog/extracciondeinformaciondepdfsconpython-2)  
3. [Extracting information from PDFs with Python (part 3).](/blog/extracciondeinformaciondepdfsconpython-3)  

For the Cencoex report PDF, there is the script already explained earlier that saves the information in a mongodb database called `cencoex` in a collection called salud. 

The following figure shows the documents of the collection:

![](./images/extracciondedatosdelpdfdereportedesaluddecencoex-2.png)

With this information stored in mongodb, a RESTful API will be created with Eve as explained in the [previous articles](/blog/tags).

The previous image shows that the documents have the following fields:  

- `_id`: The object identifier  
- `rif`: The RIF of the company that was assigned the dollars; the field is a string.  
- `monto`: Amount in dollars of the foreign currency allocation to that company; the field is a string.  
- `empresa`: The name of the company that was assigned the dollars; the field is a string.   
- `numero`: The assigned number that appears in the pdf; it is an integer.   

With this information the schema to access the data through Eve will be built.

Here is the `settings.py` file:
```python
#Configuracion de mongodb
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
#MONGO_USERNAME = 'user'
#MONGO_PASSWORD = 'user'
MONGO_DBNAME = 'cencoex'



RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
#Esquema
schema = {
    'numero': {
        'type': 'integer',
    },
    'rif': {
        'type': 'string',
        'maxlength': 11,
    },
    'empresa': {
        'type': 'string',
    },
    'monto': {
        'type': 'string',
    },
}



empresa = {
    'titulo': 'numero',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'numero'
    },

    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    'resource_methods': ['GET', 'POST'],

    'schema': schema
}

DOMAIN = {
    'salud': empresa,
}

```
As you can see, the domain is salud, which takes the company information, where the field to handle is the number. The schema was defined to handle the same fields as the collection. 


The `run.py` file is what starts the RESTful API:
```python
#!/usr/bin/env python

from eve import Eve
app = Eve()

if __name__ == '__main__':
    app.run()

```
To start the RESTful API run `run.py`:
```
python run.py
```

Accessing http://127.0.0.1:5000/ with the restclient client gives the following:

![](./images/extracciondedatosdelpdfdereportedesaluddecencoex-3.png)

To access the list of elements of the RESTful API, enter http://127.0.0.1:5000/salud/ in the client; the following figures show the result:

![](./images/extracciondedatosdelpdfdereportedesaluddecencoex-4.png)

![](./images/extracciondedatosdelpdfdereportedesaluddecencoex-5.png)

As the figure shows, a JSON with the documents of the mongodb database is returned.

Now we want to access the first number of the report as follows:
``` 
http://127.0.0.1:5000/salud/1
```
The result is shown in the following two figures:

![](./images/extracciondedatosdelpdfdereportedesaluddecencoex-6.png)

![](./images/extracciondedatosdelpdfdereportedesaluddecencoex-7.png)


Of course, this is a demonstration, but you can try searching by other fields. 

Django could be used with the RESTful API framework in order to improve how those mongodb database documents are queried.

The idea was to show how easy it is to publish the data of a Cencoex report. In fact, the most complicated part is extracting the data from a PDF, and information is even lost depending on the document format used; as shown in a previous article, the document is an Excel spreadsheet and information was indeed lost in the extraction. 

Institutions that have this information in a database can make the fields they require public as read-only in a RESTful API, which removes the process of searching for information in PDFs. 


Here is the proposal that the free software community is working on, on [github by the Venezuelan Free Software community](https://github.com/cslve/gobiernoabierto).


Here are some youtube videos:
Open Government:

[https://youtu.be/wcao6i1yDQ4 (broken link)](https://youtu.be/wcao6i1yDQ4 "https://youtu.be/wcao6i1yDQ4")

<iframe width="560" height="315" src="https://www.youtube.com/embed/wcao6i1yDQ4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



Open Government Partnership:

[https://youtu.be/QbGDoV_HoFY (broken link)](https://youtu.be/QbGDoV_HoFY "https://youtu.be/QbGDoV_HoFY")  

<iframe width="560" height="315" src="https://www.youtube.com/embed/QbGDoV_HoFY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


[https://youtu.be/Mj7NvmFr5i0 (broken link)](https://youtu.be/Mj7NvmFr5i0 "https://youtu.be/Mj7NvmFr5i0")

<iframe width="560" height="315" src="https://www.youtube.com/embed/Mj7NvmFr5i0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)