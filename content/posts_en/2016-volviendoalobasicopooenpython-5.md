Title: Back to basics, OOP in Python (part 5)  
Date: 2016-12-19 09:00  
Category: Tutorial Python    
Tags: Python,POO
lang: en
translation: true


Continuing with the articles on Object-Oriented Programming in Python, in this case we will use what was covered in [part 4 of the series](/blog/volviendoalobasicopooenpython-4), where a `Punto2D` class was created along with a child class `Punto3D` that inherited from `Punto2D`.

In this case new concepts will be introduced:  
- metaclasses (abstract class)
- abstract method:   

With the abstract class, a class is defined with its abstract methods, which do nothing and only declare the methods; then that class is inherited and the methods that were defined as abstract are implemented. 

In this case the abstract class `ADTPunto` is created, which defines a series of methods; then the class Punto is created, inheriting from `ADTPunto`, where the methods defined in the abstract class are implemented. The abstract class ends up being like an interface for a class. 

The code of the abstract class `punto` is shown below: 

```python

from abc import ABCMeta, abstractmethod


class ADTPunto (object):


    __metaclass__ = ABCMeta



    @abstractmethod


    def ValorX(self):


        pass



    @abstractmethod


    def ValorY(self):


        pass



    @abstractmethod


    def mover(self,puntoNuevo):


        pass



    @abstractmethod


    def reset(self):


        pass



    @abstractmethod


    def distanciaOtroPunto(self,punto):


        pass

```

The `Punto` class that inherits from `ADTPunto` is shown below:
 
```python

from math import sqrt



class Punto(ADTPunto):


    def __init__(self,x,y):


        self.__x = x


        self.__y = y


        super(Punto,self).__init__()





    @property


    def punto(self):


        """el getter de punto, devuelve el punto"""


        return (self.__x,self.__y)





    @punto.setter


    def punto(self,Punto):


        """Asigna nuevo valor al punto"""


        self.__x = Punto.punto[0]


        self.__y = Punto.punto[1]





    @punto.deleter


    def punto(self):


        """Borra los valores del punto"""


        del self.__x


        del self.__y




    @property


    def ValorX(self):


        """Devuelve el valor de x"""


        return self.__x





    @property


    def ValorY(self):


        """Devuelve el valor de y"""


        return self.__y





    def reset(self):


        """Fija el punto en (0,0)"""


        self.__x = 0


        self.__y = 0





    def distanciaOtroPunto(self,oPunto):


        '''devuelve la distancia entre el punto original y un punto dado'''


        return sqrt((self.__x - oPunto.punto[0])**2 + (self.__y - oPunto.punto[1])**2 )





    def mover(self,oPunto):


        """Cambia el punto a un nuevo punto"""


        self.__x = oPunto.punto[0]


        self.__y = oPunto.punto[1]


```




Finally, the instantiation of both classes is shown:


```python


if __name__ == "__main__":


    try:


        prueba = ADTPunto()


    except (TypeError):


        print ("No puede instanciar una clase abstracta")



    punto2d = Punto(3,5)


    print(punto2d.punto)


    print(punto2d.ValorX)


    print(punto2d.ValorY)


    punto2d.mover(Punto(5,5))


    print(punto2d.punto)


    print(punto2d.distanciaOtroPunto(Punto(10,10)))


    punto2d.reset()


    print(punto2d.punto)
```



When the script is run you get the following:
```
python ej12_adt.py 
No puede instanciar una clase abstracta
(3, 5)
3
5
(5, 5)
7.07106781187
(0, 0)
```

As you can see, an attempt was made to instantiate the `ADTPunto` class, which generates a type error.

The complete code of the classes is in [gitlab in the tutorial-poo repo](https://gitlab.com/ecrespo/tutorial-poo/blob/master/ej12_adt.py).


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)




