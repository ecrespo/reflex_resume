Title: Copy Xandros to a flash drive to start the installation process on the Asus EEEPC
Date: 2009-03-15 09:00
Category: Linux
Tags: Debian,Asus  
lang: en
translation: true

One of the nice things about the Xandros that ships with the Asus EEEPC 901 is its desktop paradigm, which moves away from the traditional desktop and closer to the interface of mobile devices such as cell phones.
I had been using the EEEPC 901 with Debian for a while and wanted to try the Xandros installation process in order to reinstall Debian, the stable Lenny release.

You need a flash drive of about 2GB, since sometimes the machine does not read flash drives larger than 2GB, and 1GB ones are not enough to create the boot system.

The first thing to do is find the Asus DVD called Linux Recovery Rev 1.0. Copy the files:

* P701L.gz
* usb.img
* user_start.dat
* 2008.04.03_20.30.bld
* blockcount.dat

The first thing you need to do is plug in the flash drive and run the data dump command:

```
dd if=./usb.img of=/dev/sdb
```

In my case the flash drive is the device sdb.

Then you need to mount the flash drive and copy the files P701L.gz, user_start.dat, 2008.04.03_20.30.bld and blockcount.dat

```
mount /dev/sdb1 /mnt/temporal
cp -v P701L.gz 2008.04.03_20.30.bld blockcount.dat user_start.dat /media/EEEPC/
```

With this procedure the boot flash drive is ready, and all that is left is to plug it into the Asus to start the installation process.

===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)