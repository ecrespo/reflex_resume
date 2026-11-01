Title: Installing Debian on the Asus EEE PC 901
Date: 2009-03-15 11:00
Category: Linux,Debian
Tags: Linux,Debian, Asus
lang: en
translation: true

After installing Xandros I will install Debian Lenny. The steps are as follows:

1. Download the installer image from here along with the md5 file.

2. Check that the image downloaded correctly with the command md5sum debian-eeepc.img.

3. Copy the image to the USB stick (preferably 1GB minimum or 2 GB maximum, since some
  larger USB sticks do not work on the Asus). With the data dump command and the name of the
  device, the command to run is dd if=./debian-eeepc.img of=/dev/sdb, where sdb
  is the device name on the computer I am using.

4. Restart the machine, press F2 to set up booting from the USB stick, and start the installer boot process.

5. The installation process is the same as the Lenny installer; the difference is that this
version supports the Atheros wireless card at boot.

The next post will explain the whole Debian configuration process on the Asus, and then I will try installing Android.

===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)