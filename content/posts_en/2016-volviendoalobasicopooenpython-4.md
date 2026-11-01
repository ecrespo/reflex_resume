Title: Back to basics, OOP in Python (part 4)  
Date: 2016-10-31 09:00  
Category: Tutorial Python  
Tags: Python,POO
lang: en
translation: true  

You can review the previous articles on Object-Oriented Programming at this [link](/blog/tags).

This article covers inheritance, encapsulation, the use of getter, setter and deleter, and the use of static methods and classmethod.

The article on [part 3 of OOP](/blog/volviendoalobasicopooenpython-3) explains the use of @property and @method.setter; what remained to be explained is the deleter, which is used to delete attributes of the object.

@staticmethod is used when the self argument is not used in a method.

@classmethod defines a method that receives the class among its arguments (by convention it is named cls).

The Punto2D class will be created with the following attributes and methods:

- The point is defined as (x,y); the Punto2 class has private attributes (these attributes cannot be accessed from the class instance, which is why there are a getter and a setter):
    - self.__x
    - self.__y
- Method __init__ that assigns the initial values to the instance.
- getter, setter and deleter of punto.
- getter, setter and deleter of ValorX and ValorY.
- Method mover: Assigns a new value to the point.
- Method reset: Assigns the value (0,0) to the point. 
- Method distanciaOtroPunto: Calculates the distance to another point.

The code of `ej12.py` is shown below:

```python
#!/usr/bin/env python3

# -*- coding: utf-8 -*-


from math import sqrt


class Punto2D(object):

    """Representacion de un punto en 2 dimensiones"""

    cont_puntos = 1



    def __init__(self,punto=(0,0)):

        '''constructor del punto'''

        self.__x,self.__y = punto

        Punto2D.cont_puntos += 1



    @property

    def ValorX(self):

        '''Devuelve el valor de X'''

        return self.__x



    @ValorX.setter

    def ValorX(self,x):

        '''Se le asigna un valor  a x por medio de setter'''

        self.__x = x



    @property

    def ValorY(self):

        '''Devuelve el valor de y'''

        return self.__y



    @ValorY.setter

    def ValorY(self,y):

        '''Se le asigna un valor a y por medio del setter'''

        self.__y = y



    @property

    def punto(self):

        """el getter de punto, devuelve el punto"""

        return (self.__x,self.__y)



    @punto.setter

    def punto(self,punto):

        ''''el setter de punto'''

        self.__x,self.__y = punto



    @property

    def cantPuntos(self):

        '''Devuelve la cantidad de puntos creados'''

        return Empleado.cont_puntos



    @punto.deleter

    def punto(self):

        '''deleter de punto'''

        del self.__x

        del self.__y

        cont_puntos = 0



    def mover(self,x,y):

        '''mueve el punto a un nuevo punto'''

        self.__x, self.__y = x,y



    def reset(self):

        '''coloca en el origen al punto'''

        self.mover(0,0)



    def distanciaOtroPunto(self,oPunto):

        '''devuelve la distancia entre el punto original y un punto dado'''

        return sqrt((self.__x - oPunto.punto[0])**2 + (self.__y - oPunto.punto[1])**2 )



    @staticmethod

    def autor(autor):

        '''Se define el autor de la clase'''

        return "El autor de esta clase es: {}".format(autor)



    @classmethod

    def cantidadPuntos(cls,cantidad):

        '''Se cambia la cantidad de puntos'''

        cls.cont_puntos = cantidad



if __name__ == "__main__":

    #Se crea cordenada de la clase Punto2D donde se le pasa (4,6)

    cordenada = Punto2D((4,6))

    #Se muestra el valor del punto.

    print(cordenada.punto)

    #Se asigna por setter un nuevo valor

    cordenada.punto = (10,15)

    #Se muestra el nuevo valor de cordenada

    print(cordenada.punto)

    #Se calcula la distancia con respecto a otro punto.

    print(cordenada.distanciaOtroPunto(Punto2D((100,100))))

    #Se fija el punto en un valor (0,0)

    cordenada.reset()

    #Se muestra el nuevo valor de la cordenada.

    print (cordenada.punto)

    #Se muestra un mensaje pasando el autor de la clase.

    print (cordenada.autor("Ernesto"))

    #Muestra la cantidad de puntos que se han creado.

    print ('Cantidad de puntos : {0}'.format(cordenada.cont_puntos ))

    #Se modifica la cantidad de puntos a 1 por medio de setter.

    Punto2D.cantidadPuntos(1)

    #Se vuelve a mostrar la cantida de puntos.

    print ('Cantidad de puntos : {0}'.format(cordenada.cont_puntos ))

    #Se borra la instancia cordenada.

    del(cordenada)

    #Se intenta mostrar el punto pero va a devolver que no se puede

    try:

        print (cordenada.punto)

    except (NameError):

        print ("No existe el objeto cordenada")
``` 

