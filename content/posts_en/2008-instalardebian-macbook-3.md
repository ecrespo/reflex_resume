Title: Installing Debian on a Mac Book. Part three (configuration)
Date: 2008-06-08 10:30
lang: en
Category: Debian, Linux, Mac Book

Continuation of the Mac Book configuration.

Configuring backlight + volume + CD-ROM eject:
The backlight (Fn+F1 and Fn+F2 keys) works fine using the program [pommed](http://packages.debian.org/pommed), 
pommed also enables the CD-ROM eject button. [gpomme](http://packages.debian.org/gpomme) 
is a graphical application for configuring pommed.

By default in Debian the F1, F2, F3, ..F12 keys are disabled and act 
the same as the Fn+F1 and Fn+F2, .... Fn+F12 keys. 

To enable the use of the keys you must edit the file /etc/pommed.conf, 
change init=-1 to init=80, change volume="PCM" to volume="Front" and restart 
pommed (/etc/init.d/pommed restart).


1. High resolution video playback:

Edit /etc/X11/xorg.conf and add the following to the Device section:

```
Option "LinearAlloc" "6144"
Option "CacheLines" "1080"
```

2. Keyboard configuration:
2.1. X11 configuration:

Add this option in the keyboard section:

```
Option          "XkbOptions"    "lv3:rwin_switch,apple:badmap"
```

It can also be configured from the GNOME desktop at:
System-> 'Preferences' -> 'Keyboard'.

And select the macbook/macbook pro (int) keyboard.

For the console, add the following line to /etc/console-tools/remap:

```
s/keycode 126 =/keycode 126 = AltGr/;
```

For mouse emulation on the keyboard you can make the following key assignments:


```
xmodmap -e "keycode 115 = Alt_L"           # left-apple
xmodmap -e "keycode 116 = Zenkaku_Hankaku" # right-apple
xmodmap -e "keycode 108 = Pointer_Button3" # KP-ENTER
xmodmap -e "keycode 204 = Pointer_Button2" # eject
xkbset m
```

Touchpad configuration:

Install gsynaptics:

```
aptitude install gsynaptics
```

Edit /etc/X11/xorg.conf adding the following:

```
Section "InputDevice"
      Identifier      "Synaptics Touchpad"
      Driver          "synaptics"
      Option          "SendCoreEvents"        "true"
      Option          "Device"                "/dev/psaux"
      Option          "Protocol"              "auto-dev"
      Option          "HorizScrollDelta"      "0"
EndSection
```

Add the following lines in /etc/modprobe.d/:

```
install usbhid /sbin/modprobe appletouch; /sbin/modprobe --ignore-install usbhid $CMDLINE_OPTS
```

Then add appletouch to /etc/initramfs-tools/modules and run update-initramfs.

A possible configuration in xorg.conf is the following:

```
Section "InputDevice"
       Identifier      "Configured Mouse"
       Driver          "synaptics"
       Option          "SendCoreEvents"        "true"
       Option          "Device"                "/dev/input/mice"
       Option          "Protocol"              "auto-dev"
       Option          "LeftEdge"              "0"
       Option          "RightEdge"             "850"
       Option          "TopEdge"               "0"
       Option          "BottomEdge"            "645"
       Option          "MinSpeed"              "0.4"
       Option          "MaxSpeed"              "1"
       Option          "AccelFactor"           "0.02"
       Option          "FingerLow"             "55"
       Option          "FingerHigh"            "60"
       Option          "MaxTapMove"            "20"
       Option          "MaxTapTime"            "100"
       Option          "HorizScrollDelta"      "0"
       Option          "VertScrollDelta"       "30"
       Option          "SHMConfig"             "on"
   EndSection
```


Processor-related settings.
CPU frequency scaling.
Run the following:

```
echo acpi_cpufreq >> /etc/modules
```

Frequency scaling in user space:

Install powertop, which lets you reduce battery consumption while working on battery.

```
aptitude install powertop
```

Install powernowd

```
aptitude install powernowd
```

===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC) 
using the digital wallet of your choice to the following 
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)