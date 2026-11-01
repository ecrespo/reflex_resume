Title: Capture the phone's location (Android) from Linux.
Date: 2010-12-21 10:00
Category: Tutorial Python en Android
Tags: Android, Linux, Python, SMS
lang: en
translation: true

It took me a few days to update my Milestone to Froyo, thanks to the androidve people, who released a Venezuelan version of Froyo called [FroyoVE](http://androidve.blogspot.com/2010/12/navidad-antes-del-24-froyove-152-la.html).

Today I will write about how to get the information handled by the GPS from Linux.

The first thing to do is start the location, capture the information, and then stop the location.

Here is the program code:



```python
#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
#Script que permite capturar la localización GPS del celular (ANDROID) desde Linux.
#Autor: Ernesto Crespo
#Correo:ecrespo@gmail.com
#Licencia: GPLv3
#Versión:0.1


#Importando el módulo android
import android
from time import sleep




#Función de envio de mensajes
def localizacion():
    #Se crea la instancia de la clase Android
    droid = android.Android()
    #Se inicia la localizacion
    droid.startLocating()
    #Se espera 15 segunfos
    sleep(15)
    #Se presenta en la consola la información de la localización
    #Se maneja la información de un diccionario.
    print "Altitud: ",droid.readLocation().result["network"]["altitude"]
    print "Proveedor: ",droid.readLocation().result["network"]["provider"]
    print "Latitud: ",droid.readLocation().result["network"]["latitude"]
    print "Longitud: ",droid.readLocation().result["network"]["longitude"]
    print "Tiempo: ",droid.readLocation().result["network"]["time"]
    print "Velocidad: ",droid.readLocation().result["network"]["speed"]
    print "Precisión: ",droid.readLocation().result["network"]["accuracy"]
    #Se detiene la localización
    droid.stopLocating()


#Ejecución del programa principal.
if __name__ == "__main__":
    #Ejecución de la función
    localizacion()
```

Running it from the console shows the following:


```
localizacion.py

Altitud:  0
Proveedor:  network
Latitud:  8.65770805
Longitud:  -71.11786675
Tiempo:  1292944124223
Velocidad:  0
Precisión:  65
```

Using Google Maps I checked that the latitude and longitude returned by the phone's GPS are near Troncal 7 in Mérida.




===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)