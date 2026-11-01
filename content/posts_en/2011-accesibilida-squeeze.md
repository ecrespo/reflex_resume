Title: Accessibility in squeeze
Date: 2011-02-06 09:00
Category: Tutorial Linux
Tags: Linux, Debian, Accesibilidad
lang: en
translation: true

Since the development of squeeze began, it was clear to me that improvements to accessibility in the Debian installer were coming. With Lenny you could use a USB Braille reader without problems during the installation process, in both text and graphical mode.


With the squeeze version, the installation document even explains how to enable accessibility during this process; the information is at this [link (broken link)](http://www.debian.org/releases/stable/i386/ch05s02.html.es).

Below is a brief summary of the guide:

1. USB Braille devices: These are detected automatically during the installer boot process thanks to the brltty application; for more information about this application you can visit the [link (broken link)](http://www.mielke.cc/brltty/doc/drivers/).
2. Serial Braille devices: For these devices you need to pass some parameters to the kernel when the installer boots. The syntax is brltty=driver, port,table. The default port is ttyS0; you can find the list of drivers [here](http://www.mielke.cc/brltty/doc/Manual-BRLTTY/English/BRLTTY-11.html) and the list of table codes [here](http://www.mielke.cc/brltty/doc/Manual-BRLTTY/English/BRLTTY-6.html).
3. Speech synthesizer devices: This is the improvement squeeze brings, since voices can now be played during the Debian installation process, only for the graphical installer; you need to pass some boot parameters to the installation CD with the following syntax: speakup.synth=driver. The voices are played through the speakup application, but you need to pass it the driver type so that it can play the voices properly. At this [link (broken link)](http://www.linux-speakup.org/spkguide.txt) you will find the guide on how to use speakup and the list of drivers.
4. High contrast themes: For people with low vision a high contrast theme can be used; to enable it at boot, add the following parameter theme=dark. This option already existed in Lenny in the graphical interface of the installer.

Additionally, the Debian team has created a group dedicated to accessibility in the customization of the Debian CD; for more information visit the Debian Pure Blends site dedicated to [accessibility](http://www.debian.org/devel/debian-accessibility/).




===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
