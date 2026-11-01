Title: Replacing loops with map, filter and reduce.
Date:  2020-02-07 15:33
Category: Tutorial de Python
Tags: Python,Maps,Filter,Reduce
lang: en
translation: true
Slug: python-loops-maps-filter-reduce-2020
Authors: Ernesto Crespo
Summary: Using Map, Filter and Reduce


This article is based on the medium article, [How To Replace Your Python For Loops with Map, Filter, and Reduce (broken link)](https://medium.com/better-programming/how-to-replace-your-python-for-loops-with-map-filter-and-reduce-c1b5fa96f43a). 


The article has 3 phases: the first shows the logic of the examples using loops, then list comprehension is used, and finally map, filter and reduce. 


## Loops 

In this first part a list with 100 numbers is generated (I know a loop is not needed to generate this first list), then the even numbers are computed from that list, then a list with the squares of the numbers generated at the start is built, and finally the total sum of the numbers in the last list is calculated.

### Generating numbers in a list

In [1]:
```python
numeros = [] 
for i in range(0,100): 
    numeros.append(i)
print(numeros)
```

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]

Another way to do it: 
In [2]:
```python
numeros = list(range(100))
print(numeros)
```

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]


### Filtering even numbers from the list


In[3]: 
```python 
numeros_pares = [] 
for numero in numeros:
    if numero % 2 == 0: 
        numeros_pares.append(numero) 
print(numeros_pares)
```

[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98]


### Calculating the square of the even numbers

In[4]:
```python
numeros_pares_cuadrados = []
for numero in numeros_pares:
    numeros_pares_cuadrados.append(numero ** 2)
print(numeros_pares_cuadrados)
```

[0, 4, 16, 36, 64, 100, 144, 196, 256, 324, 400, 484, 576, 676, 784, 900, 1024, 1156, 1296, 1444, 1600, 1764, 1936, 2116, 2304, 2500, 2704, 2916, 3136, 3364, 3600, 3844, 4096, 4356, 4624, 4900, 5184, 5476, 5776, 6084, 6400, 6724, 7056, 7396, 7744, 8100, 8464, 8836, 9216, 9604]

### Calculating the total sum of the even numbers

In[5]:
```python 
# calculate total
total = 0
for numero in numeros_pares_cuadrados:
   total += numero
print(total)
```
161700


## Using list comprehension

Now the calculations are repeated using list comprehension instead of loops. 

### Filtering even numbers from the list


In[6]: 
```python 
numeros_pares = [numero for numero in numeros if numero % 2 == 0] 
print(numeros_pares)
```

[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98]


### Calculating the square of the even numbers

In[7]:
```python
numeros_pares_cuadrados = [numero ** 2 for numero in numeros_pares]
print(numeros_pares_cuadrados)
```

[0, 4, 16, 36, 64, 100, 144, 196, 256, 324, 400, 484, 576, 676, 784, 900, 1024, 1156, 1296, 1444, 1600, 1764, 1936, 2116, 2304, 2500, 2704, 2916, 3136, 3364, 3600, 3844, 4096, 4356, 4624, 4900, 5184, 5476, 5776, 6084, 6400, 6724, 7056, 7396, 7744, 8100, 8464, 8836, 9216, 9604]


### Calculating the total sum of the even numbers

In[8]:
```python 
# calculate total
total = sum([numero for numero in numeros_pares_cuadrados])
print(total)
```
161700

## Using map, filter and reduce 

### Definitions

* map: Apply the same set of steps to each element, storing the result.
map(function,list)
* filter: apply a validation criterion and keep the elements that evaluate that criterion as True.
filter(function,list)
* reduce: returns a value that is passed from one element to the next.
reduce(function,list)

It is worth mentioning that the function passed in will be a lambda.

Here is a simple lambda example that calculates the sum of two numbers:
In[9]: 
```python 
suma = lambda x,y: x+y 
print(suma(1,2))
```
3

### Filtering even numbers from the list

There is a lambda that takes x as its argument and evaluates whether it is an even number; filter is given the lambda and the list of numbers to filter. 

In[10]: 
```python 
numeros_pares = list(filter(lambda x: (x % 2 == 0), numeros))
print(numeros_pares)
```

[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98]

### Calculating the square of the even numbers

Here map is used, with a lambda that takes x as its argument and calculates the square of x; map is given the list of even numbers.

In[11]:
```python
numeros_pares_cuadrados = list(map(lambda x: (x ** 2), numeros_pares))
print(numeros_pares_cuadrados)
```

[0, 4, 16, 36, 64, 100, 144, 196, 256, 324, 400, 484, 576, 676, 784, 900, 1024, 1156, 1296, 1444, 1600, 1764, 1936, 2116, 2304, 2500, 2704, 2916, 3136, 3364, 3600, 3844, 4096, 4356, 4624, 4900, 5184, 5476, 5776, 6084, 6400, 6724, 7056, 7396, 7744, 8100, 8464, 8836, 9216, 9604]

### Calculating the total sum of the even numbers

For this case you have to import reduce from the functools library. 

The lambda requires an accumulator and a value n, which are added together. reduce is given the lambda and the list of squared even numbers.

In[12]:
```python 
from functools import reduce

total = reduce(lambda acc, n: acc + n, numeros_pares_cuadrados)
print(total)
```

161700

As the series of examples shows, depending on the case, using for or while to create a list or to get a result from a list may be unnecessary; list comprehension or filter, map and reduce can be used instead. This can make the code you are developing faster.


####
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
