Title: Back to basics, OOP in Python (composition) (part 9)  
Date: 2016-12-31 18:00  
Category: Tutorial Python  
Tags: Python,POO
lang: en  
translation: true  


To finish the series of articles on [object-oriented programming with python](/blog/tags), 

Composition means using objects inside other objects without using inheritance.

The UML diagram of two objects A and B is shown below. 

![](./images/volviendoalobasicopooenpythoncomposicion9-1.png)

The example code is shown below: 

```python
#!/usr/bin/env python3


# -*- coding: utf-8 -*-


"""Composición"""


class A(object):


    def a1(self):


        print("a1")


class B(object):


    def b(self):


        print ("b")


        A().a1()


if __name__ =="__main__":


    objetoB = B()


    objetoB.b()

```

When you run the code you get the following output:
```
b
a1
```

This example is fairly simple. Composition is another way of reusing code.

You can see the code on [gitlab](https://gitlab.com/ecrespo/tutorial-poo/blob/master/ej16.py). 



##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)




