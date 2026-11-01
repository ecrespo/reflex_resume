Title:  Introduction to Pandas  
Date: 2018-01-07 16:00  
Category: Tutorial Python  
Tags: Ciencia de Datos,Python,Pandas,Data Science
lang: en
translation: true

Pandas is a python library for analyzing data; it supports multiple data inputs.

The article is based on an English-language article [Building a neural network with python (broken link)](http://www.springboard.com/blog/beginners-guide-neural-network-in-python-scikit-learn-0-18/), and on a [pandas tutorial (broken link)](http://www.tutorialspoint.com/python_pandas/).

This tutorial will use a dataset in csv format about wines ([chemical analysis to determine the origin of wines](http://archive.ics.uci.edu/ml/datasets/Wine)).

Below, the way to handle the data from the file [wine_data.csv](http://github.com/ecrespo/codigo_blog/blob/master/pandas/wine_data.csv) is described step by step.

You can download the file [Pandas.py](http://github.com/ecrespo/codigo_blog/blob/master/pandas/Pandas.py) and [Pandas.ipynb](http://github.com/ecrespo/codigo_blog/blob/master/pandas/Pandas.ipynb) from github.

Import `Pandas` as `pd`:
```python
>>> import pandas as pd
```
Extract the data from the csv file and define the column names:
```python
>>> wine = pd.read_csv('wine_data.csv', names = ["Cultivator", "Alchol", "Malic_Acid", "Ash", "Alcalinity_of_Ash", "Magnesium", "Total_phenols", "Falvanoids", "Nonflavanoid_phenols", "Proanthocyanins", "Color_intensity", "Hue", "OD280", "Proline"])
```
Show the first rows of data:
```python
>>> wine.head()
```
![](./images/introduccionapandas-1.png) 

Show the dimensions of the table:
```
>>> wine.shape
(178, 14)
```
There are 178 rows and 14 columns.

Show the first 2 rows of the table:
```python
wine.loc[[0,1]]
```
![](./images/introduccionapandas-2.png) 

Show the first two rows and the `Cultivator` and `Alchol` columns
```python
>>> wine.loc[[0,1]][["Cultivator","Alchol"]]
```
![](./images/introduccionapandas-3.png) 

This introduction is necessary since future articles will work a lot with the `pandas` library.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
