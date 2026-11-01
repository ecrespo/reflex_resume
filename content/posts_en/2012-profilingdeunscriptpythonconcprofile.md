Title: Profiling a python script with cProfile
Date: 2012-12-05 9:00
Category: Tutorial Python
Tags:General,Linux,numpy,python,cProfile,Profiling
lang: en
translation: true

Continuing with the articles about profiling, another tool for profiling is called `cProfile`, a C extension introduced in Python 2.5. It is used for deterministic profiling (time is measured precisely rather than sampled).

The example I will develop is the same one as the inverse matrix generation; the difference is that the definition of the matrix's n value and its generation will be in a function called main. This function will then be called from `cProfile`.

Here is the code:
```python
#!/usr/bin/env python

# -*- coding: utf-8 -*-



#Se importa numpy como np

import numpy as np

import cProfile

import sys

#funcion que genera matrices inversas.

def Inversa(n):

    a = np.matrix(np.random.rand(n, n))

    return a.I

 

def main():
    

    #Se define una lista de  tamaños de la matriz

    tamagno = 2**np.arange(0,12)

    #Se recorre la lista de tamaños y se invierte cada matriz con la

    #funcion.

    for n in tamagno:

        Inversa(n)



#Se ejecuta la función main desde la llamada run de cProfile.    

cProfile.run('main()')
```

When you run the script, the result is the profiling of the inverse matrix generation:

```
ecrespo@jewel:~/proyectos/ernesto-ecrespo.blogspot/cprofile$ python matrizinversa.py 

         809 function calls in 5.764 seconds



   Ordered by: standard name



   ncalls  tottime  percall  cumtime  percall filename:lineno(function)

        1    0.000    0.000    5.764    5.764 <string>:1(<module>)

       24    0.000    0.000    0.058    0.002 defmatrix.py:233(__new__)

       36    0.000    0.000    0.000    0.000 defmatrix.py:279(__array_finalize__)

       12    0.000    0.000    0.000    0.000 defmatrix.py:55(asmatrix)

       12    0.015    0.001    5.467    0.456 defmatrix.py:808(getI)

        1    0.000    0.000    0.000    0.000 dual.py:12(<module>)

       12    0.000    0.000    0.000    0.000 linalg.py:127(_to_native_byte_order)

       12    0.000    0.000    0.257    0.021 linalg.py:139(_fastCopyAndTranspose)

       12    0.000    0.000    0.000    0.000 linalg.py:151(_assertRank2)

       12    0.000    0.000    0.000    0.000 linalg.py:157(_assertSquareness)

       12    0.000    0.000    5.396    0.450 linalg.py:244(solve)

       12    0.020    0.002    5.452    0.454 linalg.py:404(inv)

       36    0.000    0.000    0.000    0.000 linalg.py:66(_makearray)

       36    0.000    0.000    0.000    0.000 linalg.py:71(isComplexType)

       24    0.000    0.000    0.000    0.000 linalg.py:84(_realType)

       12    0.000    0.000    0.000    0.000 linalg.py:99(_commonType)

       12    0.007    0.001    5.751    0.479 matrizinversa.py:12(Inversa)

        1    0.013    0.013    5.764    5.764 matrizinversa.py:17(main)

       36    0.000    0.000    0.000    0.000 numeric.py:167(asarray)

       12    0.000    0.000    0.035    0.003 numeric.py:1830(identity)

       36    0.000    0.000    0.000    0.000 {getattr}

       72    0.000    0.000    0.000    0.000 {isinstance}

       60    0.000    0.000    0.000    0.000 {issubclass}

       60    0.000    0.000    0.000    0.000 {len}

       12    0.000    0.000    0.000    0.000 {max}

       24    0.000    0.000    0.000    0.000 {method '__array_prepare__' of 'numpy.ndarray' objects}

       24    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}

       12    0.059    0.005    0.059    0.005 {method 'astype' of 'numpy.ndarray' objects}

       12    0.058    0.005    0.058    0.005 {method 'copy' of 'numpy.ndarray' objects}

        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

       24    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}

       12    0.220    0.018    0.220    0.018 {method 'rand' of 'mtrand.RandomState' objects}

       12    0.000    0.000    0.000    0.000 {method 'transpose' of 'numpy.ndarray' objects}

       12    0.000    0.000    0.000    0.000 {method 'view' of 'numpy.ndarray' objects}

       12    0.000    0.000    0.000    0.000 {min}

       24    0.257    0.011    0.257    0.011 {numpy.core.multiarray._fastCopyAndTranspose}

        1    0.000    0.000    0.000    0.000 {numpy.core.multiarray.arange}

       36    0.000    0.000    0.000    0.000 {numpy.core.multiarray.array}

       24    0.035    0.001    0.035    0.001 {numpy.core.multiarray.zeros}

       12    5.078    0.423    5.078    0.423 {numpy.linalg.lapack_lite.dgesv}
```

The output is the same as the one shown in the article on timeit with ipython.  In addition to the [timeit article](/blog/profilingdeunscriptpythoncontimeit), the meaning of each column is shown below:

- `ncalls`: Number of calls.
- `tottime`: Total time spent in a function.
- `percall`: Time per call, calculated as the total time divided by the number of calls.
- `cumtime`: Cumulative time spent in a function and in the functions it calls, including recursive calls.  

You can download the script code from [bitbucket (broken link)](https://bitbucket.org/ecrespo/ernesto-ecrespo.blogspot/src/a3294957f9a7a41932385d064d7799ad1dd80b60/cprofile/matrizinversa.py?at=default).



##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)