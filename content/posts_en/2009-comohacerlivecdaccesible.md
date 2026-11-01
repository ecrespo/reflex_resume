Title: How to make a live-usb or live-cd
Date: 2009-03-29 10:00
Category: Linux
Tags: Live-CD,Debian,Instalación
lang: en
translation: true

Based on the guides at the following links: [live-usb (broken link)](http://www.debian-administration.org/articles/630) and the Spanish tutorial on [Debian Live (broken link)](http://el-directorio.org/DebianLive#head-9df2b36e5793bbfb9353ffbf472fb3e38608935e), which is a tutorial for the old version of live-helper called live-package,
or this other [tutorial (broken link)](http://wiki.freenetproject.org/deDebianLiveCD) that explains how to remaster the live-cd.

Live-helper is a framework that allows you to create a live-cd or live-usb
based on a Debian system.

You need a machine with enough disk space to build the live
system; 3GB of space is enough.

1. Install live-helper:

```
aptitude install live-helper
```

2. Create a directory to work in:  

```
mkdir live-usb
```

3. Change to the working directory.

```
cd live-usb
```

4. Create the configuration for building the live-usb.

```
lh_config -b usb-hdd -d lenny --mirror-bootstrap http://debian.velug.org.ve/debian/ --mirror-chroot http://debian.velug.org.ve/debian/ --mirror-binary http://debian.velug.org.ve/debian --username Usuario --iso-publisher "Ernesto Crespo" -l es --security disabled --hostname live-usb --bootappend-live "locale=es_VE.UTF-8 keyb=es" --packages-lists "gnome gdm iceweasell-i10n-es-es iceweasel pidgin openoffice openoffice.org-writer openoffice.org-l10n-es myspell-es evince less mc module-assistant wireless-tools printconf hpijs foomatic-db-gutenprint cupsys-bsd foomatic-filters-ppds hplip foomatic-db-hpijs cupsys cupsys-client cupsys-driver-gutenprint foomatic-db-engine vim-full "
```

5. Build the image.

```
lh_build
```

6. Copy the binary.img image to the pendrive. If the device is identified as /dev/sda, run the following command.

```
dd if=./binary.img of=/dev/sda bs=1M
```

7.1. Test the iso. If it is a live-cd, run:

```
qemu -cdrom binary.img -boot d
```

7.2. If it is a live-usb, run:

```
qemu -hda binary.img -boot c
```

This process creates an image called binary.img for USB devices. It defines
the repository to use, the live user name, a description of the person
publishing the live system, the locales to use and the keyboard layout at
boot time of the live system; finally, it defines the list of packages to include in the live-usb.

If you want to create a live-cd, keep in mind that the maximum size a live-cd can have
is 700MB, so the environment configuration is the following:

```
lh_config -b iso -d lenny --mirror-bootstrap http://debian.velug.org.ve/debian/ --mirror-chroot http://debian.velug.org.ve/debian/ --mirror-binary http://debian.velug.org.ve/debian --username usuario --iso-publisher "Ernesto Crespo" -l es --security disabled --hostname live-cd --bootappend-live "locale=es_VE.UTF-8 keyb=es" --bootstrap-flavour minimal --apt apt --linux-flavours 486 --binary-indices disabled --memtest disabled --apt-recommends disabled --packages-lists "gnome gdm iceweasell-i10n-es-es iceweasel pidgin openoffice openoffice.org-writer openoffice.org-l10n-es myspell-es evince less mc module-assistant wireless-tools printconf hpijs foomatic-db-gutenprint cupsys-bsd foomatic-filters-ppds hplip foomatic-db-hpijs cupsys cupsys-client cupsys-driver-gutenprint foomatic-db-engine"
```


The options in a different color will reduce the size of the live-cd since a minimal image will be built,
apt-get will be used instead of aptitude, the kernel for the 486 architecture will be used, the binary
indices are disabled, as are the installation of memtest and apt recommendations.

===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)