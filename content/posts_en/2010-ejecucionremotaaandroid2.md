Title: Remote execution of python scripts from Linux on an Android phone (phone connected over USB)
Date: 2010-12-15 10:00
Category: Tutorial de Python en Android
Tags: Android, Python, Debian, Linux
lang: en
translation: true

In the previous post I explained how to run python scripts remotely on an Android phone from Linux over wifi; now I will explain how to do it over a USB cable, which is actually simpler than the previous article.
I will build on what was explained in the [previous](/blog/ejecucionremotaaandroid) post and in the post about [sending text messages](/blog/enviaresmsconpythonandroid).

The first thing to do is connect the phone to the computer over USB, enable debugging mode and set the USB connection to Portal and Tools.

The SL4A server must be started. Menu->View->Interpreters->Menu->Start Server->Private.

Then check the notification messages to find out which port the server opens. In my case it was 58825.

From the Linux console, run the following commands:
Forward every request on port 9999 to port 58825.

```
./adb forward tcp:9999 tcp:58825

```

Export an environment variable.

```
export AP_PORT=9999
```

The program is the following:

```python
#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
#Script que permite enviar mensaje de texto a un celular android desde Linux.
#Autor: Ernesto Crespo
#Correo:ecrespo@gmail.com
#Licencia: GPLv3
#Versión:0.1

#Importando el módulo android,sys y re
import android,sys,re


#Función de envio de mensajes
def Enviomensaje():
    #Se averigua si se le pasa al script el número celular y el mensaje, y que el número sea válido para venezuela.
    if len(sys.argv) == 3:
        numero = sys.argv[1]
        mensaje = sys.argv[2]
    else:
        print "error enviando mensaje, se necesita pasar el número y mensaje"
        sys.exit
    if Validar(numero) == 0:
        print "Número invalido"
        sys.exit
    #Creando la instancia droid del objeto Android
    droid = android.Android()
    #Enviando el mensaje de texto
    droid.smsSend(numero,mensaje)
    #Se presenta un mensaje de notificación en el celular.
    droid.makeToast('Mensaje enviado')


#Función que válida si el número es de movilnet, digitel o movistar.
def Validar(numero):
    #Valida si los numeros tienen 11 digitos y que sean de los proveedores movilnet, digitel y movistar
    if len(numero) == 11 and ((re.search("041[2|4|6]\d\d\d\d\d\d\d",numero)) or (re.search("042[4|6]\d\d\d\d\d\d\d",numero))) :
        return 1
    else:
        return 0
#Ejecución del programa.
if __name__ == "__main__":
    Enviomensaje()
```

Run the script.
```
enviomensajes.py 0xxxyyyzzww  "2da prueba, avisame si te llega el sms"
```

===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)