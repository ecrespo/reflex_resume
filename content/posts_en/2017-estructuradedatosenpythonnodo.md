Title: Data structures in Python (Node)
Date: 2017-03-07 09:00
Category: Tutorial Python
Tags: Python,Estructura de datos
lang: en
translation: true

I remember at the Universidad de Carabobo how we were taught Data structures and ADTs (abstract data types) in Digital Computing II (programming methodology). Among them:

- Linked list
- Doubly linked list
- Circular list
- etc.

The course was taught with Turbo Pascal 6.0, Modula 3, Oberon and Component Pascal.

In this case we will build the base data structure called a node; in the next article the node will be used to build a linked list.

A Node has the following attributes and methods:

- Attributes:
    - dato: data.
    - prox: next node.
- Methods:
    - getter dato: Returns the data.
    - setter dato: Sets the value of dato.
    - getter proximo: Returns the value of proximo.
    - setter proximo: Returns the value of proximo.

To test the node data structure (node object), 3 instances are created with the data (apple, pear and grape), each pointing to the next node; the first node points to `None`.

Here is the code of the `nodos.py` module that contains the `Nodo` class:

```python
#!/usr/bin/env python3



class Nodo(object) :

    """Objeto Nodo"""

    def __init__( self, dato,prox=None ) :

        """Construye el objeto nodo con los atributos 

        datos, prox, prev"""

        self.__dato = dato

        self.__prox = prox

    

    def __str__(self):

        return 'Nodo ['+str(self.__dato)+']'



    @property

    def dato(self):

        return self.__dato

    

    @dato.setter

    def dato(self,dato):

        self.__dato = dato



    @property

    def proximo(self):

        return self.__prox



    @proximo.setter

    def proximo(self,prox):

        self.__prox = prox 





if __name__ == '__main__':

    nodo1 = Nodo("manzana")

    nodo2 = Nodo("pera",nodo1)

    nodo3 = Nodo("uva",nodo2)

    print (nodo1.dato,nodo1.proximo)

    print (nodo2.dato,nodo2.proximo)

    print (nodo3.dato,nodo3.proximo)
    print (nodo1)
    print (nodo2)
    print (nodo3)
    
```

Running the script gives the following:
```python
('manzana', None)
('pera', <__main__.Nodo object at 0x7f174f358290>)
('uva', <__main__.Nodo object at 0x7f174f3582d0>)
Nodo [manzana]
Nodo [pera]

Nodo [uva]
```
The next article will explain inheritance of the Nodo class with the listaenlazada class.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
