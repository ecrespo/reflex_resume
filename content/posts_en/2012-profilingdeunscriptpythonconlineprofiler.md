Title: Profiling a python script with line_profiler
Date: 2012-12-04 9:00 
Category: Tutorial Python
Tags: General,Linux,numpy,Python,Profiling, line_profiler
lang: en
translation: true

Now we will see how to use the `line_profiler` tool to profile Python programs.

The first thing to do is install `line_profiler` with the `easy_install` or `pip` command:
```
easy_install line_profiler
```
```
pip install line_profiler
```

The code to be reviewed is the same as in the previous article (inverse matrix). The difference is that the profile decorator is used on the function that generates the inverse matrix.

The code is the following:
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



#Se define una lista de  tamaños de la matriz

tamagno = 2 ** np.arange(0, 12)

#Se recorre la lista de tamaños y se invierte cada matriz con la

#funcion.

for n in tamagno:

    Inversa(n)
```
To do the profiling, run the following command:

```python
ecrespo@jewel:~/proyectos/ernesto-ecrespo.blogspot/line_profiler$ kernprof.py -l -v  matrizinversa.py 

Wrote profile results to matrizinversa.py.lprof

Timer unit: 1e-06 s



File: matrizinversa.py

Function: Inversa at line 10

Total time: 6.05993 s



Line #      Hits         Time  Per Hit   % Time  Line Contents

==============================================================

    10                                           @profile

    11                                           def Inversa(n):

    12        12       260506  21708.8      4.3      a = np.matrix(np.random.rand(n, n))

    13        12      5799424 483285.3     95.7      return a.I
```

The result shows the total execution time, then each executed line and the percentage of time spent on it. Note that generating the matrix does not take long, but inverting it takes 95.7% of the execution time.
The meaning of each parameter is:  

- `Line`: The line number in the file.
- `Hits`: The number of times the line is executed.
- `Time`: Time spent executing each line.
- `Per Hit`: Average time spent executing each line.
- `% Time`: Percentage of time spent executing the line relative to the time spent executing all the lines.

The script's code is on [bitbucket (broken link)](https://bitbucket.org/ecrespo/ernesto-ecrespo.blogspot/src/dbfc744caa2138355d0be1811a1edbde5379f189/line_profiler/matrizinversa.py?at=default).

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV
  
Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)