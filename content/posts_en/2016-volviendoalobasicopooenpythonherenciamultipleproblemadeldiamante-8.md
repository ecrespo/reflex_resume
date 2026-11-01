Title: Back to basics, OOP in Python (multiple inheritance, the diamond problem) (part 8)  
Date: 2016-12-31 17:00  
Category: Tutorial Python    
Tags: Python,POO
lang: en  
translation: true  

Continuing with the articles about [object-oriented programming in python](/blog/tags).

The previous article explained how to work with multiple inheritance. Now the diamond problem and how Python solves it will be explained.

Diamond inheritance is shown in the following figure:

![](./images/volviendoalobasicopooenpythonherenciamultipleproblemadeldiamante8-1.png)


Where the parent class is class A, and classes B and C inherit from it; finally class D inherits from both B and C, and both of those classes, as we already know, inherit from A. Through which path is A inherited, through B or through C?

That is the diamond problem itself; you can find more information on the [wikipedia](https://es.wikipedia.org/wiki/Problema_del_diamante) page. 

Each language has its own way of solving this problem. In the case of Python, it builds a list of classes, which are searched from left to right and from bottom to top (D,B,A,C,A), and then removes all occurrences of a repeated class except the last one. So the resolution order ends up being D,B,C,A. 

An example in python is shown below: 

```python

#!/usr/bin/env python3


# -*- coding: utf-8 -*-


"""multiple herencia, problema del diamante"""




class A(object):


    def __init__(self,mensajeA):


        self.mensajeA = mensajeA




    @staticmethod


    def quienSoy():


        return "Soy A"





class B(A):


    def __init__(self,mensajeA, mensajeB):


        A.__init__(self,mensajeA)


        self.mensajeB = mensajeB





    @staticmethod


    def quienSoy():


        return "Soy B"




class C(A):


    def __init__(self,mensajeA,mensajeC):


        A.__init__(self,mensajeA)


        self.mensajeC = mensajeC





    @staticmethod


    def quienSoy():


        return "Soy C"




class D(B,C):


    def __init__(self,mensajeA,mensajeB,mensajeC,mensajeD):


        B.__init__(self,mensajeA,mensajeB)


        C.__init__(self,mensajeA,mensajeC)


        self.mensajeD = mensajeD




    @staticmethod


    def quienSoy():


        return "Soy D"




if __name__ == '__main__':


    ca = A("prueba de A")


    cb = B("prueba de A desde B","prueba de B")


    cc = C("prueba de A desde C","prueba de C")


    cd = D("prueba de A desde D","prueba de B desde D","prueba de C desde D","prueba de D")


    print ("Mensaje de A:",ca.mensajeA)


    print ("Quien es?: ",ca.quienSoy())


    print ("Mensaje 1 de B:", cb.mensajeB)


    print("Mensaje 2 de B:", cb.mensajeA)


    print ("Quien es?:",cb.quienSoy())


    print ("Mensaje 1 de C:", cc.mensajeC)


    print ("Mensaje 2 de C:", cc.mensajeA)


    print ("Quien es?:", cc.quienSoy())


    print ("Mensaje 1 de D:", cd.mensajeD)


    print ("Mensaje 2 de D:", cd.mensajeB)


    print ("Mensaje 3 de D:", cd.mensajeC)


    print ("Mensaje 4 de D:", cd.mensajeA)


    print("Quien es?:", cd.quienSoy())

```


Note that super was not used, because to resolve the evaluation it is easier to define the object directly instead of using super as a call into the inheritance chain. 


When the code is run, the following output is produced:
```
Mensaje de A: prueba de A
Quien es?:  Soy A
Mensaje 1 de B: prueba de B
Mensaje 2 de B: prueba de A desde B
Quien es?: Soy B
Mensaje 1 de C: prueba de C
Mensaje 2 de C: prueba de A desde C
Quien es?: Soy C
Mensaje 1 de D: prueba de D
Mensaje 2 de D: prueba de B desde D
Mensaje 3 de D: prueba de C desde D
Mensaje 4 de D: prueba de A desde D
Quien es?: Soy D
``` 

As you can see, the execution of the last class shows the sequence explained in this article.

You can download the code of this example from [gitlab](https://gitlab.com/ecrespo/tutorial-poo/blob/master/ej18.py). 



##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)



