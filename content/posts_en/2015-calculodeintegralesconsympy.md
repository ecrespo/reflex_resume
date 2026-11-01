Title: Calculating Integrals with Sympy  
Date: 2015-02-21 10:00  
Category: Tutorial Python  
Tags: Canaima,Debian,General,Python,Ubuntu,Sympy  
lang: en
translation: true  

Continuing with the articles about the `Sympy` library, the previous articles covered the following:

- [Calculating limits with Sympy](/blog/calculodelimitesconlalibreriasympy)
- [Calculating derivatives with Sympy](/blog/calculodederivadasconsympy)

This article covers the topic of calculating Integrals.

Next, run ipython notebook (if you want to load the notebook file for this article, you can download it from the following [link (broken link)](https://bitbucket.org/ecrespo/ernesto-ecrespo.blogspot/src/087eb1686b0d118e545f1e7c285f7ad007a5bf41/integrales/integrales.ipynb?at=default)).

The tutorial script is shown below:
```python
# coding: utf-8

# In[16]:

#Se importa sympy

from sympy import *

x = Symbol('x')

# In[26]:

diff(5*(x**5)+3*(x**3)-6*x+5,x); #Se calcula la derivada de la funcion 5(x^5)+3(x^3)-6x+5

# In[27]:

integrate(Out[3],x);#Se integra el resultado de la derivada,noten q el resultado es la ecuación de In[3] pero sin el valor constante

# In[19]:

integrate(cos(x)**2+sin(x),x); #Se inte cos(x)**2+sin(x) con respecto a x

# In[20]:

pprint (Integral(cos(x)**2+sin(x),x));#Se muestra la integral de la ecuación anterior

# In[28]:

integrate(Out[27],(x,0,5));#Se calcula el valor de la integral de 0 a 5 de la ecuación de la salida 27

# In[29]:

integrate(cos(x)**2+sin(x),(x,0,pi));#Se calcula la integral con el rango de 0 a pi
```

The image of the notebook execution is shown below:

![](./images/calculodeintegralesconsympy-1.png)

For a better view of the exercise I recommend running the notebook from the link above.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
