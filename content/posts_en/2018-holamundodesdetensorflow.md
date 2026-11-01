Title: Hello World from TensorFlow  
Date: 2018-02-04 08:00  
Category: Tutorial Python  
Tags: Python, TensorFlow
lang: en
translation: true  


[TensorFlow](https://www.tensorflow.org/) is an open source library for machine learning (Machine Learning) across a range of tasks, developed by Google to meet its needs for systems capable of building and training neural networks to detect and decipher patterns and correlations, analogous to the learning and reasoning used by humans (more information on [wikipedia](https://es.wikipedia.org/wiki/TensorFlow)).

To install on Linux use pip:
```
pip3 install TensorFlow
```

The first exercise will be to write a Hello world from TensorFlow (using jupyter notebook).

In [1]:
```python
#Se importa tensorflow
import tensorflow as tf
```
In [2]:
```python
#Se crea una constante en la variable hola, donde se le pasa un string
hola = tf.constant("Hola mundo desde TensorFlow!")
```
In [3]:
```python
#Veamos que devuelve la variable hola
print(hola)
Tensor("Const:0", shape=(), dtype=string)
```
#### It returns a tensor object, with a constant of type string

In [4]:
```python
hola
```
Out[4]:
```python
<tf.Tensor 'Const:0' shape=() dtype=string>
```
In [5]:
```python
#Se crea la sesión de tensorflow
sess=tf.Session()
```
In [6]:
```python
#Se corre la sesión pasandole la variable hola
print(sess.run(hola))
b'Hola mundo desde TensorFlow!'
```
In [ ]:
```

```
 
As you can see, to be able to view the value of a TensorFlow constant you 
have to create the session and run the constant in the session.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)