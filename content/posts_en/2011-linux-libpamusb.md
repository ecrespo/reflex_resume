Title: Logging in a user by authenticating with a flash drive
Date: 2011-07-26 09:00
Category: Tutorial de Linux
Tags: Linux,Debian, Ubuntu, Canaima,libpam,gnome, usb
lang: en
translation: true

When you go a bit paranoid, you come up with ideas for how to validate users when they log in to a desktop session through GDM.

In Debian/Ubuntu/Canaima there are the packages libpam-usb and pamusb-tools, which let you create a key that is stored on the flash drive. Then pam is configured to ask for the key when the user and password are entered in the machine's GDM; if the flash drive is not plugged in, GDM shows an invalid password message.

To install these packages, run aptitude:

```
aptitude install libpam-usb pamusb-tools
```

Then plug the flash drive into the machine and add the device to /etc/pamusb.conf with the pamusb-conf command:

```
pamusb-conf --add-device /media/F060-785C/
```

Where /media/F060-785C/ is the path of the flash drive.

Add to /etc/pamusb.conf the user who will log in to the machine:

```
pamusb-conf --add-user ecrespo
```

Check the pamusb configuration with the user that was added:

```
pamusb-check ecrespo
* Authentication request for user "ecrespo" (pamusb-check)
* Device "/media/F060-785C/" is connected (good).
* Performing one time pad verification...
* Regenerating new pads...
* Unable to update pads.
* Access granted.
```

When the program returns access granted, everything is ready to use the flash drive at login; all that is left is to modify pam so that it allows authentication with the flash drive.

Edit the file /etc/pam.d/common-aut and add the following line:

```
auth sufficient pam_usb.so
```

With this line GDM verifies the key's token; if you want it to ask for both the password and the token, change sufficient to required.

```
auth required pam_usb.so
```

From now on, logging in requires both the password and the token.

Below is the message the console prints when running sudo -s :

```
[sudo] password for ecrespo: 
* pam_usb v0.4.2
* Authentication request for user "ecrespo" (sudo)
* Device "/media/F060-785C/" is connected (good).
* Performing one time pad verification...
* Regenerating new pads...
* Unable to update pads.
* Access granted.
```



===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)