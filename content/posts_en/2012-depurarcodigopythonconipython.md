Title: Debugging Python code with ipython.
Date: 2012-12-06 9:00
Category: Tutorial Python
Tags: General,Linux,numpy,python,ipython
lang: en
translation: true

The previous 3 articles explained how to do profiling with 3 tools (timeit, line_profiler and cProfile). Now we will explain how to debug Python code.

In this case we will debug code using `ipython`.
Besides allowing profiling, `ipython` also allows code debugging.

The code below generates an array, then prints the array, the value of one element of that array, and iterates over the array's elements:

```python
#!/usr/bin/env python

# -*- coding: utf-8 -*-

#Se importa numpy como np

import numpy as np

a = np.arange(10)

print a

print a[8]

print a[9]

for i in a:

    print i

print a[10]
```

The result of running the script is the following:

```
ecrespo@jewel:~/proyectos/ernesto-ecrespo.blogspot/debugipython$ python arreglo.py 

[0 1 2 3 4 5 6 7 8 9]

8

9

0

1

2

3

4

5

6

7

8

9

Traceback (most recent call last):

  File "arreglo.py", line 17, in <module>

    print a[10]

IndexError: index out of bounds
```


The error message appears when trying to print the value of element 10 of the array a (which does not exist).

Next, run `ipython` from the Linux console. ipython enters an interactive interpreter, where you run the command `%run script.py`. This starts debug mode with the script passed as the argument:

```python
ecrespo@jewel:~/proyectos/ernesto-ecrespo.blogspot/debugipython$ ipython

Python 2.7.3rc2 (default, Apr 22 2012, 22:35:38) 

Type "copyright", "credits" or "license" for more information.



IPython 0.13.1 -- An enhanced Interactive Python.

?         -> Introduction and overview of IPython's features.

%quickref -> Quick reference.

help      -> Python's own help system.

object?   -> Details about 'object', use 'object??' for extra details.



In [1]: %run arreglo.py

[0 1 2 3 4 5 6 7 8 9]

8

9

0

1

2

3

4

5

6

7

8

9



---------------------------------------------------------------------------


IndexError                                Traceback (most recent call last)


/usr/lib/python2.7/dist-packages/IPython/utils/py3compat.pyc in execfile(fname, *where)


    176             else:


    177                 filename = fname


--> 178             __builtin__.execfile(filename, *where)





/home/ecrespo/proyectos/ernesto-ecrespo.blogspot/debugipython/arreglo.py in <module>()


     15     print i


     16 


---> 17 print a[10]





IndexError: index out of bounds

```

The result is the execution of the script, and it points to the section where the error is.

Now run the `%debug` command:
```python
In [2]: %debug
> /home/ecrespo/proyectos/ernesto-ecrespo.blogspot/debugipython/arreglo.py(17)<module>()
     15     print i
     16 
---> 17 print a[10]
```
It is clear that the error is on line 17 of the script, where it tries to print element 10 of the array, which does not exist.

You can list the code by running the `list` command:
```python
ipdb> list
     12 print a[9]
     13 
     14 for i in a:
     15     print i
     16 
---> 17 print a[10]
```
Evaluating code. You can run a Python statement to evaluate the size of the array.
```python
ipdb> len(a)
10
```
Print the value of a:
```python
ipdb> print a
[0 1 2 3 4 5 6 7 8 9]
```
Viewing the stack calls: it is a stack that holds information about the active functions of a running program. The command to see the stack is bt:

```python
ipdb> bt

  /usr/lib/python2.7/dist-packages/IPython/utils/py3compat.py(178)execfile()


    174             if isinstance(fname, unicode):


    175                 filename = fname.encode(sys.getfilesystemencoding())


    176             else:


    177                 filename = fname


--> 178             __builtin__.execfile(filename, *where)





> /home/ecrespo/proyectos/ernesto-ecrespo.blogspot/debugipython/arreglo.py(17)<module>()


     13 


     14 for i in a:


     15     print i


     16 


---> 17 print a[10]



Moverse hacia arriba en el stack se logra al ejecutar el comando `u`:
```python
ipdb> u
> /usr/lib/python2.7/dist-packages/IPython/utils/py3compat.py(178)execfile()
    176             else:
    177                 filename = fname
--> 178             __builtin__.execfile(filename, *where)

Para moverse hacia abajo en el stack se logra al ejecutar el comando d:
ipdb> d
> /home/ecrespo/proyectos/ernesto-ecrespo.blogspot/debugipython/arreglo.py(17)<module>()
     15     print i
     16 
---> 17 print a[10]
```


To exit debug mode run the command `exit`; to leave the `ipython` command interpreter run `exit` again.

It is clear that the error in the script is on line 17, where it tries to print an element of the array that does not exist.

This is how you can debug Python code with `ipython`. 

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)