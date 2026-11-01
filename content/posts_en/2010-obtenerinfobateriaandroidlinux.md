Title: Getting the battery status of an Android phone from Linux
Date: 2010-12-16 10:00
Category: Tutorial Python en Android
Tags: Android, Linux, Python, SMS
lang: en
translation: true

This post shows the functions that let you get information about the battery status of an Android phone from Linux.

To monitor the battery status, first call the function that starts monitoring, and then you can get the following information:

* Battery health
* Type of connection used to charge the battery
* Battery status
* Type of technology used in the battery
* Battery temperature
* Battery voltage

The program is the following:


```python
#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
#Script que muestra la información de la bateria del celular con Android.
#Autor: Ernesto Crespo
#Correo:ecrespo@gmail.com
#Licencia: GPLv3
#Versión:0.1


#Importando el módulo android
import android


def Bateria():
    
    droid = android.Android()
    #Se inicia el monitoreo de la bateria
    droid.batteryStartMonitoring()
    #Se captura la información de la salud de la bateria y se presenta un 
    #mensaje por la consola.
    bateriaSalud = droid.batteryGetHealth()[1]
    if bateriaSalud == 2:
        print "La bateria está bien"
    elif bateriaSalud == 1:
        print "Salud de la Bateria desconocido"
    elif bateriaSalud == 3:
        print "La bateria tiene sobrecarga"
    elif bateriaSalud == 4:
        print "La bateria está muerta"
    elif bateriaSalud == 5:
        print "La bateria tiene sobrevoltaje"
    else:
        print "falla desconocida"
    #Se captura la información del tipo de conexión que usa el celular
    #Se despliega la información por la consola.
    tipoConexion = droid.batteryGetPlugType()[1]
    if tipoConexion == 0:
        print "Cable desconectado"
    elif tipoConexion == 1:
        print "Fuente de alimentación: cargador AC"
    elif tipoConexion == 2:
        print "Fuente de alimentación: cable USB"
    else:
        print "Desconocido"
    #Se captura la información del estatus de la bateria y se presenta en la
    #consola.
    estatus = droid.batteryGetStatus()[1]
    if estatus == 2:
        print "Bateria cargandose"
    elif estatus == 3:
        print "Bateria descargandose"
    elif estatus == 4:
        print "Bateria no se está cargando"
    elif estatus == 5:
        print "Bateria full de carga"
    print "Tipo de tecnología de la bateria: ",droid.batteryGetTechnology()[1]
    print "Temperatura de la bateria: ",droid.batteryGetTemperature()[1]
    print "voltaje de la bateria: ",droid.batteryGetVoltage()[1]
    #Se detiene el monitoreo de la bateria
    droid.batteryStopMonitoring()
    
    
if __name__ == "__main__":
    #Ejecución de la función
    Bateria()
```

Running the program shows the following:

```
bateria.py
La bateria está bien
Fuente de alimentación: cable USB
Bateria cargandose
Tipo de tecnología de la bateria:  Li-ion
Temperatura de la bateria:  370
voltaje de la bateria:  4003
```

Regarding the temperature, I expect it to be 37 degrees, and the voltage to be measured in millivolts.




===

Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)