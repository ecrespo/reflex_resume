Title: Variables and placeholders in Tensorflow  
Date: 2018-02-10 09:00  
Category: Tutorial de Python  
Tags: Python,TensorFlow
lang: en
translation: true  

Continuing with the Tensorflow series, there are the following articles:

1. [Hello world from TensorFlow](/blog/holamundodesdetensorflow)  
2. [Basic math with TensorFlow](/blog/matematicasbasicascontensorflow)
3. [Handling matrices with Tensorflow](/blog/manejodematricescontensorflow) 

The Tensorflow Variable object lets you define a variable (store a state in a Graph object with an initial value), whereas the placeholder object is used to feed external data into a Graph object, but the data to be fed is not supplied when the placeholder is created; for that, the initialization of the variables is used.

Below is the example of using variables and placeholder from `jupyter notebook`:

In [1]:
```python
#Se importa tensofflow
import tensorflow as tf
```
In [2]:
```python
#Se crea una sesión interactiva ( útil cuando se usa jupyter notebook)
sess = tf.InteractiveSession()
```
In [3]:
```python
#Se crea tensor como un número uniforme aleatorio, una matrix de 4x4, de elementos
#de valores entre 0 a 1.
tensor = tf.random_uniform((4,4),0,1)
```
In [4]:
```python
#tensor es un objeto Tensor, de números aleatorios uniformes, de una matrix 4x4 y de typo float32.
tensor
```
Out[4]:
```python
<tf.Tensor 'random_uniform:0' shape=(4, 4) dtype=float32>
```
In [5]:
```python
#se crea variable como un objeto variable que se le pasa como valor inicial el objeto tensor.
variable = tf.Variable(initial_value=tensor)
```
In [6]:
```python
#Se imprime el valor de la variable, 
#esta devuelve tipo Variable, con una matriz 4x4 con elementos de tipo float32
print(variable)

<tf.Variable 'Variable:0' shape=(4, 4) dtype=float32_ref>
```
In [7]:
```python
#Se inicializa las variables con init
init = tf.global_variables_initializer()
```
In [8]:
```python
#Se corre la inicialización
sess.run(init)
```
In [9]:
```python
#Se muestra el valor de la variable corriendo la sesión, se nota los elementos
#entre 0 a 1 y de tipo float32
sess.run(variable)
```
Out[9]:
```python
array([[0.05263364, 0.94140494, 0.4843645 , 0.36463213],
       [0.9149779 , 0.01328921, 0.3837136 , 0.7204586 ],
       [0.5955255 , 0.70812213, 0.19933975, 0.40913558],
       [0.359192  , 0.82358146, 0.1225971 , 0.24963093]], dtype=float32)
```
In [10]:
```python
#Se crea el placeholder, lo cual reserva el espacio, pero no tiene datos como una variable.
ph = tf.placeholder(tf.float32,shape=(None,5))
```
In [11]:
```python
#Se muestra el objeto placeholder, sólo tiene definido el tipo de datos el cual es float32
print(ph)

Tensor("Placeholder:0", shape=(?, 5), dtype=float32)
```
In [ ]:
```
 
```

The next article will explain the use of Graph.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
