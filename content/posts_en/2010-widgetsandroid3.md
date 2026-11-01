Title: Widgets on Android with Python. Part 3 (spinner bar)
Date: 2010-07-15 10:00
Category: Tutorial Python en Android
Tags: Android, Python
lang: en
translation: true

Here I will explain how to use the spinner bar (a rotating progress indicator).
Basically the program is the same as in the previous post: it asks for the running time and then starts the spinner.

The code is shown below:


```python
#Se importa los módulos android y time
import android, time
#Se instancia el objeto Android
droid = android.Android()
#Se define un título y un mensaje
title = 'Spinner'
message = 'Este es un simple progreso spinner.'
 
#Se solicita se escriba el tiempo a ejecutar 
numero = droid.getInput("Escriba el tiempo","tiempo:")

#Se crea la barra de progreso spinner con el título y mensaje 
droid.dialogCreateSpinnerProgress(title, message)
 
#Se muestra la barra de progreso 
droid.dialogShow()

#Se genera un tiempo de espera dado el número de entrada 
time.sleep(int(numero[1]))
#Se cierra la barra de progreso spinner
droid.dialogDismiss()
```

The following figure shows the running time input.


![Spinner - Input](./images/bspinner1.png)

Below is the spinner progress bar.


![Spinner - Result](./images/bspinner2.png)

Finally, here is the QR code of the program.


![Code](./images/barra_spinner.png)


===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)