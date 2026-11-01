Title: Visualizing Graph objects with Tensorboard  
Date: 2018-02-12 12:00  
Category: Tutorial Python  
Tags: Python,TensorFlow,Inteligencia Aritifical, DeepLearning,MachineLearning
lang: en  
translation: true  

Continuing with the articles about TensorFlow, in this case I will show how the Graph object is visualized with TensorBoard.

You can check the articles of the TensorFlow series below:

1. [Hello world from Tensorflow](/blog/holamundodesdetensorflow)  
2. [Basic math with Tensorflow](/blog/matematicasbasicascontensorflow)  
3. [Handling matrices with Tensorflow](/blog/manejodematricescontensorflow)  
4. [Variables and placeholders in Tensorflow](/blog/variablesyplaceholdersentensorflow)  
5. [Tensorflow Graph object](/blog/objetographdetensorflow)  

This article is based on the English tutorial [Visualization (broken link)](http://learningtensorflow.com/Visualisation/) and the documentation on the [TensorFlow](http://www.tensorflow.org/programmers_guide/graph_viz). 

There will be two ways of doing the same exercise: the first one simply identifies the operations in the Graph Object (addition, multiplication and division), then the session log is saved and visualized. 

In the next exercise the same operations will be done, but now the Graph Objects are identified with scopes, which will allow a better visualization of those objects and their operations. 

Here is the first exercise:

In [1]:
```python
#Se importa Tensorflow
import tensorflow as tf
```
In [2]:
```python
#Se suma 1+2
a = tf.add(1, 2,name="Suma_estos_numeros")
```
In [3]:
```python
#Se multiplica el valor de la suma anterior por 3
b = tf.multiply(a, 3)
```
In [4]:
```python
#se suma 4+5
c = tf.add(4, 5,name="Suma_estos")
```
In [5]:
```python
#Se multiplica el resultado de la suma anterior por 6
d = tf.multiply(c, 6,name="Multiplica_estos_numeros")
```
In [6]:
```python
#Se multiplica 4*5
e = tf.multiply(4, 5,name="B_suma")
```
In [7]:
```python
#Se divide el resultado de la suma de 4+5 entre 6
f = tf.div(c, 6,name="B_mul")
```
In [8]:
```python
#Se suma la multiplicación de a*3 más la multiplicación de c*6
g = tf.add(b, d)
```
In [9]:
```python
#Se multiplica el resultado de la suma de b+d con el resultado de la división de c/6
h = tf.multiply(g, f)
```
In [10]:
```python
#Se crea la sesión y se corre el resultado del objeto h y se salva en el directorio output.
with tf.Session() as sess:
    writer = tf.summary.FileWriter("output", sess.graph)
    print(sess.run(h))
    writer.close()
```
63

In [ ]:
```

```
 
Now tensorboard will be run, passing it the output directory where the session log with its operations was saved.
```python
tensorboard --logdir=./output/
```
The command will start a web session of the tensorboard application, as the following figure shows:

![](./images/visualizaciondeobjetosgraphcontensorboard-1.png) 

Opening the browser at localhost:6006 shows what the following figure displays:

![](./images/visualizaciondeobjetosgraphcontensorboard-2.png) 


There you can see the operations performed in the session and in the Graph object.

But the Graph objects and the operations can be grouped to make it easier to visualize the Objects and their operations.

Here is the rewrite of the same exercise:

In [1]:
```python
import tensorflow as tf
```
In [2]:
```python
#Se define el nombre del objeto graph y los scopes A,B y C.
with tf.name_scope("GrupoOperacion"):
    with tf.name_scope("Scope_A"):
        a = tf.add(1, 2, name="Suma_estos_numeros")
        b = tf.multiply(a, 3)
    with tf.name_scope("Scope_B"):
        c = tf.add(4, 5, name="Y_estos")
        d = tf.multiply(c, 6, name="Multiplica_estos_numeros")

with tf.name_scope("Scope_C"):
    e = tf.multiply(4, 5, name="B_suma")
    f = tf.div(c, 6, name="B_mult")
g = tf.add(b, d)
h = tf.multiply(g, f)
```
In [3]:
```python
#Se crea la sesión y se corre el resultado del objeto h
with tf.Session() as sess:
    writer = tf.summary.FileWriter("output2", sess.graph)
    print(sess.run(h))
    writer.close()
```
63

Tensorboard is run again, but in this case opening the `output2` directory:
```python
tensorboard --logdir=./output2/
```
The following image shows the different Graphs and each operation each one handles. 

![](./images/visualizaciondeobjetosgraphcontensorboard-3.png) 

This gives a better visualization of each Graph Object and its operations.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
