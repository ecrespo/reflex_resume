Title: Creating a QR Code from Python
Date: 2011-07-20 09:00
Category: Tutorial de Python y PyQt
Tags: Código QR, Python, PyQt
lang: en
translation: true

In the articles I have written about python scripts for Android I have always included an image that looks like a barcode but in 2 dimensions; this code is called a QR Code (Quick Response Barcode), and you can read more about it on [wikipedia](http://es.wikipedia.org/wiki/Codigo_QR).

In the article on how to share scripts on Android there is a [link](/blog/compartirscriptandroid) to a page that generates the QR code from a given piece of information.

The idea is to create the code from Linux, and the program that does it is called qrencode.

To install it on Debian, simply run aptitude:

```
aptitude install qrencode
```

The command to generate a file with the QR code image is shown below:

```
qrencode -o output.png 'Hola mundo!'
```

This example generates a png file called output with the QR code for "Hola Mundo!"

There is also a python module that can generate the code directly; this package is called python-qrencode on Debian, and to install it you run aptitude:

```
aptitude install python-qrencode

```

The python-qrencode project page is on github at this [link](https://github.com/Arachnid/pyqrencode). 

From this module the encode function will be used; you pass it a string as data and it returns a tuple with 3 values: the version, the image size and the image.

This image is an Image object, and it can be saved to a file.

The example code for using python-qrencode is shown below:

```python 
#!/usr/bin/env python


#modulo qrencode
from qrencode import encode

#El texto a convertir en codigo QR
texto = """Esta es uan prueba de generacion de codigo QR\n
desde python usando el modulo qrencode."""

#Se crea el codigo QR del texto,la funcion encode 
#genera una tupla donde el ultimo elemento es un
#objeto Imagen.

imagen = encode(texto)[2]

#Se salva la imagen en el archivo
#archivoprueba.png
imagen.save("/home/ernesto/archivoprueba.png")
```






===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
