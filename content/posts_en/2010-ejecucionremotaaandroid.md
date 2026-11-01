Title: Remote execution of python scripts from Linux on an Android phone
Date: 2010-10-23 10:00
Category: Tutorial de Python en Android
Tags: Android, Python, Debian, Linux
lang: en
translation: true

There is a way to run scripts, whether python, perl, ruby, bash, etc., remotely (from Linux) on an Android phone.

By installing SL4A and python you can start an SL4A service that listens on a specific port of the Android phone. There is a public or a private option: for the first, the phone has to be connected to a wifi network where it brings up the service on a specific port; for a private connection the phone must be connected through a USB port with USB debugging enabled and the phone in Portal and Tools mode.

This post is based on the SL4A remote control article found [here](http://code.google.com/p/android-scripting/wiki/RemoteControl) .

Here I will explain the public remote connection. First, the phone has to be connected to a wifi network.

On the machine I am using, I assign the IP 192.168.10.19.

Then run SL4A on the phone, press menu, select view, then interpreters, then menu again, select start server. At this point you are asked to choose between a public or private server; select the first one.

The phone puts a message in the Android notification area saying the server has started; expanding it, it says an SL4A server was started at IP 192.168.10.19 on port 52834.

Next, the Android sdk will be used on Linux by running adb.
Start the adb server.

```
./adb start-server
* daemon not running. starting it now on port 5037 *
* daemon started successfully *
```

Note that the server comes up on port 5037.


Now the ports of the adb service are forwarded.

```
./adb forward tcp:9999 tcp:52834

```

Here port 9999 is forwarded to the port the phone is listening on, which is 52834 in this case.

Next, set the environment variables with the IP and port of the Android phone that is running the SL4A server.

```
export AP_PORT=52834
export AP_HOST=192.168.10.19
```

Make sure the python2.6 path includes the python module for android. You can download it at this [link (broken link)](http://android-scripting.googlecode.com/hg/python/ase/android.py).

Below is a python script that asks you to type your user name on the phone and shows it on Linux and on the phone:

```python
#Importar módulo android
import android
#Se crea el objeto droid de la clase Android con la IP y puerto del servicio iniciado en el celular.
droid = android.Android(('192.168.10.19', 52834))
#Se solicita al usuario que escriba su nombre
texto = droid.getInput("Escriba su nombre","Nombre:")
#Se imprime el nombre del usuario en la consola de Linux
print "El nombre escrito en el celular es: %s" %texto[1]
#Se presenta un saludo al usuario en el celular
droid.makeToast('Hola %s' %texto[1])
```

To run the program, place the script prueba-remota.py in the same directory as the SL4A android.py module, or put the module in the python2.6 path.
Run it with python2.6:

```
$ python2.6 prueba-remota.py 

```

El nombre escrito en el celular es: ernesto


===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)