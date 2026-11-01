Title: Dataclasses in Python
Date:  2022-01-16 15:45
Category: Tutorial Python
Tags: dataclass
lang: en
translation: true
Slug: python_dataclass
Authors: Ernesto Crespo
Summary: This article covers how to create dataclasses and what they are useful for

The articles this article is based on are: 

* [Data Classes in Python (broken link)](https://justgiveacar.medium.com/data-classes-in-python-991a3f68ddf9)
* [9 Reasons Why You Should Start Using Python Dataclasses (broken link)](https://towardsdatascience.com/9-reasons-why-you-should-start-using-python-dataclasses-98271adadc66)


Data classes in python let you write less code, and they are supported in python from version 3.7 onward. 


## Regular classes

We will start with a simple class in Python called perro (dog), with an init method that takes the class arguments as attributes:

* Nombre: String type.
* Raza: String type.
* Edad: Integer type.


```python 

class Perro:
    nombre: str
    raza: str
    edad: int
      
    def __init__(self, nombre, raza, edad):
        self.nombre = nombre
        self.raza = raza
        self.edad = edad

```

Three pets are instantiated with the Perro class: 

```python 

mascota1 = Perro('RUDY', 'Terrier Australiano', 2)
mascota2 = Perro('TEDDY', 'bichón frisé', 2)
mascota3 = Perro('TEDDY', 'bichón frisé', 2)

```

Pet 2 is compared with pet 3:

```python
mascota2 == mascota3

False
```

Even though both pets have the same data in their attributes, a comparison returns false. 

One option is to use a method that compares attribute by attribute. 



The contents of mascota2 are printed: 
```python

print(mascota2)


<__main__.Perro object at 0x7f9c104e7640>

```

What is shown is the in-memory id of the Perro instance.

To show the contents, each attribute is accessed: 
```python
print(mascota2.nombre,mascota2.raza,mascota2.edad)

TEDDY bichón frisé 2


```

## Data classes

To use dataclass you have to install it via pip: 

```bash 
pip install dataclasses
```

We will take the same Perro class, this time using a dataclass decorator. 

Import dataclass: 

```python

from dataclasses import dataclass

```

The Perro class is defined with the same attributes as the previous class: 

```python 

@dataclass
class Perro:
    nombre: str
    raza: str
    edad: int

```

The class is defined and each attribute only gets its type, nothing more. 

Now the pets are created: 

```python 

mascota1 = Perro('RUDY', 'Terrier Australiano', 2)
mascota2 = Perro('TEDDY', 'bichón frisé', 2)
mascota3 = Perro('TEDDY', 'bichón frisé', 2)

```

Now, when comparing pet 2 and 3, it will not return false: 

```python 

print(mascota2 == mascota3)

True

```

Next, the contents of mascota2 are printed: 

```python 

print(mascota2)

Perro(nombre='TEDDY', raza='bichón frisé', edad=2)

```

Now it does not return the Id; it returns the perro class with the attribute values that were assigned to mascota2.

You can also access the attribute data: 

```python 
print(mascota2.nombre,mascota2.raza,mascota2.edad)

TEDDY bichón frisé 2


```

You can add the __repr__ method to the class to give the information as a formatted string:

```python 
@dataclass
class Perro:
    nombre: str
    raza: str
    edad: int
    
    def __repr__(self):
        return f"{self.nombre} {self.raza} ({self.edad})"


mascota1 = Perro('RUDY', 'Terrier Australiano', 2)
mascota2 = Perro('TEDDY', 'bichón frisé', 2)
mascota3 = Perro('TEDDY', 'bichón frisé', 2)


print(mascota2)

TEDDY bichón frisé (2)

```


Besides comparing whether they are equal, you can compare whether pet 1 is greater than pet 2. 

```python

print(mascota1  > mascota2)
```

This returns an error; this comparison is not supported:

```bash
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
/tmp/ipykernel_603591/468771088.py in <module>
----> 1 mascota1  > mascota2

TypeError: '>' not supported between instances of 'Perro' and 'Perro'
```

To be able to compare them, the __post_init__ method is needed.  The attribute used for the comparison will be the age; the code will look like this: 

```python 

from dataclasses import dataclass, field

@dataclass
class Perro:
    sort_index: int = field(init=False)
    nombre: str
    raza: str
    edad: int
    
    def __repr__(self):
        return f"{self.sort_index} {self.nombre} {self.raza} ({self.edad})"  
    
    def __post_init__(self):
      self.sort_index = self.edad

```

The arguments are shown: 

```python 

mascota1 = Perro('RUDY', 'Terrier Australiano', 3)
mascota2 = Perro('TEDDY', 'bichón frisé', 2)
print(mascota2)

#2 TEDDY bichón frisé (2)


print(mascota2.sort_index,mascota2.nombre,mascota2.raza,mascota2.edad)

#2 TEDDY bichón frisé 2

```

Let's try comparing again: 

```python 
print(mascota1 > mascota2)
```

It returns an error: 
```bash
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
/tmp/ipykernel_603591/4142115589.py in <module>
----> 1 mascota1 > mascota2

TypeError: '>' not supported between instances of 'Perro' and 'Perro'
```


## Read-only classes

You can create read-only classes to prevent their initial values from being modified.


To fix this error, the order argument is used in the decorator, and read-only is defined:

```python 

@dataclass(order=True, frozen=True)
class Perro:
    sort_index: int = field(init=False)
    nombre: str
    raza: str
    edad: int
    
    def __post_init__(self):
      object.__setattr__(self, 'sort_index', self.edad)

mascota1 = Perro('RUDY', 'Terrier Australiano', 3)
mascota2 = Perro('TEDDY', 'bichón frisé', 2)
```

Now the comparison is made and it does not return an error: 

```python 
print(mascota1  > mascota2)

True
```

The contents of pet 2 are shown: 

```python 

print(mascota2)


Perro(sort_index=2, nombre='TEDDY', raza='bichón frisé', edad=2)


```

If you try to assign a value to pet 2's age, it will return an error:

```python 

mascota2.edad = 4

```

```bash 

---------------------------------------------------------------------------
FrozenInstanceError                       Traceback (most recent call last)
/tmp/ipykernel_603591/927787478.py in <module>
----> 1 mascota2.edad = 4

<string> in __setattr__(self, name, value)

FrozenInstanceError: cannot assign to field 'edad'

```

As you can see, dataclasses can make it easier to validate the data in the attributes of the objects you define. The next article will cover the pydantic module, which extends this data validation feature. 

---
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)