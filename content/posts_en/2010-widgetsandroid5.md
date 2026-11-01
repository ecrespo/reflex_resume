Title: Widgets on Android with python. Part 5 (Button)
Date: 2010-07-16 10:00
Category: Tutorial Python en Android
Tags: Android, Python
lang: en
translation: true

This article will explain how to create a message with a continue button; after pressing the button, a message with the result of the button is shown.

The application code is the following:

```python
#Importar módulo android
import android
#Se crea la instancia del objeto Android
droid = android.Android()

#título y mensaje del botón 
title = 'Interfaz de usuario'
message = 'Esta es una prueba'

#Se crea la alerta con el título y mensaje 
droid.dialogCreateAlert(title, message)

#Se define el botón 
droid.dialogSetPositiveButtonText('Continuar')
 
#Se muestra el mensaje 
droid.dialogShow()

#Se captura el resultado del resultado de darle clip al botón
#El resultado es un diccionario
response = droid.dialogGetResponse().result
 
#Se muestra el resultado del clip del botón 
droid.makeToast('El resultado de la ejecucion del boton es: %s' 
                                %response['which'])
```

The button is shown below.

![Button ](./images/mensaje_alerta1.png)

The following figure shows the message with the result of clicking the button.

![Button - Result](./images/mensaje_alerta2.png)

To finish, here is the image of the program's qr code.

![Code](./images/mensaje_alerta3.png)


===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)