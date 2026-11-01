Title: Decision tree made in Python 
Date: 2017-11-19 09:00
Category: Tutorial Python
Tags: General,Debian,Python,Machine Learning,Scikit-Learn,Árbol de decisión
lang: en
translation: true

I had not written for a while (the situation in Venezuela is not easy).

I will gradually pick the blog articles back up; I have some things on Artificial Intelligence (Neural Networks, Fuzzy Logic, machine learning and deep learning) and design patterns with Python.

This article is about a prediction model called a decision tree. According to [wikipedia (es)](https://es.wikipedia.org/wiki/%C3%81rbol_de_decisi%C3%B3n): It is a prediction model used in various fields ranging from artificial intelligence to economics. Given a set of data, diagrams of logical constructions are built, very similar to rule-based prediction systems, which serve to represent and categorize a series of conditions that occur successively, in order to solve a problem.

On youtube there is a channel dedicated to data science, mainly with Python; the youtuber is [Siraj Raval](https://www.youtube.com/channel/UCWN3xxRkmTPmbKwht9FuE5A). In the following video he explains how to make a gender classifier built with a Decision tree; you can watch the video at the following [link](https://www.youtube.com/watch?v=T5pRlIbr6gg).

<iframe width="560" height="315" src="https://www.youtube.com/embed/T5pRlIbr6gg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


The source code of the exercise in the video can be seen on [github](https://github.com/llSourcell/gender_classification_challenge/blob/master/demo.py).

The idea is to have the height, weight and shoe size data and whether the person is a man or a woman; the decision tree is built, the data is passed to it, and from there, when another data point is passed, it produces an output saying whether it is a man or a woman.

Below is the code:

```python


#!/usr/bin/env python

"""

https://www.youtube.com/watch?v=T5pRlIbr6gg

https://github.com/llSourcell/gender_classification_challenge/blob/master/demo.py



"""

#Se importa la librería sklearn el módulo tre

from sklearn import tree



#Se crea la instancia del árbol de decisión.

clf = tree.DecisionTreeClassifier()



#[altura, peso, talla de zapato]

X = [[181, 80, 44], [177, 70, 43], [160, 60, 38], [154, 54, 37], [166, 65, 40],

     [190, 90, 47], [175, 64, 39],

     [177, 70, 40], [159, 55, 37], [171, 75, 42], [181, 85, 43]]



#La salida donde se dice si es hombre o mujer

Y = ['hombre', 'hombre', 'mujer', 'mujer', 'hombre', 'hombre', 'mujer', 'mujer',

     'mujer', 'hombre', 'hombre']



#Se le pasa los datos  X y Y

clf = clf.fit(X, Y)



#Se definen los datos 1 y 2

dato1 = [190, 70, 43]

dato2 = [185, 62, 37]

prediction = clf.predict([dato1])

#Se muestra el resultado de la predicción de dato1

print(prediction)



prediction = clf.predict([dato2])


#Se muestra el resultado de la predicción de dato 2
print(prediction)
```

Running the script gives:
```python
python3 arboldecision.py 
['hombre']
['mujer']
```

It means that, for a height of 1.90 m, a weight of 70 kilograms and a size of 43, the result is that it is a man, and for a height of 1.85 m, a weight of 62 kilograms and a size of 37, the result is that it is a woman.

I recommend watching the whole video to get a better explanation of how the decision tree works. 

##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
