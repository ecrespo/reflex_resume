Title: Getting the screen resolution from Python
Date: 2015-08-27 9:00
Category:
Tags: Canaima,Debian,Python,Ubuntu
lang: en
translation: true

This article is based on an [article](http://www.blog.pythonlibrary.org/2015/08/18/getting-your-screen-resolution-with-python/) in English on the subject.

From the command line on Linux you can run the `xrandr` command as shown below:
```
ernesto@grievous:~$ xrandr | grep '*'
   1366x768      60.00*+
```
The resolution is 1366x768.

The script is shown below:
```python
#!/usr/bin/env python

#Se importa el modulo subprocess
import subprocess

#Se define un par de variables con los comandos a pasar:
cmd = ['xrandr']
cmd2 = ['grep', '*']

#Se ejecuta el comando xrandr y luego se abre una tuberia.
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

#Se ejecuta el segundo comando
p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)

#Se cierra la salida estandar.
p.stdout.close()


#Obteccion de la resolucion
resolution_string, junk = p2.communicate()
resolution = resolution_string.split()[0]
width, height = resolution.split('x')
print width,height
```

Running the script gives:
```python
./screencatch.py
1366 768
```
Get the resolution with gtk using the following script:
```python
#!/usr/bin/env python

#Se importa gtk
import gtk

#Se captura el ancho y alto
width = gtk.gdk.screen_width()
height = gtk.gdk.screen_height()

#Se muestra en la consola el resultado
print width,height
```
Running the script gives:
```python
 ./screencatch2.py
1366 768
```
Get the resolution with `PySide/PyQT` using the following script:
```python
#!/usr/bin/env python
#Importar QtGui de PySide
#para solo PyQt se cambia a
#from PyQt4 import QtGui

from PySide import QtGui

#Se crea la instancia de la aplicacion
app = QtGui.QApplication([])
#Se captura la resolucion y se muestra  en la consola
screen_resolution = app.desktop().screenGeometry()
width, height = screen_resolution.width(), screen_resolution.height()

print width,height
```
The result of running the script is:
```python
./screencatch3.py
1366 768
```

The mentioned article shows how to get the information with `wxPython`, and a link in the article shows how to get it from windows and from MacOS.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
