Title: Back to basics, OOP in Python (multiple inheritance) (part 7)  
Date: 2016-12-31 16:00  
Category: Tutorial Python    
Tags: Python,POO
lang: en  
translation: true  


Continuing with the [articles on object-oriented programming with python](/blog/tags), this time I will cover the case of multiple inheritance.

The following figure shows the UML diagram:

![](./images/volviendoalobasicopooenpythonmultipleherencia7-1.png)

The classes and what they inherit from are:  
- Direccion(object): Has an init method that receives the arguments calle, ciudad, estado and codigo.  
- Contacto(object): Has an init method that receives the arguments nombre and correo.  
- Amigo(Contacto,Direccion): Has an init method that receives the arguments nombre, correo, telefono, calle, ciudad, estado and codigo. 
- ListaContactos: Has a buscar method that receives a name as an argument.  

**ListaContactos class:**

```python
class ListaContactos(list):


    def buscar(self,nombre):


        '''Retorna todos los contactos que contengan el nombre'''


        contactos_encontrados = []


        for contacto in self:


            if nombre in contacto.nombre:


                contactos_encontrados.append(nombre)


        return contactos_encontrados

```

**Direccion class**:

```python 

class Direccion(object):


    def __init__(self,calle, ciudad,estado, codigo):


        '''Inicializa la clase con la calle, ciudad, estado y codigo postal)'''


        self.calle = calle


        self.ciudad = ciudad


        self.estado = estado


        self.codigo = codigo

```

**Contacto class:**
 
```
class Contacto(object):


    '''Clase contacto que guarda una lista de los contactos e inicializa con el nombre y el correo del contacto'''


    todos_contactos  = ListaContactos()





    def __init__(self,nombre, correo):


        self.nombre = nombre


        self.correo = correo


        Contacto.todos_contactos.append(self)

```

**Amigo class:**
 
```
class Amigo(Contacto,Direccion):


    def __init__(self,nombre, correo, telefono,calle,ciudad,estado,codigo):


        Contacto.__init__(self,nombre,correo)


        self.telefono = telefono


        Direccion.__init__(self,calle,ciudad,estado,codigo)


```


The instantiation of the amigo class is shown below: 
 
```
contacto = Amigo("Ernesto","seraph2@contacto.com","04155556565","paez","guacara","carabobo","2015")


print(contacto.nombre,contacto.correo,contacto.telefono,contacto.calle,contacto.ciudad,contacto.estado,contacto.codigo)
```

When you run the program you get the following output:
```
Ernesto seraph2@contacto.com 04155556565 paez guacara carabobo 2015
```

The full code for this article is on gitlab at the following [link](https://gitlab.com/ecrespo/tutorial-poo/blob/master/ej17.py).

##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)




