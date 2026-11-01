Title: Widgets on Android with Python. Part 2 (progress bar)
Date: 2010-07-14 10:00
Category: Tutorial Python en Android
Tags: Android, Python
lang: en
translation: true

Continuing the articles about creating Android widgets with Python.

This time we will create a program that asks for a number, and that number is then the running time of a progress bar.

The code is the following:


```python
#Importar módulo android y time 
import android,time
#instanciación de la clase android
droid = android.Android()
#Definir mensajes
titulo = "Horizontal"
mensaje = "Este es una barra de progreso horizontal"
 
#Se pide el tiempo de ejecución en seg  
numero = droid.getInput("Escriba el tiempo","tiempo:")
 
#Crear la barra horizontal con título, mensaje y el número 
droid.dialogCreateHorizontalProgress(titulo,mensaje,int(numero[1])) 
#Se muestra la barra de progreso
droid.dialogShow()
#ejecución del ciclo en 0.1 seg de la barra de progeso
for i in range(0,int(numero[1])):
   time.sleep(0.1)
   droid.dialogSetCurrentProgress(i)
 
#Se cierra la barra de progeso 
droid.dialogDismiss()
```

The program does not check whether the input is an integer; that is done by handling exceptions in Python.

The following image shows the data input.



![Progress bar - Input](./images/bprogreso1.png)


The next image is the progress bar running.


![Progress bar - Result](./images/bprogreso2.png)

Below is the QR code of the Python program.


![Code](./images/bprogreso.png)


===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)