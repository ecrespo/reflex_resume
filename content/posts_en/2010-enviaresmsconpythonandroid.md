Title: Sending text messages from Android with python
Date: 2010-06-27 15:00
Category: Tutorial Python
Tags: Android, Linux, Python, SMS
lang: en
translation: true


Continuing with the ASE API reference for Android, this article explains how to send a text message from python on an Android phone.

THE API for sending text messages is the following:

```
smsSend(String destinationAddress: typically a phone number,String text) Sends an SMS.
```

Here is the code for sending the SMS:



```python

#Importando el módulo android y el módulo time
import android, time

#Creando la instancia droid del objeto Android
droid = android.Android()

#Asignando el número de teléfono y mensaje
telefono ="0xxxyyyyyyy"
mensaje = "Esta es una prueba de envio de sms a la hora %s" %time.ctime()

#Enviar mensaje a la pantalla de android con la info del número y mensaje
droid.makeToast("enviando mensaje a %s, con el siguiente contenido: %s" %(telefono,mensaje))

#Enviando el mensaje de texto
droid.smsSend(telefono,mensaje)

```

The message reached the phone of the assigned number without problems.


===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)