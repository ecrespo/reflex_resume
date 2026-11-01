Title: Calculating Pi with the Monte Carlo method using Python.
Date: 2017-05-08 09:00
Category: Tutorial Python
Tags: General,Numpy,Python,Método de Montecarlo
lang: en
translation: true

The Monte Carlo method is a numerical statistical method used to approximate complex mathematical expressions that are expensive to evaluate exactly. For more information you can check [wikipedia](http://es.wikipedia.org/wiki/M%C3%A9todo_de_Montecarlo).

The mathematical expression to be solved is the calculation of Pi.

In this article I will show two versions of the use of the Monte Carlo Method.

In the first example, the algorithm was taken from Pascal code and ported to Python. Here is the code:

```python
#!/usr/bin/env python

#Se importa el modulo random

import random



#Se define la funcion

def Pi(limite=10000000):

    dentro = 0

    contador = 0

    #Se hace un ciclo hasta que contador sea igual al limite

    while contador < limite:

        #Se calcula  que los puntos esten dentro del radio del circulo

        #Si es asi se incrementa la variable dentro. y luego se incrementa

        #contador para pasar al siguiente ciclo.

        if ((random.random()**2 + random.random()**2) <= 1):

            dentro += 1

        contador += 1

    #Se retorna el resultado de la cantida de puntos dentro del circulo

    #entre el limite por 4.

    return 4.0*float(dentro)/limite



if __name__ == "__main__":

    n = (10000, 1000000,100000000)

    for i in n:

        print ("El valor de pi es: {0:2.8f} para n {1}".format(Pi(i),i))

```  

Running the code gives:

```
El valor de pi es: 3.14960000 para n 10000
El valor de pi es: 3.14308000 para n 1000000
El valor de pi es: 3.14141900 para n 100000000
```

Increasing the value of n gives a more precise value of PI, although of course it also takes longer to calculate.

The next example is based on an English-language article published on Medium called [Day 9: Monte Carlo Pi (broken link)](http://medium.com/100-days-of-algorithms/day-9-monte-carlo-%CF%80-7ae010743bde), and its code is on [github](http://github.com/coells/100days/blob/master/day%2009%20-%20monte%20carlo%20-%20pi.ipynb).

The code is shown below:

```python

#!/usr/bin/env python

#Se importa el modulo numpy

import numpy as np





def pi(n, batch=1000):

    t = 0

    for i in range(n // batch):

        p = np.random.rand(batch, 2)

        p = (p * p).sum(axis=1)

        t += (p <= 1).sum()

    return 4 * float(t) / n





if __name__ == "__main__":

    print ("El valor de pi es: {0:2.8f} para n {1}".format(pi(10**8),10**8))

```

Running it gives:
```
El valor de pi es: 3.14146076 para n 100000000
```

As you can see, the latter version has fewer lines of code and is faster. 



##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)