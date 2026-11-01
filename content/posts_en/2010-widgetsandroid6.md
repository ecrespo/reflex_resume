Title: Widgets in Android with python. Part 6 (Buttons)
Date: 2010-07-16 11:00
Category: Tutorial Python en Android
Tags: Android, Python
lang: en
translation: true

Continuing with the [widgets of the ASE API for the python language](/blog/categories), we will write a script that shows 3 buttons and displays a message with the result of clicking a button.


The program code is the following:

```python
#Importando el módulo android.
import android

#Crear la instancia del objeto android
droid = android.Android()

#Título y mensaje del botón.
title = 'Alerta'
message = ('Esta alerta tiene 3 botones y' 'se espera que presione uno')
 
#Crear el widget de mensaje de alerta 
droid.dialogCreateAlert(title, message)
 
#Se definen los mensajes de los botones (si, no y cancelar).
droid.dialogSetPositiveButtonText('Si')
droid.dialogSetNegativeButtonText('No')
droid.dialogSetNeutralButtonText('Cancelar')

#Mostrar el mensaje
droid.dialogShow()

#Captura del resultado de darle clip a algún botón.
#el resultado es un diccionario.
response = droid.dialogGetResponse().result
 
#Se muestra un mensaje con el resultado de darle clip.
droid.makeToast('El resultado de la ejecucion del boton es: %s'    %response['which'])
```

The following figure shows the buttons widget.

![Buttons ](./images/botones2.png)

Next, the 3 figures for clicking each button are shown.
Message for the Yes button. 

![Button - Yes](./images/botones3.png)

Message for the Cancel button.

![Button - Cancel](./images/botones4.png)

Message for the No button.

![Button - No](./images/botones5.png)


Finally, the figure with the QR code of the script is shown.


![Code](./images/botones1.png)


===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)