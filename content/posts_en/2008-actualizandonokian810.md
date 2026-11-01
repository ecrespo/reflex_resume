Title: Updating the firmware of the Nokia N810
Date: 2008-03-23 10:20
lang: en
Category: Nokia N810

This Holy Week I devoted myself to updating my devices that run Linux (nslu2 and nokia n810). All I need now is to buy a memory card for the PSP so I can install Linux on it too.
This post is dedicated to the Nokia N810 and the firmware update.

The firmware that ships with the device has some problems with certain packages and their dependencies, such as skype and xchat. So the first thing to do is update it before installing additional programs.

The steps are as follows:

1. Download the [flasher-3.0 (broken link)](http://tablets-dev.nokia.com/d3.php) program.
2. Download the firmware for the Nokia N810. You can download the latest version of the firmware here.
3. Make sure the Nokia's battery is fully charged.
4. Disconnect the Nokia from the power supply and turn it off.
5. Connect the Nokia to the computer's USB port without turning it on.
6. Run the following command as root:
```
./flasher-3.0 -F  RX-44_2008SE_2.2007.51-3_PR_COMBINED_MR0_ARM.bin -f -R
```
7. The following message will appear in the computer's console: "Suitable USB device not found, waiting"
8. Turn on the Nokia and the firmware update process will start; the tablet will show the USB-connected symbol.
9. When it finishes, the console shows the message: you're done now!
10. The device is now updated. If the update is not done when the device is brand new, you need to back it up with the backup and recovery tools.
