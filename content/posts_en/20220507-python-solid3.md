Title: S.O.L.I.D. Principles - 3. Liskov Substitution Principle (LSP) 
Date:  2022-05-08 13:00
Category: Tutorial Python
Tags: python,solid
lang: en
translation: true
Slug: python_solid3
Authors: Ernesto Crespo
Summary: Third article on the SOLID principles, in this case the Liskov Substitution Principle.

In software engineering there is the [S.O.L.I.D](https://es.wikipedia.org/wiki/SOLID) principle. The SOLID principles are guidelines that can be applied in software development to eliminate bad designs that force the programmer to refactor until the code is readable and extensible. 

Its principles are:

* Single responsability principle - Single responsibility principle.
* Open/closed principle - Open/closed principle.
* Liskov substitution principle - Liskov substitution principle.
* Interface segregation principle - Interface segregation principle.
* Dependency inversion principle - Dependency inversion principle.


Below I leave a video by [ArjanCodes](https://www.youtube.com/watch?v=pTB30aXS77U&t=1s) that explains the S.O.L.I.D principles with python code:

<iframe width="560" height="315" src="https://www.youtube.com/embed/pTB30aXS77U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

The previous articles:
* [Single responsibility principle](/blog/python_solid1).
* [Open/closed principle](/blog/python_solid2)

The [Liskov substitution principle](https://es.wikipedia.org/wiki/Principio_de_sustituci%C3%B3n_de_Liskov) is defined as: Every class that inherits from another can be used as its parent without needing to know the differences between them.

The main idea behind the Liskov substitution principle is that, for any class, a client should be able to use any of its subtypes indistinguishably, without even noticing, and therefore without compromising the expected behavior at runtime. This means that clients are completely isolated from, and unaware of, changes in the class hierarchy.



1. From the open/closed principle, an abstract class was created and different classes that inherit from that abstract class were created for each payment process. The code is shown below.


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

Processing paypal payment type
Verifying security code: 0372846
```

There is an error in how the paypal payment process class was created. Paypal does not need a security code, it needs an email address, but modifying the payment method of the paypal class would violate the Liskov substitution principle.

To solve it, the security code argument is removed and it is set when initializing the respective payment method.

The code is shown below:

```python

from abc import ABC, abstractmethod

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


# La clase abstracta con el método de pago que ya no maneja el código de seguridad.
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self,order):
        pass 


# Se define las clases de pago a debito y crédito y se le define el código de seguridad.
class DebitPaymentProcessor(PaymentProcessor):
    
    def __init__(self,security_code):
        self.security_code = security_code
    
    def pay(self,order):
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):
    
    def __init__(self,security_code):
        self.security_code = security_code
    
    def pay(self,order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

# Para el caso de paypal se define el correo electrónico.
class PaypalPaymentProcessor(PaymentProcessor):
    
    def __init__(self,email_address):
        self.email_address = email_address
        
    
    def pay(self,order):
        print("Processing paypal payment type")
        print(f"Verifying email address: {self.email_address}")
        order.status = "paid"

# Ahora se instancia la clase Order, y se agrega los items a comprar en la orden.

order = Order()
order.add_item("Teclado", 1, 50)
order.add_item("Memoria", 1, 150)
order.add_item("Cable USB", 2, 5)

# Imprime el precio total de la orden
print(order.total_price())


# Se define el método de pago debito

processor = DebitPaymentProcessor("0372846")
processor.pay(order)

# Se define el método de pago TC

processor = CreditPaymentProcessor("0372846")
processor.pay(order)



# Se define el método de pago paypal
processor = PaypalPaymentProcessor("h@h.com")
processor.pay(order)

```

The output produces the following: 

```bash 

210
Processing debit payment type
Verifying security code: 0372846

Processing debit payment type
Verifying security code: 0372846

Processing credit payment type
Verifying security code: 0372846

Processing paypal payment type
Verifying email address: h@h.com
```




2. QR code generation. 

From the article on the open/closed principle we have the following code: 


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

The change that will allow compliance with this principle is to initialize the classes with the kwargs instead of passing them to the generate method. 

```python

from abc import ABC, abstractmethod
import qrcode as qrc
from MyQR import myqr

class GenerateQR(ABC):
    @abstractmethod
    def generate(self,text):
        pass 

class GenerateMyQR(GenerateQR):
    
    def __init__(self,version,**kwargs):
        self.version = version
        self.colorize = kwargs.get("colorize", True)
        self.save_dir = kwargs.get("save_dir","./")
        self.picture = kwargs.get("picture",None)
        self.save_name = kwargs.get("save_name","hola1e.png")
                 
    def generate(self,text):
        
        if not self.picture: 
            return myqr.run(words=text, version=my_qr.version, save_name=self.save_name,
                            save_dir=self.save_dir, colorized=self.colorize, contrast=1.0, brightness=1.0)
            
        return myqr.run(words=text, version=self.version, save_name=self.save_name, picture=self.picture,
                        save_dir=self.save_dir, colorized=self.colorize, contrast=1.0, brightness=1.0)


class GenerateQRCode(GenerateQR):
    
    def __init__(self,version,**kwargs):
        self.version = version
        self.save_name = kwargs.get("save_name","hola2e.png")
        self.box_size = kwargs.get("box_size",10)
        self.border = kwargs.get("border",5)
        self.fit = kwargs.get("fit",True)
        self.fill = kwargs.get("fill","black")
        self.back_color = kwargs.get("back_color","white")
    
    def generate(self,text,):
        # box_size,border,fit,fill,back_color
        
        self.qr = qrc.QRCode(
            version=self.version,
            box_size=self.box_size,
            border=self.border
        )
        self.qr.add_data(text)
        self.qr.make(fit=self.fit)
        self.img = self.qr.make_image(
            fill=self.fill, back_color=self.back_color)
        self.img.save(self.save_name)


gen_qr = GenerateMyQR(version=1,{"save_name":"hola2.png"})
gen_qr.generate("Hola mundo")

gen_qr = GenerateQRCode(version=1,{"save_name":"hola2.png"})
gen_qr.generate("Hola mundo")

```

References: 

* [SOLID Principles in Python](https://softwarecrafters.io/python/principios-solid-python)
* [The SOLID principles illustrated in simple Python examples](https://blog.damavis.com/los-principios-solid-ilustrados-en-ejemplos-sencillos-de-python/)
* [SOLID principles explained in Python with examples.](https://ichi.pro/es/principios-solid-explicados-en-python-con-ejemplos-56291217871103)
* [The S.O.L.I.D Principles in Python (broken link)](https://medium.com/geekculture/the-s-o-l-i-d-principles-in-python-a041c5aa9969#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ2M2RiZTczYWFkODhjODU0ZGUwZDhkNmMwMTRjMzZkYzI1YzQyOTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2NDY5NjE2MDYsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMzA0ODgwMTUxNTE4Mzk4NTA5MyIsImVtYWlsIjoiZWNyZXNwb0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiMjE2Mjk2MDM1ODM0LWsxazZxZTA2MHMydHAyYTJqYW00bGpkY21zMDBzdHRnLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwibmFtZSI6IkVybmVzdG8gQ3Jlc3BvIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdpNzZJNGhTTXQ3U1hYbzZjdHdaNDloeDlKbTF3cU93UXZiTU0zbWtHMD1zOTYtYyIsImdpdmVuX25hbWUiOiJFcm5lc3RvIiwiZmFtaWx5X25hbWUiOiJDcmVzcG8iLCJpYXQiOjE2NDY5NjE5MDYsImV4cCI6MTY0Njk2NTUwNiwianRpIjoiNWM2ZWFkNjRjNjcyOGYxY2VhNmJhNjhkNGYzYTYyZTI3MzUxZTFhZCJ9.jMgz-2c2M8jmF-pepfaLohkEc75VeswUa7S1N6h6VgS7DOHw4rUVBjza_7VYEa_3gPpFHKiX_8OYI9_CjPJa4x1VU2encPP_FEHDU6m0lILEVVYkSV4LS7jfkJRe93GE51E8rQPUdR2IxcPc_P8mlE3Co-plLIktqAmW4_fyyMyLquDj-CjXfTpZ6RZs85rf3XH1qM-LOF8jhydDMKAhY8Iej4PCsT56C-kr26En3SqaA5BNgEftLIxhjQoFuZNCj8c7g5PuUztdmQ6UhjFA1-G392HnMx7rMYsfjeXxs2zaTeSjPh-z4JwyqkBTxZm6_rp37RpeQJFcGKzxWZNx8g)
* [SOLID Principles](https://enmilocalfunciona.io/principios-solid/)

* [ArjanCodes](https://www.youtube.com/watch?v=pTB30aXS77U&t=1s)

* [solid principles with python (broken link)](https://medium.com/@didemyaniktepe/solid-principles-with-python-97b5e7250ed7#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImZjYmQ3ZjQ4MWE4MjVkMTEzZTBkMDNkZDk0ZTYwYjY5ZmYxNjY1YTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2NTE5NjI5NzgsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMzA0ODgwMTUxNTE4Mzk4NTA5MyIsImVtYWlsIjoiZWNyZXNwb0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiMjE2Mjk2MDM1ODM0LWsxazZxZTA2MHMydHAyYTJqYW00bGpkY21zMDBzdHRnLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwibmFtZSI6IkVybmVzdG8gQ3Jlc3BvIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdpT19yRlhDM0VVWWRocmFLWjBHUmJNVlpRenhwSHRWQnl0MmI0MmU4WT1zOTYtYyIsImdpdmVuX25hbWUiOiJFcm5lc3RvIiwiZmFtaWx5X25hbWUiOiJDcmVzcG8iLCJpYXQiOjE2NTE5NjMyNzgsImV4cCI6MTY1MTk2Njg3OCwianRpIjoiNThhMzllZDhiMDNhZDM0ZDY1NDlhZDc2YzBmN2RkODY3NDNlZTgzMiJ9.db8I06It2VvYgbS6UswUsVGpbL3-OY8fFmQ367BXgF9p21W--y6OcTsKRTQp1yKVUZXbaUUoQYtIfoC00pnn9J7NHM1Fzixx1FIf8qeUm_4Yj4iPGzLwE4QapPbwJYdB1xXOLNGfQkfHb63U6ZwObrzJZrqHatNc7dwNNzpy0757d3BXvgrSNWbLXuNcxBVrdFwHqqtjJZfsyixaTAqYi4mzjg3ljpoxlYP-USeCIASUU6OJkMyCs__XjhC0ez2lWNDuPZwC3WML130U9GsHikAWR_Ue1iOIuQfC7_N2PE-GU0pYWCfIzzTvrhBoRFMhaN5i1koEOQ9w6c9ziCvH9A)

* [SOLID Coding in Python](https://towardsdatascience.com/solid-coding-in-python-1281392a6a94)

* [5 Principles to write SOLID Code](https://towardsdatascience.com/5-principles-to-write-solid-code-examples-in-python-9062272e6bdc)

* [The 5 (SOLID) Principles of Pyhon Readable Code (broken link)](https://towardsdev.com/the-5-solid-principles-of-pyhon-readable-code-67c5a3fe5693)

* [Designing to Patterns: A Pythonic Example](https://levelup.gitconnected.com/designing-to-patterns-a-pythonic-example-14bc8ce34e81)

* [How to Write Clean Code (in Python) With SOLID Principles | Principle #3 (broken link)](https://medium.com/the-brainwave/principle-3-how-to-write-clean-code-in-python-with-solid-principles-6aedf7cf47be)

* [The Liskov Substitution Principle (LSP) Explained in Python (broken link)](https://medium.com/better-programming/the-liskov-substitution-principle-lsp-explained-in-python-6ab92b29d0b8)

---
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
