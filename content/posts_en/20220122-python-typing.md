Title: Introduction to annotations and types in Python
Date:  2022-01-22 12:00
Category: Tutorial Python
Tags: python,typing,pydantic,mypy
lang: en
translation: true
Slug: python_typing
Authors: Ernesto Crespo
Summary: Learn how to use static type checking and best practices


Previous articles covered the use of dataclass, pydantic and orjson and how to use typing; this article explains best practices:

* [Dataclasses in Python](/blog/python_dataclass)
* [Data validation with Pydantic](/blog/python_pydantic)
* [Introduction to orjson](/blog/python_orjson)

Besides helping to understand the code better, type checking makes it easier to detect errors quickly and automatically using, for example, mypy. Type checking was added to Python in version 3.5. 


This article is based on the article in English: [Improving Your Python Projects With Type Hints (broken link)](https://betterprogramming.pub/improving-your-python-projects-with-type-hints-63cbdb16d97c)

## Typing syntax

Python supports type annotations for the basic variables supported by the language: str, int, float, bool and None. It comes built into the typing library.

### Variable annotation

You can indicate the type of a variable by using the colon ":". For example: 


```python 

from typing import List

nombre: str = 'Pedro'
edad: int = 24
altura_mts: float = 1.7
colegas: List[str] = ['Jane', 'John']

```

The type and the value that the variable will have are defined. 


### Annotation in functions

In the case of functions, you can add annotations to the argument variables, as well as to the function's return value. 


```python 

from typing import Dict, List
import math 

def calc_area_circulo(radio: float) -> float:
    return math.pi*(radio**2)
  
def send_email(
    subject: str,
    body: str,
    recipients: List[str],
    cache: Dict[str, str]
) -> bool:
  
    # .... 
    # Devuelve True o False el envío de un correo

    return True 
```

The first function takes the radius as a float argument and returns the area of the circle, which is also a float. 

The following example defines a function that receives subject (string), body (string), recipients (list of strings) and cache (a dictionary with string keys and string values), and the function returns a boolean. 

### Using special types

There is a series of types that complement the basic ones: 

* Any: 
* Literal: 
* Union
* TypeDict
* NoReturn
* Final


#### Any 

A variable of type Any is compatible with all the basic types. 

```python 

from typing import Any

resultado: Any = "Procesado"
  
resultado = 10

estatus: str = "Pendiente"

estatus = resultado


```
In the first case the variable resultado of type Any is defined and assigned a string, then it is assigned an integer, which is not a problem because the Any type supports it. Then the variable estatus of type string is defined and assigned a string, and then resultado is assigned to the variable estatus without problems; this is not a problem either because resultado is of type any.


#### Literal

The literal type is used to indicate that a variable has a value equal to one of the indicated values (types). 

```python 


from typing import Literal


GENERO = Literal["hombre", "mujer", "no especificado"]

def crear_usuario(
    nombre: str,
    apellido: str,
    genero: GENERO,
) -> Dict[str, str]:
    return {
        "nombre": nombre,
        "apellido": apellido,
        "genero": genero
    }

crear_usuario("John", "Doe", "hombre")

{'nombre': 'John', 'apellido': 'Doe', 'genero': 'hombre'}

```

A list is defined for the gender of literal type, and the value is one of those defined (hombre, mujer, no especificado). 


#### Union

Some variables sometimes need two basic types. 

```python 

from typing import Union


def get_temperatura() -> Union[int, float]:
    return 20.8  # funciona también con 20.

```

A function is defined that returns an integer or a float; this is achieved using Union. 


#### TypedDict

TypedDict lets you define a dictionary data type. 

```python 

from typing import TypedDict, Union


class Card(TypedDict):
    rank: Union[str, int]
    suit: str

# The Card class now has behaviours of both TypedDict and dict classes

# Card can be used to annotate a variable
ace_of_spade: Card = {'rank': 'A', 'suit': '♤'}

# or can be instantiated
ace_of_spade = Card(rank='A', suit='♤')

print(ace_of_spade)

{'rank': 'A', 'suit': '♤'}

```

#### NoReturn

NoReturn is similar to void in other programming languages; in my case I used to use None when a function returns nothing. 

```python 

from typing import NoReturn

def hola1() -> None:
    print("Hola Mundo!")

def hola2() -> NoReturn:
    print("Hola Mundo!")

```

Two hola functions are defined, the first as None and the second as NoReturn, which is how a function that does not return a value should be defined. 

#### Final


This data type is defined so that a value is not redefined. 

```python 


from typing import Final


MIN_NOMBRE_LONG: Final = 2

# mypy reporta error por que se le está asignando un nuevo valor a la
# variable
MIN_NOMBRE_LONG += 1


class Validador(object):
    MIN_NOMBRE_LONG: Final[int] = 4

class UserValidador(Validador):
    # El interprete marca una bandera en esta línea
    MIN_NOMBRE_LONG = 3

```

### Using type checkers

One of the most widely used type checkers is mypy. It can be installed using pip:

```bash 

pip install mypy 

```

To use it, simply call mypy and pass it the file to check. 

The code to validate is shown below: 

```python 

#!/usr/bin/env python3

from typing import Literal, Dict


GENERO = Literal["hombre", "mujer", "no especificado"]


def crear_usuario(
    nombre: str,
    apellido: str,
    genero: GENERO,
) -> Dict[str, str]:
    return {
        "nombre": nombre,
        "apellido": apellido,
        "genero": genero
    }


crear_usuario("John", "Doe", "hombre")
crear_usuario("Jane", "Doe", "mujer")
crear_usuario("John", "Doe", "x")

```

This code will return an error when trying to create a user with gender x.

```bash 

mypy   pruebas_typing.py
content/code/pruebas_typing.py:23: error: Argument 3 to "crear_usuario" has incompatible type "Literal['x']"; expected "Union[Literal['hombre'], Literal['mujer'], Literal['no especificado']]"
Found 1 error in 1 file (checked 1 source file)
```

This is the error message returned when trying to set the value x as the gender. 


Type notation and checking make it easier to validate that a variable always has a data type and does not change. It happened to me not long ago: I wrote a function that returned a list, and some time later a developer changed the list to a dictionary, and the function worked, but when running mypy on it. 



---
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
