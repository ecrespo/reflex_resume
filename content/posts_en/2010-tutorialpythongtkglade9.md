Title: Developing graphical applications with python+gtk+glade. Part 9. Matplotlib
Date: 2010-01-01 10:00
Category: Tutorial Python
Tags: Linux,Python,gtk,glade,matplotlib
lang: en
translation: true


Continuing with the articles on developing applications with python and gtk. Now I will join the articles related to [matplotlib](/blog/tags) and gtk.
I designed a dialog window with a plot in the center and 2 buttons: one to load the curve into the plot and the other to close the application.
The figure shows the interface design in glade.



![Tutorial 9 Glade 1](./images/tutorialpythongtkglade9-1.png)



The code that creates the application is the following:


```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Importar módulo gtk y matplotlib
import gtk
import matplotlib

matplotlib.use('GTK')
#Importar la clase figure, subplot, figurecanvasgtk, figurecanvas
from matplotlib.figure import Figure
from matplotlib.axes import Subplot
from matplotlib.backends.backend_gtk import FigureCanvasGTK, NavigationToolbar
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#Importar numpy
import numpy as np
#Definición de la clase
class App:
    def __init__(self):
        #Manejo del archivo glade por medio de gtkbuilder
        self.glade_file = "ej10.ui"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.glade_file)
        # cargar los widgets de la interfaz
        self.window = self.glade.get_object('dialog1')
        self.button1 = self.glade.get_object('button1')
        self.button2 = self.glade.get_object('button2')
        #Título de la ventana de dialogos
        self.window.set_title("Ventana de dialogo para demostrar uso de matplotlib")
        #Tamaño de la ventana de dialogos
        self.window.set_default_size(600, 400)
        #Asociación de los eventos con los widgets
        self.window.connect("destroy",self.on_dialog1_destroy)
        self.window.connect("close",self.on_dialog1_close)
        self.button1.connect ("clicked",self.on_button1_clicked)
        self.button2.connect ("clicked",self.on_button2_clicked)
        #Definición del widget que manejará la gráfica
        self.figura = Figure(figsize=(10, 8), dpi=100)
        self.ax = self.figura.add_subplot(111)
        self.ax.set_xlabel("Eje X")
        self.ax.set_ylabel("Eje Y")
        self.ax.set_title('Grafica')
        self.ax.grid(True)
        self.canvas = FigureCanvasGTK(self.figura)
        self.canvas.show()
        #Agregar la gráfica a la caja vertical
        self.vbox1 = self.glade.get_object("vbox1")
        self.vbox1.pack_start(self.canvas, True, True)
        #Mostrar la ventana
        self.window.show_all()
    
    def on_dialog1_destroy(self,*args):
        #Cerrar la ventana de dialogo
        gtk.main_quit()
    
    def on_button1_clicked(self,*args):
        #Carga la curva en la gráfica
        #Se oculta el canvas creado al inicio
        self.canvas.hide()
        #Generación de los valores X y Y
        self.x = np.arange(0,2*np.pi, .01)
        self.y = np.sin(self.x**2)*np.exp(-self.x)
        #Dibuja la curva
        self.ax.plot(self.x, self.y)
        #Se agrega la curva al canvas
        self.canvas = FigureCanvas(self.figura)
        #Se muestra el canvas
        self.canvas.show()
        #Se agrega el canvas a la caja vertical
        self.vbox1.pack_start(self.canvas, True, True)
        
    
    def on_button2_clicked(self,*args):
        #Cerrar la ventana de dialogo
        gtk.main_quit()
        
    def on_dialog1_close(self,*args):
        #Cerrar la ventana de dialogo
        gtk.main_quit()
    
    def main(self):
        #Ejecutar la aplicación gráfica
        gtk.main()
        


if __name__ == "__main__":
    #Creación de la instancia y ejecución del método main
    app = App()
    app.main()


```

The following figure shows the application running:


![Tutorial 9 Glade 2](./images/tutorialpythongtkglade9-2.png)


The following figure shows the application after pressing the apply button and loading the curve:


![Tutorial 9 Glade 2](./images/tutorialpythongtkglade9-3.png)


===

Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)