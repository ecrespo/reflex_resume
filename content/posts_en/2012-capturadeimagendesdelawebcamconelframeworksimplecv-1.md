Title: Capturing an image from the webcam with the SimpleCV framework. Part 1.
Date: 2012-07-08 9:00
Category: 
Tags: Canaima,Debian,Linux,Python,Ubuntu,SimpleCV
lang: en
translation: true

`SimpleCV` is a framework for building Computer Vision applications; it is a set of libraries that let you capture images with cameras (webcams) or IP cameras in order to obtain information from those images.

The SimpleCV project page can be visited at this [link](http://www.simplecv.org/).

To install `SimpleCV` the python installation tools `easy_install` or `pip` will be used.
```
pip install simplecv
```
The example developed is a simple application that captures the image from the webcam, shows it on screen for a few seconds and saves it to a file in png format.

The code is the following:
```python
#!/usr/bin/env python

#Importar los modulos Camera, Display e Image.

from SimpleCV import Camera, Display, Image

#Se importa sleep para darle unos segundos a la 

#aplicacion a que muestra la captura en pantalla.

from time import sleep

#Se crea una instancia de Camera.

#Se inicializa la camara

camara = Camera()

#Se crea una instancia de Display

#se inicializa display

pantalla = Display()

#Se captura una imagen usando la camara

imagen = camara.getImage()

#Muestra la imagen en pantalla

imagen.save(pantalla)

#Se salva la imagen en un archivo

imagen.save("captura.png")

sleep(2)
```
When the program is run, a window shows the capture made by the webcam and saves it to a file.  

The captured image is shown below:  

![](./images/capturadeimagendesdelawebcamconelframeworksimplecv1-1.png) 


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)