Title: S.O.L.I.D. Principles - 5. Dependency inversion principle (DIP) 
Date:  2022-05-14 14:00
Category: Tutorial Python
Tags: python,solid
lang: en
translation: true
Slug: python_solid5
Authors: Ernesto Crespo
Summary: Fifth and last article on the SOLID principles, in this case the Dependency inversion principle.

In software engineering there is the [S.O.L.I.D](https://es.wikipedia.org/wiki/SOLID) principle. The SOLID principles are guidelines that can be applied in software development to eliminate bad designs, which would otherwise force the programmer to refactor until the code is readable and extensible. 

Its principles are:

* Single responsability principle.
* Open/closed principle.
* Liskov substitution principle.
* Interface segregation principle.
* Dependency inversion principle.


Below is a video by [ArjanCodes](https://www.youtube.com/watch?v=pTB30aXS77U&t=1s) that explains the S.O.L.I.D principles with python code:

<iframe width="560" height="315" src="https://www.youtube.com/embed/pTB30aXS77U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

The previous articles:
* [Single responsibility principle](/blog/python_solid1).
* [Open/closed principle](/blog/python_solid2).
* [Liskov substitution principle](/blog/python_solid3).
* [Interface segregation principle](/blog/python_solid4).

The [Dependency inversion principle](https://es.wikipedia.org/wiki/Principio_de_inversi%C3%B3n_de_la_dependencia) is a specific way of decoupling software modules. By following the principle, the conventional dependency relationships established from high-level policy-setting modules to low-level dependency modules are inverted, which makes the high-level modules independent of the implementation details of the low-level module. The principle states: 
 
1. High-level modules should not depend on low-level modules. Both should depend on abstractions (e.g., interfaces).
2. Abstractions should not depend on details. Details (concrete implementations) should depend on abstractions.

The dependency should be on abstractions, not on concretions. High-level modules must not depend on low-level modules. Both low-level and high-level classes should depend on the same abstractions. Abstractions should not depend on details. Details must depend on abstractions.



1. Here is the code from the previous article on the Interface segregation principle, with the solution using composition.

In this case, passing an object as an argument of a method already violates this principle.

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

### Solution
To comply with the dependency inversion principle, an abstract class is created that handles whether authentication is verified, together with the AuthSMS class. In the respective payment processing classes that need to be verified by SMS, instead of passing the object as an argument, the abstract class is passed. 

Here is the code: 

```python

from abc import ABC, abstractmethod

# La clase Order 
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

# Clase abstracta authorizer con método que devuelve si está autorizado o no. 
class Authorizer(ABC):
    @abstractmethod
    def is_authorized(self) ->bool:
        pass


# Clase abstracta de procesamiento de pago
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self,order):
        pass 

# Clase SMSAutho que hereda de la clase abstracta authorizer
class SMSAuth(Authorizer):
    authorized = False
    
    def verify_code(self,code):
        print(f"Verifying code {code}")
        self.authorized = True
        
    def is_authorized(self) -> bool:
        return self.authorized

# clase pago por tarjeta de debito que recibe en el init authorizer que es la clase abstracta.
class DebitPaymentProcessor(PaymentProcessor):
    
    def __init__(self,security_code, authorizer: Authorizer):

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

# La clase de procesamiento de TC se mantiene igual.
class CreditPaymentProcessor(PaymentProcessor):
    
    def __init__(self,security_code):
        self.security_code = security_code
        
    
    def pay(self,order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


# clase dde procesamiento de pago por paypal
# Se le pasa como argumento la clase abstracta.
class PaypalPaymentProcessor(PaymentProcessor):
    
    def __init__(self,email_address,authorizer:Authorizer):
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

The output is the following: 

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

What was achieved is hiding the implementation of the composition that is passed as an argument in the payment processors that have to validate via SMS.

In the next article 


References: 

* [SOLID Principles in Python](https://softwarecrafters.io/python/principios-solid-python)
* [The SOLID principles illustrated in simple Python examples](https://blog.damavis.com/los-principios-solid-ilustrados-en-ejemplos-sencillos-de-python/)
* [SOLID Principles explained in Python with examples.](https://ichi.pro/es/principios-solid-explicados-en-python-con-ejemplos-56291217871103)
* [The S.O.L.I.D Principles in Python (broken link)](https://medium.com/geekculture/the-s-o-l-i-d-principles-in-python-a041c5aa9969#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ2M2RiZTczYWFkODhjODU0ZGUwZDhkNmMwMTRjMzZkYzI1YzQyOTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2NDY5NjE2MDYsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMzA0ODgwMTUxNTE4Mzk4NTA5MyIsImVtYWlsIjoiZWNyZXNwb0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiMjE2Mjk2MDM1ODM0LWsxazZxZTA2MHMydHAyYTJqYW00bGpkY21zMDBzdHRnLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwibmFtZSI6IkVybmVzdG8gQ3Jlc3BvIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdpNzZJNGhTTXQ3U1hYbzZjdHdaNDloeDlKbTF3cU93UXZiTU0zbWtHMD1zOTYtYyIsImdpdmVuX25hbWUiOiJFcm5lc3RvIiwiZmFtaWx5X25hbWUiOiJDcmVzcG8iLCJpYXQiOjE2NDY5NjE5MDYsImV4cCI6MTY0Njk2NTUwNiwianRpIjoiNWM2ZWFkNjRjNjcyOGYxY2VhNmJhNjhkNGYzYTYyZTI3MzUxZTFhZCJ9.jMgz-2c2M8jmF-pepfaLohkEc75VeswUa7S1N6h6VgS7DOHw4rUVBjza_7VYEa_3gPpFHKiX_8OYI9_CjPJa4x1VU2encPP_FEHDU6m0lILEVVYkSV4LS7jfkJRe93GE51E8rQPUdR2IxcPc_P8mlE3Co-plLIktqAmW4_fyyMyLquDj-CjXfTpZ6RZs85rf3XH1qM-LOF8jhydDMKAhY8Iej4PCsT56C-kr26En3SqaA5BNgEftLIxhjQoFuZNCj8c7g5PuUztdmQ6UhjFA1-G392HnMx7rMYsfjeXxs2zaTeSjPh-z4JwyqkBTxZm6_rp37RpeQJFcGKzxWZNx8g)
* [SOLID Principles](https://enmilocalfunciona.io/principios-solid/)

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
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)