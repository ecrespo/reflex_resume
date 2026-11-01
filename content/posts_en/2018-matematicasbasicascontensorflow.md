Title: Basic math with TensorFlow   
Date: 2018-02-04 15:00  
Category: Tutorial de Python  
Tags: Numpy,Python, TensorFlow
lang: en  
translation: true  

In the [previous article (broken link)](/blog/holamundodesdetensorflow) I explained the installation and showed a "hello world" from TensorFlow.

This article explains the use of constants and variables, first with a 1-dimensional array of 4 elements, how a numpy array is converted to a TensorFlow object and how to show its elements; then it shows how to handle the equation y = x+1 with x = 9.


Handling a one-dimensional array with tensorflow
In [1]:
```python
#Se importa numpy y tensorflow
import numpy as np
import tensorflow as tf
```
In [2]:
```python
#Se crea un arreglo de una dimensión
tensor_1d = np.array([5.7, 2, 8.0, 25.99])
```
In [3]:
```python
#Se imprime el arreglo
print (tensor_1d)
[  5.7    2.     8.    25.99]
```
In [4]:
```python
#Se imprime el último elemento del arreglo -> 25.99
print (tensor_1d[-1])
25.99
```
In [5]:
```python
#Dimensiones del arreglo -> 1 dimensión
tensor_1d.ndim
```
Out[5]:
```python
1
```
In [6]:
```python
#Cantidad de elementos del arreglo -> 4 elementos
tensor_1d.shape
```
Out[6]:
```python
(4,)
```
In [7]:
```python
#Tipo de los elementos que contiene el arreglo ->float64
tensor_1d.dtype
```
Out[7]:
```python
dtype('float64')
```
In [8]:
```python
#Convierte el arreglo a un objeto tensorflow
tf_tensor=tf.convert_to_tensor(tensor_1d,dtype=tf.float64)
```
In [9]:
```python
# tipo tensor, constante, 4 elementos y de tipo float64
tf_tensor
```
Out[9]:
```python
<tf.Tensor 'Const:0' shape=(4,) dtype=float64>
```
In [10]:
```python
# Se inicia sesión tensorflow y se corre la la impresión de los elementos
with tf.Session() as sess:
    print (sess.run(tf_tensor))
    print (sess.run(tf_tensor[-1]))
[  5.7    2.     8.    25.99]
25.99
```
#### Now an equation will be calculated with some variables:
```
x = 1  
y = x + 9  
print(y)  
import tensorflow as tf  
x = tf.constant(1,name='x')  
y = tf.Variable(x+9,name='y')  
print(y)  
``` 
In [13]:
```python
#Se define el valor de la constante x = 1
x = tf.constant(1,name='x')
```
In [14]:
```python
#Se define el valor de la variable y = x+9
y = tf.Variable(x+9,name='y')
```
In [16]:
```python
#Se imprime el valor de y, que devuelve el tipo de objeto tensor flow, la variable y, no tiene elementos
#y es de tipo int32.
print(y)
<tf.Variable 'y:0' shape=() dtype=int32_ref>
```
#### For it to work you have to create the session and execute run

In [20]:
```python
# Inicializa todas las variables
model = tf.global_variables_initializer()
```
In [22]:
```python
#Se inicia la sesión, se corre model y luego y. El resultado es y -> 10
with tf.Session() as session:
    session.run(model)
    print(session.run(y))
10
```
In [ ]:
```

```
 

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
