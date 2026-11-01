Title: S.O.L.I.D. Principles - 2. Open/closed principle. (OCP - Open/closed principle) 
Date:  2022-05-07 13:00
Category: Tutorial Python
Tags: python,solid
lang: en
translation: true
Slug: python_solid2
Authors: Ernesto Crespo
Summary: Second article on the SOLID principles, in this case the open/closed principle.

In software engineering there is the [S.O.L.I.D](https://es.wikipedia.org/wiki/SOLID) principle. The SOLID principles are guidelines that can be applied in software development to eliminate bad designs, which would otherwise force the programmer to refactor until the code is readable and extensible. 

Its principles are:

* Single responsability principle - Single responsibility principle.
* Open/closed principle - Open/closed principle.
* Liskov substitution principle - Liskov substitution principle.
* Interface segregation principle - Interface segregation principle.
* Dependency inversion principle - Dependency inversion principle.


Below is a video by [ArjanCodes](https://www.youtube.com/watch?v=pTB30aXS77U&t=1s) that explains the S.O.L.I.D principles with python code:

<iframe width="560" height="315" src="https://www.youtube.com/embed/pTB30aXS77U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

The [previous article](/blog/python_solid1) is about the single responsibility principle.


The [open/closed principle](https://es.wikipedia.org/wiki/Principio_de_abierto/cerrado) states that a software entity (class, module, function, etc) must remain open for extension, but closed for modification. That is, it must be possible to extend the behavior of such an entity without modifying its source code.  

In other words, the code should be written in such a way that, when adding new functionality, you do not have to modify previously written code, which may be in use by other users



1. From the single responsibility principle we have the following code, where the Order class was separated from the PaymentProcess class: 


```python

# Ahora se tiene una clase que sólo manejará métodos de la orden y se separa el método de pago en otra clase llamada PaymentProcessor


class Order:

    def __init__(self):
        self.items = []
        self.quantities = []
        self.prices = []
        self.status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total


# Clase PaymentProcessor con los métodos: pago con debito y pago a credito. 

class PaymentProcessor:
    def pay_debit(self, order, security_code):
        print("Processing debit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

    def pay_credit(self, order, security_code):
        print("Processing credit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"



# Ahora se instancia la clase Order, y se agrega los items a comprar en la orden.

order = Order()
order.add_item("Teclado", 1, 50)
order.add_item("Memoria", 1, 150)
order.add_item("Cable USB", 2, 5)

# Imprime el precio total de la orden
print(order.total_price())

# Instancia la clase de procesador de pago y se llama al método pagar con debito pasando como argumento la orden y el código de seguridad de la tarjeta.

processor = PaymentProcessor()
processor.pay_debit(order, "0372846")

```

The output is the following:

```bash 

210
Processing debit payment type
Verifying security code: 0372846

```

To comply with the open/closed principle, an Abstract class that defines the payment Process will be used, and a class is created for each payment type that inherits from that abstract class; now the payment process methods are separated into classes with a single method.

```python 

from abc import ABC, abstractmethod

# La clase Order se mantiene igual:

class Order:

    def __init__(self):
        self.items = []
        self.quantities = []
        self.prices = []
        self.status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total


# Se crea una clase abstracta del proceso de pago:
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self,order,security_code):
        pass 


# Se crea la clase de pago con debito que hereda de la clase abstracta
class DebitPaymentProcessor(PaymentProcessor):
    def pay(self,order,security_code):
        print("Processing debit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

# Se crea la clase de pago con TC que hereda de la clase abstracta
class CreditPaymentProcessor(PaymentProcessor):
    def pay(self,order,security_code):
        print("Processing credit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"


# Se crea el método de pago paypal
class PaypalPaymentProcessor(PaymentProcessor):
    def pay(self,order,security_code):
        print("Processing paypal payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"


# Ahora se instancia la clase Order, y se agrega los items a comprar en la orden.

order = Order()
order.add_item("Teclado", 1, 50)
order.add_item("Memoria", 1, 150)
order.add_item("Cable USB", 2, 5)

# Imprime el precio total de la orden
print(order.total_price())


# Se define el método de pago debito

processor = DebitPaymentProcessor()
processor.pay(order, "0372846")

# Se define el método de pago TC

processor = CreditPaymentProcessor()
processor.pay(order, "0372846")



# Se define el método de pago paypal
processor = PaypalPaymentProcessor()
processor.pay(order, "0372846")

```

The output is the following: 

```bash 

210
Processing debit payment type
Verifying security code: 0372846

Processing debit payment type
Verifying security code: 0372846

Processing credit payment type
Verifying security code: 0372846

Processing credit payment type
Verifying security code: 0372846
```

Now, when a new payment method is required, you simply create a class for that method that inherits from the abstract class; there is no longer any need to touch the classes or methods of the other payment methods.


2. QR code generation. 

From the article on the single responsibility principle we have the following code: 

```python

class GenerateQR:
    
    def __init__(self,version):
        self.version = version
    
    def myqr(self,my_qr,text,save_name,colorize,save_dir,picture=None):
        if not picture: 
            return myqr.run(words=text, version=my_qr.version, save_name=save_name,
                            save_dir=save_dir, colorized=colorize, contrast=1.0, brightness=1.0)
            
        return myqr.run(words=text, version=my_qr.version, save_name=save_name, picture=picture,
                        save_dir=save_dir, colorized=colorize, contrast=1.0, brightness=1.0)

    
    def qrcode(self,my_qr,text,save_name,box_size,border,fit,fill,back_color):
        self.qr = qrc.QRCode(
            version=my_qr.version,
            box_size=box_size,
            border=border
        )
        self.qr.add_data(text)
        self.qr.make(fit=fit)
        self.img = self.qr.make_image(
            fill=fill, back_color=back_color)
        self.img.save(save_name)

gen_qr = GenerateQR(version=1)
# Generar QR con myqr
gen_qr.myqr(my_qr,"hola mundo!","hola.png",True,"./")
# generar qr con qrcode
gen_qr.qrcode(my_qr,"hola mundo2!",'hola2.png',10,5,True,'black','white')

```

There is a single class with one method for each library, but if you want to add a new library you have to modify the class, and this breaks the principle. To avoid it, an abstract class is created, plus one class per library that inherits from the abstract class; that way, if there is a new library, you just create a new class without needing to modify the existing classes.

```python 

from abc import ABC, abstractmethod
import qrcode as qrc
from MyQR import myqr

# Clase abstracta
class GenerateQR(ABC):
    @abstractmethod
    def generate(self,my_qr,text,save_name,**kwargs):
        pass 


# Clase para la librería MyQR que hereda de la clase abstracta.
class GenerateMyQR(GenerateQR):

    def __init__(self, version):
        self.version = version
    
    def generate(self,my_qr,text,save_name,**kwargs):
        # colorize,save_dir,picture=None
        colorize = kwargs.get("colorize", True)
        save_dir = kwargs.get("save_dir","./")
        picture = kwargs.get("picture",None)
        if not picture: 
            return myqr.run(words=text, version=self.version, save_name=save_name,
                            save_dir=save_dir, colorized=colorize, contrast=1.0, brightness=1.0)
            
        return myqr.run(words=text, version=my_qr.version, save_name=save_name, picture=picture,
                        save_dir=save_dir, colorized=colorize, contrast=1.0, brightness=1.0)

# Clase de la librería qr_code que hereda de la clase abstracta.
class GenerateQRCode(GenerateQR):
    
    def __init__(self, version):
        self.version = version

    def generate(self,my_qr,text,save_name,**kwargs):
        # box_size,border,fit,fill,back_color
        box_size = kwargs.get("box_size",10)
        border = kwargs.get("border",5)
        fit = kwargs.get("fit",True)
        fill = kwargs.get("fill","black")
        back_color = kwargs.get("back_color","white")
        self.qr = qrc.QRCode(
            version=self.version,
            box_size=box_size,
            border=border
        )
        self.qr.add_data(text)
        self.qr.make(fit=fit)
        self.img = self.qr.make_image(
            fill=fill, back_color=back_color)
        self.img.save(save_name)

# Se crea la instancia de la clase pasandole la versión del código QR que se quiere usar 
# para la librería MyQR y luego para qr_code
gen_qr = GenerateMyQR(version=1)
gen_qr.generate(my_qr,"Hola mundo","hola1c.png")

gen_qrcode = GenerateQRCode()
gen_qrcode.generate(my_qr,"Hola mundo","hola2c.png")
```

As explained, it is no longer necessary to touch the code of the existing library classes, and if there is a new library you only need to create a new class inheriting from the abstract class.

References: 

* [Principios SOLID en Python](https://softwarecrafters.io/python/principios-solid-python)
* [Los principios SOLID ilustrados en ejemplos sencillos de Python](https://blog.damavis.com/los-principios-solid-ilustrados-en-ejemplos-sencillos-de-python/)
* [Principios SOLID explicados en Python con ejemplos.](https://ichi.pro/es/principios-solid-explicados-en-python-con-ejemplos-56291217871103)
* [The S.O.L.I.D Principles in Python (broken link)](https://medium.com/geekculture/the-s-o-l-i-d-principles-in-python-a041c5aa9969#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ2M2RiZTczYWFkODhjODU0ZGUwZDhkNmMwMTRjMzZkYzI1YzQyOTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2NDY5NjE2MDYsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMzA0ODgwMTUxNTE4Mzk4NTA5MyIsImVtYWlsIjoiZWNyZXNwb0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiMjE2Mjk2MDM1ODM0LWsxazZxZTA2MHMydHAyYTJqYW00bGpkY21zMDBzdHRnLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwibmFtZSI6IkVybmVzdG8gQ3Jlc3BvIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdpNzZJNGhTTXQ3U1hYbzZjdHdaNDloeDlKbTF3cU93UXZiTU0zbWtHMD1zOTYtYyIsImdpdmVuX25hbWUiOiJFcm5lc3RvIiwiZmFtaWx5X25hbWUiOiJDcmVzcG8iLCJpYXQiOjE2NDY5NjE5MDYsImV4cCI6MTY0Njk2NTUwNiwianRpIjoiNWM2ZWFkNjRjNjcyOGYxY2VhNmJhNjhkNGYzYTYyZTI3MzUxZTFhZCJ9.jMgz-2c2M8jmF-pepfaLohkEc75VeswUa7S1N6h6VgS7DOHw4rUVBjza_7VYEa_3gPpFHKiX_8OYI9_CjPJa4x1VU2encPP_FEHDU6m0lILEVVYkSV4LS7jfkJRe93GE51E8rQPUdR2IxcPc_P8mlE3Co-plLIktqAmW4_fyyMyLquDj-CjXfTpZ6RZs85rf3XH1qM-LOF8jhydDMKAhY8Iej4PCsT56C-kr26En3SqaA5BNgEftLIxhjQoFuZNCj8c7g5PuUztdmQ6UhjFA1-G392HnMx7rMYsfjeXxs2zaTeSjPh-z4JwyqkBTxZm6_rp37RpeQJFcGKzxWZNx8g)
* [Principios SOLID](https://enmilocalfunciona.io/principios-solid/)

* [ArjanCodes](https://www.youtube.com/watch?v=pTB30aXS77U&t=1s)

* [solid principles with python (broken link)](https://medium.com/@didemyaniktepe/solid-principles-with-python-97b5e7250ed7#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImZjYmQ3ZjQ4MWE4MjVkMTEzZTBkMDNkZDk0ZTYwYjY5ZmYxNjY1YTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2NTE5NjI5NzgsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMzA0ODgwMTUxNTE4Mzk4NTA5MyIsImVtYWlsIjoiZWNyZXNwb0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiMjE2Mjk2MDM1ODM0LWsxazZxZTA2MHMydHAyYTJqYW00bGpkY21zMDBzdHRnLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwibmFtZSI6IkVybmVzdG8gQ3Jlc3BvIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdpT19yRlhDM0VVWWRocmFLWjBHUmJNVlpRenhwSHRWQnl0MmI0MmU4WT1zOTYtYyIsImdpdmVuX25hbWUiOiJFcm5lc3RvIiwiZmFtaWx5X25hbWUiOiJDcmVzcG8iLCJpYXQiOjE2NTE5NjMyNzgsImV4cCI6MTY1MTk2Njg3OCwianRpIjoiNThhMzllZDhiMDNhZDM0ZDY1NDlhZDc2YzBmN2RkODY3NDNlZTgzMiJ9.db8I06It2VvYgbS6UswUsVGpbL3-OY8fFmQ367BXgF9p21W--y6OcTsKRTQp1yKVUZXbaUUoQYtIfoC00pnn9J7NHM1Fzixx1FIf8qeUm_4Yj4iPGzLwE4QapPbwJYdB1xXOLNGfQkfHb63U6ZwObrzJZrqHatNc7dwNNzpy0757d3BXvgrSNWbLXuNcxBVrdFwHqqtjJZfsyixaTAqYi4mzjg3ljpoxlYP-USeCIASUU6OJkMyCs__XjhC0ez2lWNDuPZwC3WML130U9GsHikAWR_Ue1iOIuQfC7_N2PE-GU0pYWCfIzzTvrhBoRFMhaN5i1koEOQ9w6c9ziCvH9A)

* [SOLID Coding in Python](https://towardsdatascience.com/solid-coding-in-python-1281392a6a94)

* [5 Principles to write SOLID Code](https://towardsdatascience.com/5-principles-to-write-solid-code-examples-in-python-9062272e6bdc)

* [The 5 (SOLID) Principles of Pyhon Readable Code (broken link)](https://towardsdev.com/the-5-solid-principles-of-pyhon-readable-code-67c5a3fe5693)

* [Designing to Patterns: A Pythonic Example](https://levelup.gitconnected.com/designing-to-patterns-a-pythonic-example-14bc8ce34e81)

* [Python Open–closed principle](https://www.pythontutorial.net/python-oop/python-open-closed-principle/)

* [How to Write Clean Code (in Python) With SOLID Principles | Principle #2 (broken link)](https://medium.com/the-brainwave/how-to-write-clean-code-in-python-with-solid-principles-principle-2-c54fb647f5b7)

* [The Open-Closed Principle Explained in Python (broken link)](https://betterprogramming.pub/the-open-closed-principle-explained-in-python-f5517488f990)

---
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)