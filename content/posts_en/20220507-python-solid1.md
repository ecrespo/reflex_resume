Title: S.O.L.I.D. Principles - 1. Single Responsibility Principle (SRP - Single Responsible Principle) 
Date:  2022-05-07 12:00
Category: Tutorial Python
Tags: python,solid
lang: en
translation: true
Slug: python_solid1
Authors: Ernesto Crespo
Summary: First article about the SOLID principles, in this case the single responsibility principle.

In software engineering there is the [S.O.L.I.D](https://es.wikipedia.org/wiki/SOLID) principle. The SOLID principles are guidelines that can be applied in software development to eliminate bad designs, which would otherwise force the programmer to refactor until the code is readable and extensible. 

Its principles are:

* Single responsability principle - Single responsibility principle.
* Open/closed principle - Open/closed principle.
* Liskov substitution principle - Liskov substitution principle.
* Interface segregation principle - Interface segregation principle.
* Dependency inversion principle - Dependency inversion principle.


Below is a video by [ArjanCodes](https://www.youtube.com/watch?v=pTB30aXS77U&t=1s) that explains the S.O.L.I.D principles with python code:

<iframe width="560" height="315" src="https://www.youtube.com/embed/pTB30aXS77U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



The [single responsibility principle](https://es.wikipedia.org/wiki/Principio_de_responsabilidad_%C3%BAnica) states that each module or class should have responsibility over a single part of the functionality provided, and this responsibility should be entirely encapsulated by the class. All its services should be narrowly aligned with that responsibility. 


I will use Arjan's code example and then show the code of a QR code generator in python and how, by following the S.O.L.I.D. principle, its readability and extensibility are improved.

1. Order class that has items, quantities, prices and status. With the methods add_item (add an item), total_price (total price) and pay (payment). 

```python

class Order:

    def __init__(self):

        self.items = []
        self.quantities = []
        self.prices = []
        self.status = "open"

    def add_item(self, name, quantity, price):
        # Agrega un item con la cantidad y precio a la orden.
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        # Retorna el precio total a pagar.
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total

    def pay(self, payment_type, security_code):
        # Genera el pago según la forma de pago, debito o crédito.
        if payment_type == "debit":
            print("Processing debit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        elif payment_type == "credit":
            print("Processing credit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        else:
            raise Exception(f"Unknown payment type: {payment_type}")


# Se instancia la orden con los items, sus cantidades y precios.
order = Order()
order.add_item("Teclado", 1, 50)
order.add_item("Memoria", 1, 150)
order.add_item("Cable USB", 2, 5)

# Imprime el precio total de la orden
print(order.total_price())

# Se define la forma de pago.
order.pay("debit", "0372846")

```

The output generated is the total amount to pay and then the payment method:

```bash
210
Processing debit payment type
Verifying security code: 0372846
```

The problem with the order class is that if you want to add another payment method, you have to modify that class, which belongs to the order, when that class should not care about the payment method; it should simply create the Order.  

To improve this, a class called PaymentProcessor (payment processor) will be created, which is the one that will handle the different payment methods.

Below is the code:

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

This returns the same as in the previous code.

```bash 

210
Processing debit payment type
Verifying security code: 0372846

```

The advantage of this new version is that if you need to add a new payment method, for example payment with cryptocurrencies or paypal, you do not need to touch the Order class, only the PaymentProcessor class.

2. QR code generator.

There are libraries to generate QR codes: MyQR, qrcode and amzqr.



```python

from MyQR import myqr
import qrcode as qrc
from amzqr import amzqr

class GenQR:
    def __init__(self, version, *args, **kwargs):
        self.__version = version
        self.__box_size = kwargs.get("box_size", None)
        self.__border = kwargs.get("border", None)
        self.__fit = kwargs.get("fit", None)
        self.__fill = kwargs.get("fill", None)
        self.__back_color = kwargs.get("back_color", None)
        self.__colorize = kwargs.get("colorize", None)
        self.__picture = kwargs.get("picture", None)
        self.__save_dir = kwargs.get("save_dir", None)

    def generate(self, library="MyQR", text, save_name):
        # Genera código QR y lo guarda en un archivo
        #Se genera el código dependiendo de la librería.
        if library == "MyQR":
            if not self.__picture:
                resp = myqr.run(words=text, version=self.__version, save_name=save_name,
                                save_dir=self.__save_dir, colorized=self.__colorize, contrast=1.0, brightness=1.0, save_format='PNG')
            else:
                resp = myqr.run(words=text, version=self.__version, save_name=save_name, picture=self.__picture,
                                save_dir=self.__save_dir, colorized=self.__colorize, contrast=1.0, brightness=1.0, save_format='PNG')
            return resp

        self.__qr = qrc.QRCode(
            version=self.__version,
            )
        self.__qr.add(text)
        self.__qr.make(fit=self.__fit)
        self.__img = self.__qr.make_image(
            fill=self.__fill, back_color=self.__back_color)
        self.__img.save(save_name)

# Se crea la instancia 

genqr = GenQR(version=1)
genqr.generate(library='MyQR',text='Hola mundo!',save_name='hola.png')

```

Here the problem is that there is one method whose QR code generation depends on the library used, but if a new library has to be added, you will probably have to modify the arguments it receives and add code for the new library in that method. The solution is to create methods for each library. 

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

Another option is to create a class for each library. 

The next article will explain the open/closed principle.





References: 

* [SOLID principles in Python](https://softwarecrafters.io/python/principios-solid-python)
* [The SOLID principles illustrated in simple Python examples](https://blog.damavis.com/los-principios-solid-ilustrados-en-ejemplos-sencillos-de-python/)
* [SOLID principles explained in Python with examples.](https://ichi.pro/es/principios-solid-explicados-en-python-con-ejemplos-56291217871103)
* [The S.O.L.I.D Principles in Python (broken link)](https://medium.com/geekculture/the-s-o-l-i-d-principles-in-python-a041c5aa9969#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ2M2RiZTczYWFkODhjODU0ZGUwZDhkNmMwMTRjMzZkYzI1YzQyOTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2NDY5NjE2MDYsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMzA0ODgwMTUxNTE4Mzk4NTA5MyIsImVtYWlsIjoiZWNyZXNwb0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiMjE2Mjk2MDM1ODM0LWsxazZxZTA2MHMydHAyYTJqYW00bGpkY21zMDBzdHRnLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwibmFtZSI6IkVybmVzdG8gQ3Jlc3BvIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdpNzZJNGhTTXQ3U1hYbzZjdHdaNDloeDlKbTF3cU93UXZiTU0zbWtHMD1zOTYtYyIsImdpdmVuX25hbWUiOiJFcm5lc3RvIiwiZmFtaWx5X25hbWUiOiJDcmVzcG8iLCJpYXQiOjE2NDY5NjE5MDYsImV4cCI6MTY0Njk2NTUwNiwianRpIjoiNWM2ZWFkNjRjNjcyOGYxY2VhNmJhNjhkNGYzYTYyZTI3MzUxZTFhZCJ9.jMgz-2c2M8jmF-pepfaLohkEc75VeswUa7S1N6h6VgS7DOHw4rUVBjza_7VYEa_3gPpFHKiX_8OYI9_CjPJa4x1VU2encPP_FEHDU6m0lILEVVYkSV4LS7jfkJRe93GE51E8rQPUdR2IxcPc_P8mlE3Co-plLIktqAmW4_fyyMyLquDj-CjXfTpZ6RZs85rf3XH1qM-LOF8jhydDMKAhY8Iej4PCsT56C-kr26En3SqaA5BNgEftLIxhjQoFuZNCj8c7g5PuUztdmQ6UhjFA1-G392HnMx7rMYsfjeXxs2zaTeSjPh-z4JwyqkBTxZm6_rp37RpeQJFcGKzxWZNx8g)
* [SOLID principles](https://enmilocalfunciona.io/principios-solid/)

* [ArjanCodes](https://www.youtube.com/watch?v=pTB30aXS77U&t=1s)

* [solid principles with python (broken link)](https://medium.com/@didemyaniktepe/solid-principles-with-python-97b5e7250ed7#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImZjYmQ3ZjQ4MWE4MjVkMTEzZTBkMDNkZDk0ZTYwYjY5ZmYxNjY1YTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2NTE5NjI5NzgsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMzA0ODgwMTUxNTE4Mzk4NTA5MyIsImVtYWlsIjoiZWNyZXNwb0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiMjE2Mjk2MDM1ODM0LWsxazZxZTA2MHMydHAyYTJqYW00bGpkY21zMDBzdHRnLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwibmFtZSI6IkVybmVzdG8gQ3Jlc3BvIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdpT19yRlhDM0VVWWRocmFLWjBHUmJNVlpRenhwSHRWQnl0MmI0MmU4WT1zOTYtYyIsImdpdmVuX25hbWUiOiJFcm5lc3RvIiwiZmFtaWx5X25hbWUiOiJDcmVzcG8iLCJpYXQiOjE2NTE5NjMyNzgsImV4cCI6MTY1MTk2Njg3OCwianRpIjoiNThhMzllZDhiMDNhZDM0ZDY1NDlhZDc2YzBmN2RkODY3NDNlZTgzMiJ9.db8I06It2VvYgbS6UswUsVGpbL3-OY8fFmQ367BXgF9p21W--y6OcTsKRTQp1yKVUZXbaUUoQYtIfoC00pnn9J7NHM1Fzixx1FIf8qeUm_4Yj4iPGzLwE4QapPbwJYdB1xXOLNGfQkfHb63U6ZwObrzJZrqHatNc7dwNNzpy0757d3BXvgrSNWbLXuNcxBVrdFwHqqtjJZfsyixaTAqYi4mzjg3ljpoxlYP-USeCIASUU6OJkMyCs__XjhC0ez2lWNDuPZwC3WML130U9GsHikAWR_Ue1iOIuQfC7_N2PE-GU0pYWCfIzzTvrhBoRFMhaN5i1koEOQ9w6c9ziCvH9A)

* [SOLID Coding in Python](https://towardsdatascience.com/solid-coding-in-python-1281392a6a94)

* [5 Principles to write SOLID Code](https://towardsdatascience.com/5-principles-to-write-solid-code-examples-in-python-9062272e6bdc)

* [The 5 (SOLID) Principles of Pyhon Readable Code (broken link)](https://towardsdev.com/the-5-solid-principles-of-pyhon-readable-code-67c5a3fe5693)

* [Designing to Patterns: A Pythonic Example](https://levelup.gitconnected.com/designing-to-patterns-a-pythonic-example-14bc8ce34e81)

* [Python Single Responsibility Principle](https://www.pythontutorial.net/python-oop/python-single-responsibility-principle/)

* [How to Write Clean Code (in Python) With SOLID Principles | Principle #1 (broken link)](https://medium.com/the-brainwave/how-to-write-clean-code-in-python-with-solid-principles-principle-1-e5b0d2e6469f)

* [The Single Responsibility Principle Explained in Python (broken link)](https://betterprogramming.pub/the-single-responsibility-principle-explained-in-python-622e2d996d86)





---
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
