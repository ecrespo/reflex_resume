Title: Application that shows the phone's coordinates in google maps on the desktop
Date: 2011-01-06 09:00
Category: Tutorial Python
Tags: Linux,Python,gtk,glade,webkit, Google maps, Android
lang: en
translation: true

This article builds on 2 previous articles: the first about a basic web browser with python+gtk+webkit and the second about capturing the phone's location with Android.

The idea is to capture the phone's GPS information and display it in a gtk application, using webkit to show the geographic location through google maps.

The glade interface is shown below.



![Glade webkit - Browser](./images/tutorialpythongtkglade12-1.png)


It is really the same browser application; the only difference is that the text entry and the "go" button were removed.

The application code is shown below:


```python
#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
"""
Nombre:Geolocalizacion
Descripción: Programa que captura la localización del GPS del Celular y lo
    muestra en google maps en el escritorio Linux.
Versión:0.1
Licencia:GPLv3
Autor: Ernesto Crespo
correo: ecrespo@gmail.com
"""
#Import gtk and webkit


import gtk
import webkit
#Importando el módulo android
import android
from time import sleep



#class App
class App:
    def __init__(self):
        #Constructor
        #Se asocia el archivo glade al Builder
        self.glade_file = "geolocalizcion.glade"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.glade_file)
        #Se asocia la ventana geo
        self.window = self.glade.get_object('geo')
        #Se asocia el botón salir
        self.exit = self.glade.get_object('salir')
        #Se asocia la ventana deslizante
        self.scrolledwindow1 = self.glade.get_object('scrolledwindow1')
        #
        #Se conecta el evento destruir
        self.window.connect("destroy",self.on_geo_destroy)
        #Se asocia el evento del botón salir
        self.exit.connect('clicked', self.on_salir_clicked)
        #Se abre la página de google maps
        #Se instancia la clase webview
        self.webview = webkit.WebView()
        #Se agrega a la ventana deslizante
        self.scrolledwindow1.add(self.webview)
        #Se captura la localización
        tupla = localizacion()
        #Se abre el url de google maps pasandole la longitud y latitud
        self.__go("http://maps.google.com/maps?q=%s,%s" %tupla)

        #Se muestra la ventana principal de la aplicación
        self.window.show_all()


    def __go(self,url):
        #Se abre el url
        self.webview.open(url)


    def on_geo_destroy(self,*args):
        #Se cierra la apliación
        gtk.main_quit()

    def on_salir_clicked(self,*args):
     #Se cierra la aplicación
        gtk.main_quit()


    def main(self):
        #Se inicia la aplicación
        gtk.main()


def localizacion():

        #Se crea la instancia de la clase Android
        droid = android.Android()
        #Se inicia la localizacion
        droid.startLocating()
        #Se espera 15 segundos
        sleep(15)
        #Se presenta en la consola la información de la localización
        #Se maneja la información de un diccionario.
        latitud = droid.readLocation().result["network"]["latitude"]
        longitud = droid.readLocation().result["network"]["longitude"]
        #Se detiene la localización
        droid.stopLocating()
        #Se retorna la latitud y longitud capturada por medio del GPS del celular.
        return (latitud,longitud)


if __name__ == '__main__':
    app = App()
    app.main()

```

The figure of the application running, showing the map and the position returned by the phone's GPS.

![Browser ](./images/tutorialpythongtkglade12-2.png)



===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
