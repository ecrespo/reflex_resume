Title: Handling the phone's text messages from Linux (Android)
Date: 2010-12-16 09:00
Category: Tutorial Python en Android
Tags: Android, Linux, Python, SMS
lang: en
translation: true


Continuing with the scripts that run remotely on the phone, I will now show how to handle text messages: search for messages and delete them.

The idea is to find all the messages from a given phone number, show each message in the console and delete those messages.

The remote execution procedure explained in the [previous post](/blog/ejecucionremotaaandroid2) is followed.



The code is the following:

```python
#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
#Script que permite manejar los SMS del celular con android desde Linux.
#Autor: Ernesto Crespo
#Correo:ecrespo@gmail.com
#Licencia: GPLv3
#Versión:0.1


#Importando el módulo android,sys y re
import android


#Función de envio de mensajes
def Contactos():
    #Se crea la instancia de la clase Android
    droid = android.Android()
    #Se captura la cantidad de mensajes de texto )como en mi caso todos los 
    #mensajes han sido leídos coloco 0, si quiero los no leídos coloco 1.
    cantidad = droid.smsGetMessageCount(0)[1]
    #El número de celular a buscar
    numero = "0xxxyyyzzww"
    #Se recorren todos los mensajes.
    for i in range(cantidad):
        #Si el mensaje es del número dado se captura el identificador
        #del mensaje, se imprime un mensaje  en pantalla con la información:
        #read:Si mensaje ya fue leído
        #date: la fecha del mensaje
        #_id:identificador del mensaje.
        #address: número celular.
        #body:cuerpo del mensaje.
        #Toda está información se maneja desde un diccionario.
        #Si el celular no es de la persona buscada se continua con la 
        #siguiente iteración. 
        #A la función de borrar se le pasa el identificador del mensaje
        if droid.smsGetMessages(0)[1][i]["address"] == numero:
            identificador = droid.smsGetMessages(0)[1][i]["_id"]
            print "Borrando mensaje\t",i,droid.smsGetMessages(0)[1][i]["read"],droid.smsGetMessages(0)[1][i]["date"],droid.smsGetMessages(0)[1][i]["address"],droid.smsGetMessages(0)[1][i]["body"]
            droid.smsDeleteMessage(identificador)
        else:
            continue
if __name__ == "__main__":
    #Ejecución de la función
    Contactos()

```

The output of the program is the following:

 It returns a message saying the SMS has been deleted, the message number, whether it was read, the date, the phone number and the body of the message.

```
Borrando mensaje 296 1 1285030227398 0xxxyyyzzww Ah bueno... Yo les aviso.
Borrando mensaje 358 1 1283635867054 0xxxyyyzzww Ok. Ahi voy.
```



===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)