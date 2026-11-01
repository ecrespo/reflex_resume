Title: python+qt tutorial. Part 2
Date: 2010-01-25 11:00
Category: Tutorial Python
Tags: Linux,Python,qt
lang: en
translation: true


This tutorial explains how to set an icon on the window and create a button to quit the application, with all the code written in an object-oriented style.



```python
#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#Importar módulo sys
import sys 
#De PyQt4 importar QtGui y QtCore
from PyQt4 import QtGui, QtCore 
#Se crea la clase QuitButton que hereda de la clase QWidget.
class QuitButton(QtGui.QWidget):
    def __init__(self, parent=None):
       QtGui.QWidget.__init__(self, parent)
       #Se define el tamaño de la ventana
       self.setGeometry(400, 400, 250, 150)
        #Se le coloca un título a la ventana y se asocia un icono. 
       self.setWindowTitle('Prueba de boton para salir') 
       self.setWindowIcon(QtGui.QIcon('./icono.png'))   
       #Se crea el botón salir con su tamaño        
       quit = QtGui.QPushButton('Salir', self)        
       quit.setGeometry(10, 10, 60, 35)        
       #Se asocia la señal del botón con quit 
       self.connect(quit, QtCore.SIGNAL('clicked()'),QtGui.qApp, QtCore.SLOT('quit()'))   

#Se ejecuta el programa principal
if __name__ == "__main__":    
   #Se instancia la clase QApplication    
   app = QtGui.QApplication(sys.argv)    
   #Se instancia el objeto QuitButton    
   qb = QuitButton()    
   #Se muestra la aplicación    
   qb.show()    
   #Se sale de la aplicación    
   sys.exit(app.exec_())


```


The following figure shows the application running.


![Tutorial 2 pyqt 1](./images/tutorialpyqt2-1.png)


===

Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)