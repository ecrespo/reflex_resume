Title: Remote control of the music player in Debian from Android
Date: 2011-04-03 09:00
Category: Demostración Aplicación para Android
Tags: Android, Linux, Debian, gnome
lang: en
translation: true

Looking for applications to remotely control music players on Linux from Android, I came across [tesla](http://sourceforge.net/apps/trac/android-tesla/).

To install tesla on the phone you can download the apk file from [andAppStore (broken link)](http://andappstore.com/AndroidApplications/apps/186356).
On your Debian machine you need to install openssh and libpam-ck-connector.
aptitude install libpam-ck-connector openssh-server openssh-client openssh-blacklist-extra openssh-blacklist

You need to restart ssh.
```
/etc/init.d/ssh restart.
```

The phone must be connected to the same wifi network as your computer.

When you start tesla on the phone it will ask for your computer's IP address, the user you log in with and its password, as the figure shows.

![App tesla - setup](./images/tesla1.png)

You can select other players that work on Linux before connecting the application.

![App tesla - control](./images/tesla2.png)

The following image shows tesla running on the phone and then the Rhythmbox player.

![Rhythmbox music player](./images/reproductormusica.png)


===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
