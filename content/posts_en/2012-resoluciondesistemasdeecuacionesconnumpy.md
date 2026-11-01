Title: Solving systems of equations with NumPy
Date: 2012-12-02 9:00
Category: Tutorial Python
Tags: Canaima,Debian,General,Linux,numpy,Python,Ubuntu
lang: en
translation: true

Recalling a bit about solving systems of equations with Linear Algebra.

Python, by means of NumPy, can be used to solve these systems of equations using matrices.

The equations to be solved are:
```
3x+9y-10z = 24
x-6y+4z = -4
10x-2y+8z = 20
```
These equations can be represented as a system of matrices as `A*x=B`, where, to solve for the matrix x, the inverse of A is applied, `x = inv(A)*B`. Where A in our case is `[[3 9 -10][1 -6 4][10 -2 8]` and B is `[[24][-4[[20]]`.

The code to solve the system of equations is the following:
```python
#!/usr/bin/env python

#Se importa numpy como np
import numpy as np


#Se define los valores de la matriz A
A = np.matrix([[3,9,-10],[1,-6,4],[10,-2,8]])

#Se definen los valores de la matriz B
B = np.matrix([[24],[-4],[20]])

#Se calcula el valor de X con X=inv(A)*B
X = A**(-1)*B


#Se muestra el resultado
print("El resultado de X es:",X)

#Para verificar el resultado se calcula X*A y debe dar B
print("El resultado de A*X es B-> ",A*X)
```

The result of running the script is shown below:
```python
('El resultado de X es:', matrix([[ 2.99029126],
        [ 0.40776699],
        [-1.13592233]]))
('El resultado de A*X es B-> ', matrix([[ 24.],
        [ -4.],
        [ 20.]]))
```
There is a problem when computing the inverse matrix, which is that not every matrix can be inverted, so this solution does not work in all cases. The solution is to use the [numpy.linalg.svd](https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.svd.html) function.

Instead of using the matrix class, the following code will use the array class and the `numpy.linalg.svd` function.
```python
#!/usr/bin/env python

#Se importa numpy como np
import numpy as np

#Se define los valores de la matriz A
A = np.array([[3,9,-10],[1,-6,4],[10,-2,8]])

#Se definen los valores de la matriz B
B = np.array([[24],[-4],[20]])

#Se calcula el valor de X con X=inv(A)*B
X = np.linalg.inv(A).dot(B)


#Se muestra el resultado
print("El resultado de X es:",X)
```
The result is the following:
```
('El resultado de X es:', array([[ 2.99029126],
       [ 0.40776699],
       [-1.13592233]]))
```
So the value of x is 2.99, y is 0.407 and z is -1.1359, shown with 2 different procedures.

You can find the code for these 2 examples in the [bitbucket repository of this blog's code (broken link)](https://bitbucket.org/ecrespo/ernesto-ecrespo.blogspot/src/71eb8e1fcbaf472997dbcd4d179f2423b7ee4ae6/numpy1?at=default).

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)