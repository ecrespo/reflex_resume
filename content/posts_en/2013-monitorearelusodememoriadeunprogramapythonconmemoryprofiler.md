Title: Monitoring the memory usage of a Python program with memory_profiler
Date: 2013-02-02 10:00
Category: 
Tags: Canaima,Debian,General,Linux,Python,Ubuntu
lang: en
translation: true

`Memory_profiler` is a Python module developed to monitor the memory consumption of a Python program, line by line for each instruction of the program.

To install the module, use `easy_install` or `pip`:
```
easy_install -U memory_profiler
```
```
pip install -U memory_profiler
```
Here is the code from the article about profiling published [earlier](/blog/profilingdeunscriptpythoncontimeit):
```python
#!/usr/bin/env python

# -*- coding: utf-8 -*-

#Se importa numpy como np
import numpy as np

#Se define el uso del decorador profile. En la funcion que genera matrices inversas.
@profile
def Inversa(n):
    a = np.matrix(np.random.rand(n, n))
    return a.I

if __name__ == '__main__':
    #Se define una lista de  tamaños de la matriz
    tamagno = 2 ** np.arange(0, 12)
    #Se recorre la lista  y se invierte cada matriz con la
    #funcion Inversa
    for n in tamagno:
        Inversa(n)
```
To start the monitoring, run the following command:
```python
python -m memory_profiler matrizinversa.py
```

The result is shown below:
```python
Filename: matrizinversa.py

Line #    Mem usage    Increment   Line Contents
================================================
     8                             @profile
     9     11.89 MB      0.00 MB   def Inversa(n):
    10     11.91 MB      0.02 MB       a = np.matrix(np.random.rand(n, n))
    11     12.10 MB      0.19 MB       return a.I

Filename: matrizinversa.py
Line #    Mem usage    Increment   Line Contents
================================================
     8                             @profile
     9     12.11 MB      0.00 MB   def Inversa(n):
    10     12.11 MB      0.00 MB       a = np.matrix(np.random.rand(n, n))
    11     12.16 MB      0.05 MB       return a.I

Filename: matrizinversa.py
Line #    Mem usage    Increment   Line Contents
================================================
     8                             @profile
     9     12.16 MB      0.00 MB   def Inversa(n):
    10     12.16 MB      0.00 MB       a = np.matrix(np.random.rand(n, n))
    11     12.16 MB      0.00 MB       return a.I

Filename: matrizinversa.py
Line #    Mem usage    Increment   Line Contents
================================================
     8                             @profile
     9     12.16 MB      0.00 MB   def Inversa(n):
    10     12.16 MB      0.00 MB       a = np.matrix(np.random.rand(n, n))
    11     12.16 MB      0.00 MB       return a.I

Filename: matrizinversa.py
Line #    Mem usage    Increment   Line Contents
================================================
     8                             @profile
     9     12.16 MB      0.00 MB   def Inversa(n):
    10     12.16 MB      0.00 MB       a = np.matrix(np.random.rand(n, n))
    11     12.16 MB      0.00 MB       return a.I

Filename: matrizinversa.py
Line #    Mem usage    Increment   Line Contents
================================================
     8                             @profile
     9     12.16 MB      0.00 MB   def Inversa(n):
    10     12.16 MB      0.00 MB       a = np.matrix(np.random.rand(n, n))
    11     12.17 MB      0.00 MB       return a.I

Filename: matrizinversa.py
Line #    Mem usage    Increment   Line Contents
================================================
     8                             @profile
     9     12.17 MB      0.00 MB   def Inversa(n):
    10     12.22 MB      0.05 MB       a = np.matrix(np.random.rand(n, n))
    11     12.35 MB      0.13 MB       return a.I

Filename: matrizinversa.py
Line #    Mem usage    Increment   Line Contents
================================================
     8                             @profile
     9     12.35 MB      0.00 MB   def Inversa(n):
    10     12.45 MB      0.09 MB       a = np.matrix(np.random.rand(n, n))
    11     12.95 MB      0.50 MB       return a.I

Filename: matrizinversa.py
Line #    Mem usage    Increment   Line Contents
================================================
     8                             @profile
     9     12.45 MB      0.00 MB   def Inversa(n):
    10     12.95 MB      0.50 MB       a = np.matrix(np.random.rand(n, n))
    11     13.54 MB      0.59 MB       return a.I

Filename: matrizinversa.py
Line #    Mem usage    Increment   Line Contents
================================================
     8                             @profile
     9     12.53 MB      0.00 MB   def Inversa(n):
    10     14.54 MB      2.00 MB       a = np.matrix(np.random.rand(n, n))
    11     16.79 MB      2.26 MB       return a.I

Filename: matrizinversa.py
Line #    Mem usage    Increment   Line Contents
================================================
     8                             @profile
     9     12.79 MB      0.00 MB   def Inversa(n):
    10     20.79 MB      8.00 MB       a = np.matrix(np.random.rand(n, n))
    11     28.88 MB      8.09 MB       return a.I

Filename: matrizinversa.py
Line #    Mem usage    Increment   Line Contents
================================================
     8                             @profile
     9     12.87 MB      0.00 MB   def Inversa(n):
    10     44.87 MB     32.00 MB       a = np.matrix(np.random.rand(n, n))
    11     77.38 MB     32.50 MB       return a.I
```

The execution cycles of the inverse matrix generation in the file `matrizinversa.py` are shown. The columns represent the line of the program being executed, the amount of memory used, the memory increment and the code being executed.

##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)