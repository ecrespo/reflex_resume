Title: Back to basics, OOP in Python (part 6)
Date: 2016-12-31 15:00
Category: Tutorial Python
Tags: Python,POO
lang: en
translation: true

Continuing with the series of articles about [Object-Oriented Programming in Python](/blog/tags).

This article explains the use of the `classmethod` decorator, which receives the class as its argument. 

There is an abstract class called figura (shape), which has the following decorators:

- `abstractmethod`: Abstract methods that contain nothing, only the description of the methods; these methods are: area, perimetro and quienEresTu.  
- `abstractproperty`: Abstract property; in this case the color method is defined.   
- `property`: The color method returns the color as a property.  
- `@color.setter`: Defines a new color.   
- `classmethod`: __subclasshook__ is defined as a classmethod, which lets you customize the behavior of Issubclass without having to register a subclass of the abstract class (this method must return True, False or NotImplemented).  

Then the Rectangulo class is created, inheriting from the abstract class Figura, and then the Cuadrado class is created, inheriting from the Rectangulo class.


The code of the Figura class is shown below:

```python
#Se importa sqrt de math



from math import sqrt



#Se importa ABCMeta, abstractmethod, abstractproperty



from abc import ABCMeta, abstractmethod,abstractproperty



#Interface



class Figura(object):



    __metaclass__ = ABCMeta




    @abstractmethod



    def area(self):



        """Calcula el area"""



        pass




    @abstractmethod



    def perimetro(self):



        """Calcula el perimetro"""



        pass




    @abstractmethod



    def quienEresTu(self):




        """Devuelve el mensaje de quien es el objeto"""



        print (u"Soy una forma y un método abstracto ")




    @abstractproperty



    def color(self):



        pass




    @property



    def color(self):



        pass




    @color.setter



    def color(self,valor):



        pass




    @classmethod



    def __subclasshook__(cls, C):



        return NotImplemented

```



The code of the Rectangulo class is shown:


```python

class Rectangulo(Figura):

    def __init__(self,ancho, alto):

        """Define los atributos de rectangulo"""

        self.ancho, self.alto = ancho, alto

        super(Rectangulo,self).__init__()

        self.__color = "rojo"



    def area(self):

        """Devuelve el area"""

        return self.ancho*self.alto



    def perimetro(self):

        """devuelve el perimetro"""

        return 2*self.ancho+2*self.alto



    @property

    def color(self):

        """Devuelve el atributo color"""

        return self.__color



    @color.setter

    def color(self,valor):

        """Define el color del rectangulo"""

        self.__color = valor



    def quienEresTu(self):

        """devuelve que es el objeto"""

        print (u"Soy un Rectangulo")
```

The code of the Cuadrado class is shown below:
```python
class Cuadrado(Rectangulo):

    def __init__(self,largo):
        """Define el largo del cuadrado y se lo pasa a la clase rectangulo"""
        self.largo = largo
        super(Cuadrado,self).__init__(largo,largo)

    def area(self):
        """DEvuelve el area del cuadrado"""
        return self.largo*self.largo
```

Finally, the use of the classes is shown:
 
```python


if __name__ == '__main__':


    r = Rectangulo(5,6)


    print ("Es una subclase rectangulo de shape?:",issubclass(Rectangulo,Figura))


    print ("Es una subclase cuadrado de shape?:",issubclass(Cuadrado,Figura))


    print ("Es una subclase cuadrado de rectangulo?:",issubclass(Cuadrado,Rectangulo))


    print ("Es una subclase rectangulo de cuadrado?:",issubclass(Rectangulo,Cuadrado))


    print ("r es una instancia de rectangulo?:",isinstance(r,Rectangulo))


    print ("r es una instancia de cuadrado?:",isinstance(r,Cuadrado))


    print ("Area del rectangulo:",r.area())


    print("Color del rectangulo:",r.color)


    r.color = "Black"


    print("Color del rectangulo:",r.color)


    print ("Perimetro del rectangulo",r.perimetro())


    r.quienEresTu()


    sq = Cuadrado(5)


    print ("Area del cuadrado:",sq.area())


    print ("Perimetro del cuadrado:",sq.perimetro())

```



Running the code gives the following result:

```
Es una subclase rectangulo de shape?: True
Es una subclase cuadrado de shape?: True
Es una subclase cuadrado de rectangulo?: True
Es una subclase rectangulo de cuadrado?: False
r es una instancia de rectangulo?: True
r es una instancia de cuadrado?: False
Area del rectangulo: 30
Color del rectangulo: rojo
Color del rectangulo: Black
Perimetro del rectangulo 22
Soy un Rectangulo
Area del cuadrado: 25
Perimetro del cuadrado: 20

```
You can find the complete code of the classes on gitlab at the following [link](https://gitlab.com/ecrespo/tutorial-poo/blob/master/ej13.py).



##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)




