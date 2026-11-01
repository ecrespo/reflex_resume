Title: S.O.L.I.D. Principles - 4. Interface segregation principle (ISP) 
Date:  2022-05-08 14:00
Category: Tutorial Python
Tags: python,solid
lang: en
translation: true
Slug: python_solid4
Authors: Ernesto Crespo
Summary: Fourth article about the SOLID principles, in this case the Interface Segregation Principle.

In software engineering there is the [S.O.L.I.D](https://es.wikipedia.org/wiki/SOLID) principle. The SOLID principles are guidelines that can be applied in software development to eliminate bad designs that force the programmer to refactor until the code is readable and extensible. 

Its principles are:

* Single responsability principle - Principio de responsabilidad única.
* Open/closed principle - Principio abierto/cerrado.
* Liskov substitution principle - Principio de sustitución Liskov.
* Interface segregation principle - Principio de segregación de la interfaz.
* Dependency inversion principle - Principio de inversión de la dependencia.


Below is a video by [ArjanCodes](https://www.youtube.com/watch?v=pTB30aXS77U&t=1s) that explains the S.O.L.I.D principles with python code:

<iframe width="560" height="315" src="https://www.youtube.com/embed/pTB30aXS77U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

The previous articles:
* [Single responsibility principle](/blog/python_solid1).
* [Open/closed principle](/blog/python_solid2).
* [Liskov substitution principle](/blog/python_solid3).


The [Interface Segregation Principle](https://es.wikipedia.org/wiki/Principio_de_segregaci%C3%B3n_de_la_interfaz) states that the clients of a given program should only know about those methods they actually use and not those they do not need to use. ISP is applied to a broad and complex interface to split it into smaller and more specific ones, so that each client uses only the one it needs and can ignore the rest. This kind of reduced interface is called a role interface.


The Interface Segregation Principle states that clients should not be forced to depend on methods they do not use and therefore suggests creating specific interfaces or classes for those clients.



1. From the Liskov substitution principle we have the payment processing code. Here is the code.


```python

from abc import ABC, abstractmethod

# La clase Order se mantiene igual así que en el siguiente código no se mostrará.
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
Verifying email address: h@h.com
```


### First improvement

To comply with the segregation principle, the improvement is made in the abstract class: instead of having a single method (pay), it now also has one for authentication via SMS.

Here is the code:

```python 

from abc import ABC, abstractmethod


# La clase abstracta de procesamiento de pago
# tiene los métodos pay y auth_sms

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self,order):
        pass 
    @abstractmethod
    def auth_sms(self,code):
        pass 


# La clase DebitPaymentProcessor hereda de la clase abstracta.
class DebitPaymentProcessor(PaymentProcessor):
    
    def __init__(self,security_code):
        self.security_code = security_code
        self.verified = false
    
    def pay(self,order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"
        
    def auth_sms(self,code):
        print(f"Verifying SMS code {code}")
        self.verified = True


# La clase CreditPaymentProcessor hereda de la clase abstracta
# El problema acá es que pago con TC no necesita enviar un SMS de autenticación
# pero toca usarlo por la clase abstracta, al enviar un mensaje de error, pero 
# al hacer esto se está violando el principio de sustitución de Liskov. 
class CreditPaymentProcessor(PaymentProcessor):
    
    def __init__(self,security_code):
        self.security_code = security_code
        
    
    def pay(self,order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"
        
    # Esta es una violacion del principio de sustitución de Liskov
    def auth_sms(self,code):
        raise Exception("Credit card payments don't support SMS code authorizations")

# La clase de procesamiento de pago por paypal hereda de la clase abstracta.
class PaypalPaymentProcessor(PaymentProcessor):
    
    def __init__(self,email_address):
        self.email_address = email_address
        self.verified = False
        
    
    def pay(self,order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing paypal payment type")
        print(f"Verifying email address: {self.email_address}")
        order.status = "paid"
        
        
    def auth_sms(self,code):
        print(f"Verifying SMS code {code}")
        self.verified = True

```


### Second improvement


To fix the violation of the Liskov substitution principle, 2 abstract classes will be created, one for authentication via SMS
and another one to validate the ones that do not use SMS.

```python 

# Clase abstracta procesador de pago que ahora sólo tiene el método pay
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self,order):
        pass 


# Ahora se tiene una clase abstracta de procesamiento de pago SMS que hereda de
# la clase anterior. 
# Con sólo el método de auth_sms por que ya el de pago lo hereda de la clase abstracta anterior.
class PaymentProcessor_SMS(PaymentProcessor):

    @abstractmethod
    def auth_sms(self,code):
        pass 


# Clase procesamiento de tarjeta de debito que hereda de la 
# clase abstracta de pago SMS.
class DebitPaymentProcessor(PaymentProcessor_SMS):
    
    def __init__(self,security_code):
        self.security_code = security_code
        self.verified = false
    
    def pay(self,order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"
        
    def auth_sms(self,code):
        print(f"Verifying SMS code {code}")
        self.verified = True


# Clase de procesamiento de TC que hereda de la clase raíz.
class CreditPaymentProcessor(PaymentProcessor):
    
    def __init__(self,security_code):
        self.security_code = security_code
        
    
    def pay(self,order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


# Clase de procesamiento vía paypal que hereda de la Clase abstracta 
# que soporta SMS

class PaypalPaymentProcessor(PaymentProcessor_SMS):
    
    def __init__(self,email_address):
        self.email_address = email_address
        self.verified = False
        
    
    def pay(self,order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing paypal payment type")
        print(f"Verifying email address: {self.email_address}")
        order.status = "paid"
        
        
    def auth_sms(self,code):
        print(f"Verifying SMS code {code}")
        self.verified = True

```

Now the different classes have only the methods they need, well separated, complying with the segregation
principle. 

There is another solution, which uses composition: the SMSAuth class is created, which will have the SMS code verification method and whether it is authorized. The abstract payment processing class will only have the pay method, 


```python 

class SMSAuth:
    authorized = False
    
    def verify_code(self,code):
        print(f"Verifying code {code}")
        self.authorized = True
        
    def is_authorized(self) -> bool:
        return self.authorized 

# Clase abstracta procesamiento de pago con método pay.
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self,order):
        pass 

# Clase procesamiento pago por tarjeta de debito que hereda de la clase abstracta.
# el método init recibe como argumentos el código de seguridad y la clase SMSAuth para autorizar el pago.
class DebitPaymentProcessor(PaymentProcessor):
    
    def __init__(self,security_code, authorizer: SMSAuth):

        self.authorizer = authorizer
        self.security_code = security_code
    
    def pay(self,order):
        # Se consulta si no está autorizado el pago
        # al no tener autorización devuelve una excepción.
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

# Clase de procesamiento de pago con TC, que hereda de la clase abstracta.
# En este caso no se necesita la clase SMSAuth, sólo el código de seguridad.
class CreditPaymentProcessor(PaymentProcessor):
    
    def __init__(self,security_code):
        self.security_code = security_code
        
    
    def pay(self,order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

# Clase de procesamiento de pago vía paypal, hereda de la misma clase abstracta.
# El init recibe de argumentos dirección de correo y el objecto SMSAuth.
class PaypalPaymentProcessor(PaymentProcessor):
    
    def __init__(self,email_address,authorizer:SMSAuth):
        self.authorizer = authorizer
        self.email_address = email_address
        self.verified = False
        
    
    def pay(self,order):
        # Se valida si se tiene autorización para realizar el pago.
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
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

# Se define el autorizador.
authorizer = SMSAuth()

# Se define el método de pago debito
# ahora se le pasa el código y el autorizador.

processor = DebitPaymentProcessor("0372846",authorizer)
# Se verifica el pago
authorizer.verify_code(454545)

# Realiza el pago de la orden.
processor.pay(order)

# Se define el método de pago TC
# Para este caso se mantiene igual.
processor = CreditPaymentProcessor("0372846")
processor.pay(order)



# Se define el método de pago paypal
# Se le pasa el correo y el autorizador.
processor = PaypalPaymentProcessor("h@h.com",authorizer)
# Se realiza el pago de la orden.
processor.pay(order)
```

The output of this execution is the following:
```bash

210
Verifying code 454545
Processing debit payment type
Verifying security code: 0372846

Processing debit payment type
Verifying security code: 0372846

Processing credit payment type
Verifying security code: 0372846

Processing paypal payment type
Verifying email address: h@h.com

```

The good thing about composition is that it removes the need to create an additional abstract class.


References: 

* [SOLID Principles in Python](https://softwarecrafters.io/python/principios-solid-python)
* [The SOLID principles illustrated with simple Python examples](https://blog.damavis.com/los-principios-solid-ilustrados-en-ejemplos-sencillos-de-python/)
* [SOLID Principles explained in Python with examples.](https://ichi.pro/es/principios-solid-explicados-en-python-con-ejemplos-56291217871103)
* [The S.O.L.I.D Principles in Python (broken link)](https://medium.com/geekculture/the-s-o-l-i-d-principles-in-python-a041c5aa9969#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ2M2RiZTczYWFkODhjODU0ZGUwZDhkNmMwMTRjMzZkYzI1YzQyOTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2NDY5NjE2MDYsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMzA0ODgwMTUxNTE4Mzk4NTA5MyIsImVtYWlsIjoiZWNyZXNwb0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiMjE2Mjk2MDM1ODM0LWsxazZxZTA2MHMydHAyYTJqYW00bGpkY21zMDBzdHRnLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwibmFtZSI6IkVybmVzdG8gQ3Jlc3BvIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdpNzZJNGhTTXQ3U1hYbzZjdHdaNDloeDlKbTF3cU93UXZiTU0zbWtHMD1zOTYtYyIsImdpdmVuX25hbWUiOiJFcm5lc3RvIiwiZmFtaWx5X25hbWUiOiJDcmVzcG8iLCJpYXQiOjE2NDY5NjE5MDYsImV4cCI6MTY0Njk2NTUwNiwianRpIjoiNWM2ZWFkNjRjNjcyOGYxY2VhNmJhNjhkNGYzYTYyZTI3MzUxZTFhZCJ9.jMgz-2c2M8jmF-pepfaLohkEc75VeswUa7S1N6h6VgS7DOHw4rUVBjza_7VYEa_3gPpFHKiX_8OYI9_CjPJa4x1VU2encPP_FEHDU6m0lILEVVYkSV4LS7jfkJRe93GE51E8rQPUdR2IxcPc_P8mlE3Co-plLIktqAmW4_fyyMyLquDj-CjXfTpZ6RZs85rf3XH1qM-LOF8jhydDMKAhY8Iej4PCsT56C-kr26En3SqaA5BNgEftLIxhjQoFuZNCj8c7g5PuUztdmQ6UhjFA1-G392HnMx7rMYsfjeXxs2zaTeSjPh-z4JwyqkBTxZm6_rp37RpeQJFcGKzxWZNx8g)
* [Principios SOLID](https://enmilocalfunciona.io/principios-solid/)

* [ArjanCodes](https://www.youtube.com/watch?v=pTB30aXS77U&t=1s)

* [solid principles with python (broken link)](https://medium.com/@didemyaniktepe/solid-principles-with-python-97b5e7250ed7#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImZjYmQ3ZjQ4MWE4MjVkMTEzZTBkMDNkZDk0ZTYwYjY5ZmYxNjY1YTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2NTE5NjI5NzgsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMzA0ODgwMTUxNTE4Mzk4NTA5MyIsImVtYWlsIjoiZWNyZXNwb0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiMjE2Mjk2MDM1ODM0LWsxazZxZTA2MHMydHAyYTJqYW00bGpkY21zMDBzdHRnLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwibmFtZSI6IkVybmVzdG8gQ3Jlc3BvIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdpT19yRlhDM0VVWWRocmFLWjBHUmJNVlpRenhwSHRWQnl0MmI0MmU4WT1zOTYtYyIsImdpdmVuX25hbWUiOiJFcm5lc3RvIiwiZmFtaWx5X25hbWUiOiJDcmVzcG8iLCJpYXQiOjE2NTE5NjMyNzgsImV4cCI6MTY1MTk2Njg3OCwianRpIjoiNThhMzllZDhiMDNhZDM0ZDY1NDlhZDc2YzBmN2RkODY3NDNlZTgzMiJ9.db8I06It2VvYgbS6UswUsVGpbL3-OY8fFmQ367BXgF9p21W--y6OcTsKRTQp1yKVUZXbaUUoQYtIfoC00pnn9J7NHM1Fzixx1FIf8qeUm_4Yj4iPGzLwE4QapPbwJYdB1xXOLNGfQkfHb63U6ZwObrzJZrqHatNc7dwNNzpy0757d3BXvgrSNWbLXuNcxBVrdFwHqqtjJZfsyixaTAqYi4mzjg3ljpoxlYP-USeCIASUU6OJkMyCs__XjhC0ez2lWNDuPZwC3WML130U9GsHikAWR_Ue1iOIuQfC7_N2PE-GU0pYWCfIzzTvrhBoRFMhaN5i1koEOQ9w6c9ziCvH9A)

* [SOLID Coding in Python](https://towardsdatascience.com/solid-coding-in-python-1281392a6a94)

* [5 Principles to write SOLID Code](https://towardsdatascience.com/5-principles-to-write-solid-code-examples-in-python-9062272e6bdc)

* [The 5 (SOLID) Principles of Pyhon Readable Code (broken link)](https://towardsdev.com/the-5-solid-principles-of-pyhon-readable-code-67c5a3fe5693)

* [Designing to Patterns: A Pythonic Example](https://levelup.gitconnected.com/designing-to-patterns-a-pythonic-example-14bc8ce34e81)

* [Python Interface Segregation Principle](https://www.pythontutorial.net/python-oop/python-interface-segregation-principle/)

* [How to Write Clean Code (in Python) With SOLID Principles | Principle #4 (broken link)](https://medium.com/the-brainwave/how-to-write-clean-code-in-python-with-solid-principles-principle-4-2297c45d37e2)

* [The Interface Segregation Principle (ISP) Explained in Python (broken link)](https://medium.com/better-programming/the-interface-segregation-principle-isp-explained-in-python-46e173241642)

---
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)