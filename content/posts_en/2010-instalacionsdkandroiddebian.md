Title: Installing the Android SDK on Linux
Date: 2010-05-27 10:00
Category: Tutorial Linux
Tags: Linux, Android, Debian
lang: en
translation: true


To access an Android phone from Debian, the first thing to do is download the Android SDK from the following [link](http://developer.android.com/sdk/index.html).


Then extract android-sdk_r06-linux_86.tgz.

```
tar -xvzf android-sdk_r06-linux_86.tgz
```

Then change to the android-sdk_r06-linux_86 directory and then to the tools directory.

```
cd android-sdk_r06-linux_86/tools
```

Run android:

```
./android
```


The following window will appear. Select the packages to install.

![sdk 1](./images/sdkandroid1.png)

Then accept the license of all the packages and the installation process starts, as the figure shows.

![sdk 2](./images/sdkandroid2.png)

When the installation of the SDK APIs and libraries finishes, select Virtual Devices.

![sdk 3](./images/sdkandroid3.png)

Create one as the figure shows.

![sdk 4](./images/sdkandroid4.png)

When you click Create, a window will show the results of creating the virtual device; after clicking OK the device will appear in the list of devices.

![sdk 5](./images/sdkandroid5.png)

When you click the Start button, a window opens showing options to launch the virtual device.

![sdk 6](./images/sdkandroid6.png)


When you click the Launch button, a virtualized Android phone will start, as the following figure shows.

![sdk 7](./images/sdkandroid7.png)


The next post will explain the use of adb, which allows access to the real phone.




===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)