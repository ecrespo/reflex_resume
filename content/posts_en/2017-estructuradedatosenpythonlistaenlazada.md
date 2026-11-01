Title: Data structures in Python (Linked List)
Date: 2017-03-11 09:00
Category: Tutorial Python
Tags: General,Python
lang: en
translation: true

Continuing with the series on data structures, the previous article dealt with the [Node data structure](/blog/estructuradedatosenpythonnodo); this article will use the Node by composition in the linked list.

This article is based on the youtube tutorial called [Python:Linked Lists](http://www.youtube.com/watch?v=Ast5sKQXxEU), which links to the [code on github (broken link)](http://github.com/joeyajames/Python/blob/master/LinkedLists.py).

<iframe width="560" height="315" src="https://www.youtube.com/embed/Ast5sKQXxEU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

The linked list is based on the `Nodo`; as you will remember, the Node holds the data and a pointer to the next node.  In the case of the linked list it will contain the following:

- Arguments:
    - Nodo: When the linked list is created, a Node with no data that points to None is created.
     - primero: private variable that points to the first node.
     -  ultimo: private variable that points to the last node.
     -  tamagno: private variable that keeps track of the number of nodes the list holds.
- Methods:
    - obtenerTamagno: Returns the size of the list.
    - add: Adds a node to the linked list.
    - remove: Removes a node from the linked list.
    - find: Looks for a value in the list, returns the value or False.



The code of the linked list is shown below:

```python
#!/usr/bin/env python3

#Se importa Nodo de nodos.

from nodos import Nodo


class ListaEnlazada(object):

    def __init__(self,primero = Nodo(None,None)):

        """Se asigna como Nodo inicial a primero y ultimo por que apuntan al mismo nodo

        y se define el tamagno de la lista en cero"""

        self.__primero = primero 

        self.__ultimo = self.__primero

        self.__tamagno = 0





    def obtenerTamagno(self):

        """Devuelve el tamagno de la lista"""

        return self.__tamagno



    def add(self,d):

        """Agrega un nodo a la lista enlazada"""

        #Se crea una instancia de nodo donde se le pasa el dato d y se coloca

        #como proximo nodo el primer nodo.

        nodoNuevo = Nodo(d,self.__primero)

        #El primer nodo apunta al nodo nuevo y se incrementa el tamagno.

        self.__primero = nodoNuevo

        self.__tamagno += 1





    def remove(self,d):

        """Se elimina el nodo que tenga el dato d"""

        #Al nodo actual se le asigna el primer nodo

        nodoActual = self.__primero

        #Y al nodo anterior se le asigna None.

        nodoAnterior = None



        #Mientras exista el nodo actual-

        while nodoActual:

            #Si el dato de nodo actual es igual al dato que se esta buscando.

            if nodoActual.dato == d:

                #Si existe nodo anterior

                if nodoAnterior:

                    #Se asigna  al apuntador proximo del nodo anterior el proximo de nodo actual

                    nodoAnterior.proximo = nodoActual.proximo

                else: 

                    #A primero se le asigna el apuntador al proximo nodo del nodo actual

                    self.__primero = nodoActual.proximo

                #En cualquiera de los dos casos se decrementa el tamagno de la lista.

                self.__tamagno -= 1

                #Devuelve True por que se elimino.

                return True

            else:

                #Se asigna al nodo anterior el nodo actual

                nodoAnterior = nodoActual

                #Se asigna al nodo actual, el nodo proximo del nodo actual

                nodoActual = nodoActual.proximo





    def find(self,d):

        """Se busca d en la lista enlazada, si existe devuelve d, si no devuelve None"""

        #a nodo actual se le asigna el primer nodo.

        nodoActual = self.__primero

        #Mientras exista el nodo actual.

        while nodoActual:

            #Si el dato de nodo actual es igual a d, devuelve d

            if nodoActual.dato == d:

                return d

            else:

                #Si no, el nodo actual apunta al proximo nodo.

                nodoActual = nodoActual.proximo

        #Si no se encuentra devuelve None.

        return None 







if __name__ == '__main__':

    miLista = ListaEnlazada()

    miLista.add(1)

    miLista.add(8)

    miLista.add(12)

    print("size: {0}".format(miLista.obtenerTamagno()))

    print (miLista.find(8))

    miLista.remove(8)

    print("size: {0}".format(miLista.obtenerTamagno()))

    print(miLista.remove(12))

    print("size:{0} ".format(miLista.obtenerTamagno()))

    print(miLista.find(5))

```

When the script is run, you get the following:
```
python listas.py 
size: 3
8
size: 2
True
size: 1
None
```

As you can see, 3 elements are added to the list, then the size of the list is shown, each element of the list is removed in turn while the `tamagno` of the list is shown as elements are removed, and finally the value 5 is searched for in the list, which returns `None`. 



##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
