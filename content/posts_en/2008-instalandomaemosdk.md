Title: Installing the Maemo SDK Chinook on Debian
Date: 2008-03-23 10:21
lang: en
Category: Nokia N810 Debian Maemo

Continuing the posts about the Nokia N810, I will now explain how to install the development kit on Debian.


I based this on a [guide (broken link)](http://linuxuk.blogspot.com/2008/01/installing-os2008-development.html) that explains how to install the
development environment for OS2008 on Ubuntu.

### Installing scratchbox

1. Download Maemo-scratchbox
```
wget http://repository.maemo.org/stable/4.0.1/maemo-scratchbox-install_4.0.1.sh
```

2. Make it executable
```
chmod +x maemo-scratchbox-install_4.0.1.sh
```

3. Run the script
```
./maemo-scratchbox-install_4.0.1.sh -d
```

This installs a version of scratchbox adapted for use with maemo.

A directory named scratchbox will be created in the root of the filesystem. It
will hold the whole structure needed to work with the architecture
used by the Nokia N810.

4. Create the user that will work with scratchbox
```
/scratchbox/sbin/sbox_adduser USERNAME yes
```

USERNAME is the user who will work with the development kit, preferably
a user that already has an account on the machine.

5. Update the list of users related to the /etc/groups file
```
newgrp sbox
```

6. Log in to scratchbox

From the user that was given a scratchbox account, run:
```
/scratchbox/login
```

If it gave no error messages, the installation went perfectly.

You leave with the exit command.

7. Edit nsswitch.conf

Run as root

```
nano /scratchbox/etc/nsswitch.conf
```

The following line has to appear

```
hosts: files dns
```

8. Add the name servers to scratchbox's resolv.conf
```
/scratchbox/login
nano /etc/resolv.conf
```

In my case:
```
nameserver 200.47.79.2
nameserver 200.47.79.3
```

With this, everything is ready to install maemo.

### Installing maemo-sdk.

All of this is done from the user that has the scratchbox account.

1. Download the maemo-sdk-install script
```
wget http://repository.maemo.org/stable/4.0.1/maemo-sdk-install_4.0.1.sh
```

2. Make the script executable
```
chmod +x maemo-sdk-install_4.0.1.sh
```

3. Run the script
```
./maemo-sdk-install_4.0.1.sh
```

At this point the environment for the installation will be created. You accept the
license of the Nokia binaries, and it is recommended to install
maemo with the development environment without the debugging packages.

The package installation will take a while; when it finishes you
will have a development environment.

4. Install xserver-xephyr on the machine.

5. Update maemo.
```
/scratchbox/login
apt-get update
apt-get dist-update
```

6. Start the Xephyr X server.
```
Xephyr :2 -host-cursor -screen 800x480x16 -dpi 96 -ac
```

This command starts a Xephyr X server for maemo.
An X server with a resolution of 800x480 will appear, as in the screenshot.
![Xephyr X server](./images/xephyr.png)


7. View maemo in the Xephyr X server.

Run the following in the scratchbox session:
```
export DISPLAY=:2
af-sb-init.sh start
```

The following screenshot shows the maemo environment.
![Xephyr X server](./images/maemo.png)


With this environment ready, in the next posts I will explain how to create a program for maemo using python.


