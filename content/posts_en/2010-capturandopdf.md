Title: Capturing the content of a pdf from python
Date: 2010-03-29 11:00
Category: Accesibilidad
Tags: Linux,Python,pypdf
lang: en
translation: true


For some time I had known about the possibility of extracting information from a pdf; the final goal is to take this information and play it back with espeak.

The following example shows the use of the pypdf module.

```python

#Importar modulo de lectura de pypdf
from pyPdf import PdfFileReader

#Capturar el archivo pdf a leer
input1 = PdfFileReader(file("tut.pdf", "rb"))

#Capturar la cantidad de paginas que tiene el documento
paginas = input1.getNumPages()
#Capturar el titulo del pdf
titulo =input1.getDocumentInfo().title
#Captura la pagina inicial del pdf
pagina1 = input1.getPage(0)
#Captura el autor del documento pdf
autor =input1.getDocumentInfo().author
#Extrae el texto de la pagina inicial del documento pdf
texto = pagina1.extractText()
print "El libro se llama : %s" %titulo
print "El autor es: %s" %autor
print "La cantidad de paginas del libro es: %s " %paginas
print "El contenido de la pagina inicial es:"
print texto

```

The result of this script is the following:
```
El libro se llama : Guía de aprendizaje de Python
El autor es: Guido van Rossum, Fred L. Drake, Jr., editor
La cantidad de paginas del libro es: 77 
El contenido de la pagina inicial es:
GuíadeaprendizajedePythonRelease2.0GuidovanRossumFredL.Drake,Jr.,editor16deoctubrede2000BeOpenPythonLabsCorreoelectrónico:python-docs@python.org
```

In the next article I will explain how to use the audio converter on the information captured from the pdf.

===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)