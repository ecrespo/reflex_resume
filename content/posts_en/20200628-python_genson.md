Title: Generating a JSON schema from an XML file with genson, lxml and xmltodict.
Date:  2020-06-28 10:55
Category: Tutorial de Python
Tags: Python, Genson,lxml, xmltodict
lang: en
translation: true
Slug: python-genson-xml-json_schema
Authors: Ernesto Crespo
Summary: This article explains how to use genson to obtain a json schema from a json file or an xml file.


The genson page is [here](https://pypi.org/project/genson/) and on [github](https://github.com/wolverdude/genson/).  The first thing to do is install genson , as well as lxml and xmltodict . 


# Installation

Install genson, lxml and xmltodict:

```bash 

pip install genson lxml xmltodict

```

# CLI Tool 

Genson can be used as a command to generate a json schema. Its help output is shown below: 

```bash 

$ genson --help

usage: genson.py [-h] [-d DELIM] [-i SPACES] [-s SCHEMA] [-$ URI] ...

Generate one, unified JSON Schema from one or more JSON objects and/or JSON
Schemas. It's compatible with Draft 6 and above.

positional arguments:
  object                files containing JSON objects (defaults to stdin if no
                        arguments are passed)

optional arguments:
  -h, --help            show this help message and exit
  -d DELIM, --delimiter DELIM
                        set a delimiter - Use this option if the input files
                        contain multiple JSON objects/schemas. You can pass
                        any string. A few cases ('newline', 'tab', 'space')
                        will get converted to a whitespace character. If this
                        option is omitted, the parser will try to auto-detect
                        boundaries
  -i SPACES, --indent SPACES
                        pretty-print the output, indenting SPACES spaces
  -s SCHEMA, --schema SCHEMA
                        file containing a JSON Schema (can be specified
                        multiple times to merge schemas)
  -$ URI, --schema-uri URI
                        the value of the '$schema' keyword (defaults to
                        'http://json-schema.org/schema#' or can be specified
                        in a schema with the -s option). If 'NULL' is passed,
                        the "$schema" keyword will not be included in the
                        result.

```

# GenSON Python API

Now the use of the genSON API for Python is shown.

## Examples

For all the examples a list of Python modules will be imported: 

* json
* lxml parse
* lxml XMLParse
* xmltodict 
* genson SchemaBuilder

```python 

import json
from lxml.etree import parse
from lxml.etree import XMLParser
import xmltodict
import genson
from genson import SchemaBuilder
```


### A list of dictionaries

There is a list of dictionaries of the following form: 

```python 

templist = [{
 'name':'Sam',
},
{
 'name':'Jack',
}]

templist
[{'name': 'Sam'}, {'name': 'Jack'}]

```

Convert the list to JSON: 

```python 

jsonf = json.dumps(templist)
jsonf 

'[{"name": "Sam"}, {"name": "Jack"}]'

```

Create the SchemaBuilder instance, add the object and show the schema of that object:

```python

builder = SchemaBuilder()
builder.add_object(json.loads(jsonf))
builder.to_schema()

{'$schema': 'http://json-schema.org/schema#',
 'type': 'array',
 'items': {'type': 'object',
  'properties': {'name': {'type': 'string'}},
  'required': ['name']}}

```

The schema shows that the object is of type array, that it has items of type object, and that it has a required field called name, and that name is of type string.


### Dictionaries added as individual objects

Two dictionaries that have the key "hi" with different values (string type and integer) will be added:

```python 

builder = SchemaBuilder()
builder.add_object({"hi": "there"})
builder.add_object({"hi": 5})
builder.to_schema()

{'$schema': 'http://json-schema.org/schema#',
 'type': 'object',
 'properties': {'hi': {'type': ['integer', 'string']}},
 'required': ['hi']}
```

Now the schema returns that it is of type object, and that it has a required field named "hi", but of type integer and string.

### A list with two items of different types (String, integer)

```python 

builder = SchemaBuilder()
builder.add_object(['one', 1])
builder.to_schema()

{'$schema': 'http://json-schema.org/schema#',
 'type': 'array',
 'items': {'type': ['integer', 'string']}}

```

The schema it generates is of type array, with items of type integer and string.


### Real case: NASA data

At the following [link](http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/www/repository.html#nasa) you will find the NASA data set converted to a flat xml file. You can download the xml file directly from [here](http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/nasa/nasa.xml).

The data will not be processed or restructured, since that would require knowing the data model of the research. 

The steps are the following: 

1. Create the xml parser with UTF-8 encoding

```python 

parser = XMLParser(encoding='UTF-8')

```

2. Read the xml data from the file and convert it into a dictionary: 

```python 

with open("../datos/nasa.xml", "r") as f:
  xx = xmltodict.parse(f.read())
```

3. Create the SchemaBuilder instance, pass it the dictionary and generate the schema:

```python 
sb = genson.SchemaBuilder()
sb.add_object(xx)
sb.to_schema()

{'$schema': 'http://json-schema.org/schema#',
 'type': 'object',
 'properties': {'datasets': {'type': 'object',
   'properties': {'dataset': {'type': 'array',
     'items': {'type': 'object',
      'properties': {'@subject': {'type': 'string'},
       '@xmlns:xlink': {'type': 'string'},
       'title': {'type': 'string'},
       'altname': {'type': 'array',
        'items': {'type': 'object',
         'properties': {'@type': {'type': 'string'},
          '#text': {'type': 'string'}},
         'required': ['#text', '@type']}},
       'reference': {'type': 'object',
................
```
Only a part of the schema is shown; what will be done next is to remove the "@" that appears in some of the data.

For that there is a postprocessing function:

```python 

def postprocessor(path,key,value):
    try: 
        if key.startswith("@"):
            key = "_" + key[1:]
        return key,value 
    except (ValueError, TypeError):
        return key,value
``` 
It takes the dictionary keys and changes those that start with "@" to "_". 

4. Read the xml file data again, passing the function: 

```python 

with open("../datos/nasa.xml", "r") as f:
    xx = xmltodict.parse(f.read(),encoding="utf-8",postprocessor=postprocessor)

```

5. Create the SchemaBuilder instance, add the dictionary and generate the schema:

```python
sb = genson.SchemaBuilder()
sb.add_object(xx)
sb.to_schema()

{'$schema': 'http://json-schema.org/schema#',
 'type': 'object',
 'properties': {'datasets': {'type': 'object',
   'properties': {'dataset': {'type': 'array',
     'items': {'type': 'object',
      'properties': {'_subject': {'type': 'string'},
       '_xmlns:xlink': {'type': 'string'},
       'title': {'type': 'string'},
       'altname': {'type': 'array',
        'items': {'type': 'object',
         'properties': {'_type': {'type': 'string'},
          '#text': {'type': 'string'}},
         'required': ['#text', '_type']}}

..................

```

Now you can see that some keys were changed with a "_". 

With xmltodict, lxml and genson you can process data sets and restructure them into what is required to make their analysis easier.



####


Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
