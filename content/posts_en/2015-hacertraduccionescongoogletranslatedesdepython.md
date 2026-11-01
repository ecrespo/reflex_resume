Title: Translating with google translate from python
Date: 2015-10-19 9:00
Category: Tutorial Python
Tags: Canaima,Debian,Python,Ubuntu,Google Translate
lang: en
translation: true

Google Translate has an API that lets you use the translator from a program; for Python there is [goslate](https://pypi.python.org/pypi/goslate).


To install it, use `pip`:
```python
pip install goslate
```

Run python. And try Hello World from English into other languages:

Import the module:
```python
>>> import goslate
```
Create the object instance:
```python
>>> gs = goslate.Goslate()
```

Translate hello world into German, Spanish and Italian:
```python
>>> print gs.translate('hello world', 'de')
Hallo Welt
>>> print gs.translate('hello world', 'es')
Hola mundo
>>> print gs.translate('hello world', 'it')
Ciao mondo
```
The application's `pypi` page shows other features of the application, such as detecting the language, searches, among others.


##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
