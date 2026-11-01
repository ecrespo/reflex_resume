Title: Data structures in Python (Graphs)
Date: 2017-03-12 09:00
Category: Tutorial Python
Tags: Python,Estructura de datos
lang: en
translation: true

Continuing with the series of articles about data structures in python. In this case the topic is graphs, with two examples, one using lists and another using matrices.

The previous articles are:

- [Nodes](/blog/estructuradedatosenpythonnodo)
- [Linked lists](/blog/estructuradedatosenpythonlistaenlazada)

This article is based on the code on github [Graphs with adjacency lists](http://github.com/joeyajames/Python/blob/master/graph_adjacency-list.py) and [Graphs with an adjacency matrix](ttps://github.com/joeyajames/Python/blob/master/graph_adjacency-matrix.py) and on the youtube video [Graphs in Python](http://www.youtube.com/watch?v=HDUzBEG1GlA).

<iframe width="560" height="315" src="https://www.youtube.com/embed/HDUzBEG1GlA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

As an example graph, a queue process model will be used; the image is below:

![](./images/estructuradedatosenpythongrafos-1.png)

Here is the code handling the graph as a list:

```python
#!/usr/bin/env python

class Vertice(object):

 def __init__(self, n):

  #Se define el nombre del vertice y la lista de vecinos

  self.nombre = n

  self.vecinos = list()

 

 def agregarVecino(self, v):

  if v not in self.vecinos:

   self.vecinos.append(v)

   self.vecinos.sort()


class Grafo(object):

 #Se crea un diccionario de vertices.

 vertices = {}

 

 def agregarVertice(self, vertice):

  #Se pregunta si vertice es una instancia de Vertice y si el nombre no esta en la lista de vertices.

  #Si se cumple se agrega el vertice al diccionario de vertices.

  if isinstance(vertice, Vertice) and vertice.nombre not in self.vertices:

   self.vertices[vertice.nombre] = vertice

   return True

  else:

   return False

 

 def agregarBorde(self, u, v):

  #Si u y v estan en vertices. se agregan como vecinos.

  if u in self.vertices and v in self.vertices:

   self.vertices[u].agregarVecino(v)

   self.vertices[v].agregarVecino(u)

   return True

  else:

   return False

   

 def printGrafo(self):

  #Se muestra el grafo.

  for key in sorted(list(self.vertices.keys())):

   print(key + str(self.vertices[key].vecinos))



if __name__ == '__main__':

 g = Grafo()

 cinco = Vertice('5')

 tres = Vertice('3')

 cuatro = Vertice('4')

 uno = Vertice('1')

 dos = Vertice('2')

 for i in range(ord('1'), ord('6')):

  g.agregarVertice(Vertice(chr(i)))



 bordes = ['53','54','31','35','41','42','45','12','13','14','21','24']

 for borde in bordes:

  g.agregarBorde(borde[:1],borde[1:])



 g.printGrafo()

```

Running the script gives:
```python
python grafo-listas.py
1['2', '3', '4']
2['1', '4']
3['1', '5']
4['1', '2', '5']
5['3', '4']
```

As you can see, the related vertices are: 1 connects with 2, 3 and 4, 2 with 1 and 4, 3 with 1 and 5, 4 with 1, 2 and 5; and 5 with 3 and 4.

The following code shows another way to create the graph; in this case the weight of the edges can be handled (although it is not used in the example).  Here is the code:

```python
#!/usr/bin/env python3



#Se importa nuevas caracteristicas de print

from __future__ import print_function





#Se crea la clace vertice que solo tiene como argumento su nombre.

class Vertice(object):

 def __init__(self, n):

  self.nombre = n





#Se crea la clase grafo con vertices e indices de bordes como diccionarios

#y bordes como una lista.

class Grafo(object):

 vertices = {}

 bordes = []

 indices_bordes = {}





 def agregarVertice(self,vertice):

  #Si vertice es una instancia de su clase y su nombre no esta en el 

  #diccionario de vertices se agrega.

  if isinstance(vertice, Vertice) and vertice.nombre not in self.vertices:

   self.vertices[vertice.nombre] = vertice

   #Se recorre los bordes y se agregan.

   for fila in self.bordes:

    fila.append(0)

   self.bordes.append([0] * (len(self.bordes)+1))

   self.indices_bordes[vertice.nombre] = len(self.indices_bordes)

   return True

  else:

   return False



 def agregarBorde(self,u,v, peso=1):

  #Se agrega el borde.

  if u in self.vertices and v in self.vertices:

   self.bordes[self.indices_bordes[u]][self.indices_bordes[v]] = peso

   self.bordes[self.indices_bordes[v]][self.indices_bordes[u]] = peso

   return True

  else:

   return False





 def printGrafo(self):

  #Se muestra el grafo

  for v, i in sorted(self.indices_bordes.items()):

   print(v + ' ', end='')

   for j in range(len(self.bordes)):

    print(self.bordes[i][j], end='')

   print(' ')    





if __name__ == '__main__':

 g = Grafo()

 cinco = Vertice('5')

 tres = Vertice('3')

 cuatro = Vertice('4')

 uno = Vertice('1')

 dos = Vertice('2')

 for i in range(ord('1'), ord('6')):

  g.agregarVertice(Vertice(chr(i)))



 bordes = ['53','54','31','35','41','42','45','12','13','14','21','24']

 for borde in bordes:

  g.agregarBorde(borde[:1],borde[1:])



 g.printGrafo()

```

Running the script gives the following:
```python
python grafo-matrix-adyacente.py 
1 01110 
2 10010 
3 10001 
4 11001 
5 00110 
```
As in the previous case, vertex 1 connects with 2, 3 and 4, vertex 2 connects with 1 and 4, vertex 3 connects with 1 and 5, vertex 4 connects with 1, 2 and 5; and vertex 5 connects with 3 and 4.


There are two ways to represent a graph; you can use whichever you prefer, depending on the complexity; if you need to handle weights, the matrix is the option.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
