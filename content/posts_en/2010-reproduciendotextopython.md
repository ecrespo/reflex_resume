Title: Playing text aloud from python
Date: 2010-03-30 11:00
Category: Accesibilidad
Tags: Linux,Python,pypdf, pyttsx
lang: en
translation: true


There is a python module that lets you play text aloud directly from python code without having to run an external command; this module is called pyttsx.

To install it, run easy_install:
easy_install pyttsx

Now you can try the module:


```python

#!/usr/bin/env python
#Se importa el modulo
import pyttsx
#Se inicia el motor de voz
engine = pyttsx.init()
#Se selecciona el idioma a utilizar
engine.setProperty('voice', "spanish-latin-american")
#Se genera la voz a partir de un texto
engine.say('Esta es una prueba de reproduccion de texto')
engine.say('fin')
#Se reproduce la voz
engine.runAndWait()
```

This will play the content defined in the code. Next, the content of a pdf will be played, based on the previous post and this one:


```python

#!/usr/bin/env python
"""
Nombre: pdf2voz
Descripcion: Programa que reproduce el contenido de un pdf 
Autor: Ernesto Crespo
Correo: ernesto@crespo.org.ve
Licencia: GPL v3
Version de prueba para definir la construccion del reproductor
"""
import pyttsx
#Importar modulo de lectura de pypdf
from pyPdf import PdfFileReader
#Inicia el motor de reproduccion de texto a voz
engine = pyttsx.init()
#Se define el Idioma a reproducir
engine.setProperty('voice', "spanish-latin-american")
#Capturar el archivo pdf a leer
input1 = PdfFileReader(file("tut.pdf", "rb"))
#Capturar la cantidad de paginas que tiene el documento
paginas = input1.getNumPages()
titulo =input1.getDocumentInfo().title
#Captura la pagina inicial del pdf
pagina1 = input1.getPage(0)
#Captura el autor del documento pdf
autor =input1.getDocumentInfo().author
#Extrae el texto de la pagina inicial del documento pdf
texto = pagina1.extractText()
#Reproduccion de la informacion del pdf
engine.say("El titulo de libro es %s" %titulo)
engine.say("La cantidad de paginas del libro son %s" %paginas)
engine.say("El autor del documento es %s" %autor)
engine.say("El texto de la pagina inicial es")
engine.say(texto)
engine.runAndWait()


```

What remains is to work on a program that generalizes the playback of pdf documents, letting you define which pages to play, the volume and the language, among other options.


===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)