Running `ej12.py` gives the following:
```python
python ej12.py
(4, 6)
(10, 15)
123.794184031
(0, 0)
El autor de esta clase es: Ernesto
Cantidad de puntos : 3
Cantidad de puntos : 1
No existe el objeto cordenada

```

Now `ej12_3d.py` will be created, which will have the Punto3D class that inherits from Punto2D.

The Punto3D class has practically the same methods; the only difference is that it now handles a point with 3 dimensions: it inherits X and Y from the 2-dimensional point and handles Z. 

So the methods of Punto2D are overridden in Punto3D. To access the Punto2D object, super is used. 

Below is the code of `ej12_3d.py`:

```python
#!/usr/bin/env python3


# -*- coding: utf-8 -*-





#Se importa la clase Punto2D de ej12.py


from ej12 import Punto2D


#Se importa raiz cuadrada


from math import sqrt





class Punto3D(Punto2D):


    '''Se define la clase Punto3D'''





    def __init__(self,punto3d):


        '''Método init donde se le asigna x y y a Punto2D por medio de super'''


        super(Punto3D,self).__init__(punto3d[0:-1])


        self.__z = punto3d[-1]





    @property


    def ValorZ(self):


        '''devuelve el valor de z por medio de getter'''


        return self.__z





    @ValorZ.setter


    def ValorZ(self,z):


        '''Se asigna un valor a z por medio de setter'''


        self.__z = z





    @ValorZ.deleter


    def ValorZ(self):


        '''se borra el valor de z por medio de deleter'''


        del (self.__z)





    @property


    def punto(self):


        '''el getter de punto, devuelve el punto'''


        x,y = super(Punto3D,self).punto


        return (x,y,self.ValorZ)





    @punto.setter


    def punto(self,punto3d):


        '''Se le asigna un valor al punto por medio de setter'''


        super(Punto3D,self).mover(punto3d[0],punto3d[1])


        self.__z = punto3d[-1]





    @punto.deleter


    def punto(self):


        '''Se borra el punto por medio de deleter'''


        print ("Punto borrado")


        del Punto2D


        del self.__z





    def mover(self,x,y,z):


        '''Se asigna un nuevo valor al punto''''


        super(Punto3D,self).mover(x,y)


        self.__z = z





    def reset(self):


        '''Se fija el punto como (0,0,0)'''


        super(Punto3D,self).mover(0,0)


        self.__z = 0





    def distanciaOtroPunto(self,oPunto):


        '''devuelve la distancia entre el punto original y un punto dado'''


        x,y = super(Punto3D,self).punto


        z = self.__z


        return sqrt((x - oPunto.punto[0])**2 + (y - oPunto.punto[1])**2 + (z - oPunto.ValorZ) ** 2 )


if __name__ == '__main__':


    #Se crea la instancia Punto3D con el punto.


    punto3d = Punto3D((4,6,4))


    #Se muestra el valor del punto


    print(punto3d.punto)


    #Se asigna un nuevo valor a punto.


    punto3d.punto = (3,3,3)


    #Se muestra dicho valor


    print(punto3d.punto)


    #Se muestra los valores de x,y y z.


    print(punto3d.ValorX)


    print(punto3d.ValorY)


    print(punto3d.ValorZ)


    #Se asigna el valor (0,0,0)


    punto3d.reset()


    #Se muestra su valor.


    print(punto3d.punto)


    #Se calcula la distancia con otro punto.


    print(punto3d.distanciaOtroPunto(Punto3D((15,45,55))))


    #Se borra el punto3d.


    del(punto3d)


    #Se intenta mostrar el valor o devuelve que el objeto no existe.


    try:


        print (punto3d.punto)


    except (NameError):


        print ("No existe el objeto punto3d")

```

Running `ej12_3d.py` gives the following:
```python
python ej12_3d.py
(4, 6, 4)
(3, 3, 3)
3
3
3
(0, 0, 0)
72.6291952317
No existe el objeto punto3d
```


This article shows encapsulation, inheritance and several methods.

You can find the code on gitlab for both [ej12.py](https://gitlab.com/ecrespo/tutorial-poo/blob/master/ej12.py) and [ej12_3d.py](https://gitlab.com/ecrespo/tutorial-poo/blob/master/ej12_3d.py).

##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)



