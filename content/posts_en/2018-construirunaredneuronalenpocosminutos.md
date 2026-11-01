Title: Build a neural network in a few minutes  
Date: 2018-02-11 12:00  
Category: Tutorial de Python  
Tags: Python, Numpy,Red Neuronal, Inteligencia Artificial
lang: en
translation: true

The previous article showed a neural network that classified some data ([Introduction to the perceptron](/blog/introduccionalperceptronconpython)).

As the video on [how to build a neural network in 4 minutes](http://www.youtube.com/watch?v=h3l4qz76JhQ&t=2s) says, the steps for working with Machine Learning are:

1. Build
2. Train 
3. Test



The video with the explanation of the neural network is below:

[https://youtu.be/h3l4qz76JhQ](https://youtu.be/h3l4qz76JhQ) 

<iframe width="560" height="315" src="https://www.youtube.com/embed/h3l4qz76JhQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>




This article, like the video, is based on an article published on medium called [How to build a simple neural network in 9 lines of Python code (broken link)](http://medium.com/technology-invention-and-more/how-to-build-a-simple-neural-network-in-9-lines-of-python-code-cc8f23647ca1) and on the article [A Neural Network in 11 lines of Python (Part 1)](http://iamtrask.github.io/2015/07/12/basic-python-network/).

The idea is that there is an input of 1s and 0s data and an output that is a 1 or a 0; this data sample will be used to train the neural network, then when the learning finishes and the weights of the neural network are adjusted, a new input data scenario will be passed to it and the network will calculate the output value.

Below is an image of the input data samples, the output that is generated and the new data scenario that will be received.

![](./images/construirunaredneuronalenpocosminutos-1.png) 

The equation to calculate the output of a neuron is:  

![](./images/construirunaredneuronalenpocosminutos-2.png) 

A sigmoid will be used as the activation function of the neural network:

Its equation is:

![](./images/construirunaredneuronalenpocosminutos-3.png) 

And the plot:

![](./images/construirunaredneuronalenpocosminutos-4.png) 

Substituting the summation equation into the sigmoid function gives the output of a neuron:

![](./images/construirunaredneuronalenpocosminutos-5.png) 

Below is the code for building, training and testing the neural network:


In [1]:
```python
# Datos de entrada y de salida

Entradas 	Salida
001 	0
111 	1
101 	1
011 	0
100 	?
```
In [2]:
```python
#Se importan:
# exp: valor e
# array: manejo de arreglos
#random: números aleatorios
#dot: multiplicación de matrices.
from numpy import exp, array, random, dot
```
In [3]:
```python
class RedNeuronal(object):
    def __init__(self,seed=1):
        # Seed el generador de números aleatorios, generará los mismos números
        #cada vez que el programa corra.
        random.seed(seed)

        # se modelará una simple neurona con 3 entradas y una salida.
        
        # se asignan pesos aleatorios a una matrix 3x1 con valores en el rango de -1 a 1
        # y media de cero
        self.pesos_sinaptico = 2 * random.random((3, 1)) - 1

    # La función sigmoid, describe una curva S.
    #Se pasa la suma de los pesos de las entradas a esta función
    # se normaliza entre 0 y 1.
    def __sigmoide(self, x):
        return 1 / (1 + exp(-x))

    # La derivada de la función sigmoid es el gradiente de la curva sigmoide
    def __derivada_sigmoide(self, x):
        return x * (1 - x)
    

    # Se entrena la red neuronal desde un proceso de ensayo y error
    # ajustando los pesos de las sinapcis cada vez
    def entrenar(self, datos_entrenamiento_entrada, datos_entrenamiento_salida, numero_iteraciones):
        for iteracion in range(numero_iteraciones):
            # Se para  los datos de entrenamiento a la red neuronal (una neurona)
            salida = self.pensar(datos_entrenamiento_entrada)

            # calculo del error (la diferencia entre la salida deseada y la que se predice
            error = datos_entrenamiento_salida - salida

            # multiplicar el error por la entrada y de nuevo por el gradiente de la curva sigmoide
            # Esto significa menos presos cercanos son ajustados más
            # esto significa las entradas las cuales son ceros, no causan
            # cambios a los pesos.
            ajuste = dot(datos_entrenamiento_entrada.T, error * self.__derivada_sigmoide(salida))

            # se ajustan los pesos
            self.pesos_sinaptico += ajuste

    # la neurona piensa.se le pasa las entradas.
    def pensar(self, entradas):
        # pasas las entradas a la red neuronal, se devuelve la función de activación(sigmoide)
        #se hace el producto punto de las entradas junto con los pesos.
        return self.__sigmoide(dot(entradas, self.pesos_sinaptico))
```
In [4]:
```python
#Se inicializa una neurona de la red neuronal.
red_neuronal = RedNeuronal()

print ("Pesos iniciales de la sinaptic:\n {}".format(red_neuronal.pesos_sinaptico))

# Conjunto de datos de entradas y salidas para el entrenamiento de la neurona.
#se tienen 4 muestras, cada consiste de 3 valores de entrada y 1 no de salida
datos_entrada = array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
datos_salida = array([[0, 1, 1, 0]]).T

# Se entrena a la red neuronal con el conjunto de datos
#Se entrena unas 10 mil veces y se hace un pequeño ajuste cada vez
red_neuronal.entrenar(datos_entrada, datos_salida, 100000)

print ("Nuevos pesos sinapticos luego del entrenamiento:\n{}".format(red_neuronal.pesos_sinaptico))

# Se prueba la red neuronal con un nuevo escenario de datos
print ("Considere la nueva situación [1, 0, 0] -> ?: {}".format(red_neuronal.pensar(array([1, 0, 0]))))
```
Initial synaptic weights:  
```
 [[-0.16595599]
 [ 0.44064899]
 [-0.99977125]]
```
New synaptic weights after training:  
```
[[12.00870061]
 [-0.2044116 ]
 [-5.8002822 ]]
```
Consider the new situation `[1, 0, 0] -> ?: [0.99999391]`

The result for the case of `[1,0,0]` is `1`.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)