Title: Installing python on Android
Date: 2010-06-06 13:00
Category: Tutorial Python
Tags: Linux, Android, Debian, Python
lang: en
translation: true



This article explains how to install python on Android from the emulator so that I can show the screenshots; the procedure is the same for installing python from the phone.

The first thing you need to do is start the emulator, as explained in the article on [installing the Android SDK](/blog/instalacionsdkandroiddebian).


When you run adb devices you will find a virtual device running.


```
ernesto@zvezda:~/android-sdk-linux_86/tools$ ./adb devices List of devices attached emulator-5554 device
```


Then download the ASE program from the [following link (broken link)](http://code.google.com/p/android-scripting/downloads/detail?name=ase_r24.apk).

```
ernesto@zvezda:~/android-sdk-linux_86/tools$ ./adb install ../../Descargas/ase_r22.apk 868 KB/s (217639 bytes in 0.244s) pkg: /data/local/tmp/ase_r22.apk Success
```

This indicates that the ASE program was installed without problems.


The following figure shows the emulator's home screen with ASE installed.


![Python on Android 1](./images/pythonandroid1.png)

When you click the ASE icon, a screen appears asking you to add scripts or interpreters by pressing the menu button, as the following figure shows:

![Python on Android 2](./images/pythonandroid2.png)


When you press menu, several options appear: Add, View, Preferences, Help, Update. Next figure:

![Python on Android 3](./images/pythonandroid3.png)

When you click View, a menu appears with several viewing options; in this case we want to view interpreters. Next figure:

![Python on Android 4](./images/pythonandroid4.png)

When you click Interpreters, only the Shell interpreter will appear, along with the options Add, Start server, Preferences and Help. In this case we are going to add a new interpreter.

![Python on Android 5](./images/pythonandroid5.png)

When you click add, a list of interpreters appears, from which we will install python. Next figure:

![Python on Android 6](./images/pythonandroid6.png)

When you select Python 2.6.2, the installation of the interpreter and some scripts starts, as the following 2 figures show:

![Python on Android 7](./images/pythonandroid7.png)


![Python on Android 8](./images/pythonandroid8.png)

Now Python appears next to Shell in the list of interpreters, as the following figure shows:

![Python on Android 9](./images/pythonandroid9.png)

To test that everything is working, select the interpreter and it will run, as the figure shows:

![Python on Android 10](./images/pythonandroid10.png)

Finally, the example python scripts for working with Android are listed:

![Python on Android 11](./images/pythonandroid11.png)


In upcoming articles I will explain how to use the scripts to build an Android application step by step.


===

Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)