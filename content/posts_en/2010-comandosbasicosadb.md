Title: Basic adb (Android Debug Bridge) commands to access the Motorola Milestone A853
Date: 2010-05-29 10:00
Category: Tutorial Linux
Tags: Linux, Android, Debian
lang: en
translation: true

In the [previous article](/blog/instalacionsdkandroiddebian) I explained how to install the Android SDK on Debian. Next I will explain the command that gives access to the phone, such as viewing the microsd, installing applications on the phone from the computer, among other things. 

Change to the tools directory of the Android SDK. 

```
cd android-sdk_r06-linux_86/tools 
```

Create a link from the adb application to /usr/bin . 

```
sudo ln -s /home/ernesto/android-sdk-linux_86/tools/adb /usr/bin/adb 

ls -l /usr/bin/adb 
lrwxrwxrwx 1 root root 44 may 27 20:12 /usr/bin/adb -> /home/ernesto/android-sdk-linux_86/tools/adb 
```

Create the file 50-android.rules in the /etc/udev/rules.d directory 

```
vim /etc/udev/rules.d/50-android.rules 

```

Add the following content to the file: 

```
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0bb4", ATTRS{idProduct}=="0c02", GROUP="androiddev", SYMLINK+="android%n" 
```

Create the androiddev group. 

```
sudo addgroup --system androiddev 

```

Change the file permissions and reload the udev rules. 

```
sudo chmod a+rx /etc/udev/rules.d/50-android.rules 
sudo /etc/init.d/udev reload 
```

On the phone, make sure USB debugging mode is enabled. That is: 
Settings->Applications->Development. 

Start adb as a server: 

```
sudo ./adb start-server 

```

Then verify that you have access to the phone with the adb devices command. 

```
adb devices 
* daemon not running. starting it now * 
* daemon started successfully * 
List of devices attached 
0403725B09015010 device 
```

When this information appears, and not strange characters or ??? or nothing at all, the phone is already connected to the computer. 


The adb shell command creates a shell on the phone and the ls -l command is run: 

```
$ ls -l 
drwxrwxrwt root root 2010-05-29 08:01 tmp 
drwxrwxr-x system system 2010-02-23 07:41 pds 
drwxrwxrwt root root 2010-05-29 13:21 sqlite_stmt_journals 
dr-x------ root root 2010-05-29 08:00 config 
drwxrwx--- system cache 2010-05-27 11:00 cache 
d---rwxr-x system sdcard_rw 2010-05-29 08:01 sdcard 
lrwxrwxrwx root root 2010-05-29 08:00 d -> /sys/kernel/debug 
lrwxrwxrwx root root 2010-05-29 08:00 etc -> /system/etc 
drwxr-xr-x root root 2010-01-06 09:29 system 
drwxr-xr-x root root 1969-12-31 20:00 sys 
drwxr-x--- root root 1969-12-31 20:00 sbin 
dr-xr-xr-x root root 1969-12-31 20:00 proc 
-rwxr-x--- root root 453 1969-12-31 20:00 init_prep_keypad.sh 
-rwxr-x--- root root 13218 1969-12-31 20:00 init.rc 
-rwxr-x--- root root 14824 1969-12-31 20:00 init.mapphone_umts.rc 
-rwxr-x--- root root 6840 1969-12-31 20:00 init.mapphone_cdma.rc 
-rwxr-x--- root root 1677 1969-12-31 20:00 init.goldfish.rc 
-rwxr-x--- root root 104324 1969-12-31 20:00 init 
-rw-r--r-- root root 118 1969-12-31 20:00 default.prop 
drwxrwx--x system system 2010-05-29 08:01 data 
drwx------ root root 2009-11-19 15:42 root 
drwxr-xr-x root root 2010-05-29 08:01 dev 
```

This command shows the files and directories on the phone. Note that these are unix/Linux commands, so if you change to the system directory and then app, there you will find the apk packages that are installed on the phone. 


```
$cd /system/app 
pwd 
$pwd 
/system/app 
$ls -l 
-rw-r--r-- root root 1500786 2010-01-06 09:28 MotoID.apk 
-rw-r--r-- root root 433280 2010-01-06 09:28 MovilnetContainer.apk 
-rw-r--r-- root root 2624470 2010-01-06 09:28 Maps.apk 
-rw-r--r-- root root 677433 2010-01-06 09:28 Talk.apk 
-rw-r--r-- root root 50410 2010-01-06 09:28 GoogleContactsSyncAdapter.apk 
-rw-r--r-- root root 327750 2010-01-06 09:28 MediaUploader.apk 
-rw-r--r-- root root 1310501 2010-01-06 09:28 Vending.apk 
-rw-r--r-- root root 735409 2010-01-06 09:28 Gmail.apk 
-rw-r--r-- root root 380550 2010-01-06 09:28 GoogleApps.apk 
-rw-r--r-- root root 778098 2010-01-06 09:28 SetupWizard.apk 
-rw-r--r-- root root 53777 2010-01-06 09:28 TalkProvider.apk 
```

These are some of the programs installed on the phone. 

The commands you can use in the shell are the following: 

* ls Lists the directories and folders in the path we are in.
* reboot Restarts the device
* rm Deletes a file
* rmdir Deletes a directory
* cd Changes directory
* mkdir Creates a directory
* mkswapp Creates a swap system
* mount Mounts a drive or partition
* umount Unmounts a drive
* mv Moves or renames a file 

You can run an ls inside sdcard/Videos and the following is shown: 

```
$adb shell ls /sdcard/Videos/ 
How.I.Met.Your.Mother.S05E21.HDTV.XviD-LOL.[VTV].avi 
The.Big.Bang.Theory.S03E20.The.Spaghetti.Catalyst.HDTV.XviD-FQM.avi 
```

To delete the files, run adb shell rm and then run ls again to show that the files have been deleted from the phone's sd card: 

```
ernesto@jewel:~$ adb shell rm sdcard/Videos/*.avi 
ernesto@jewel:~$ adb shell ls sdcard/Videos 
ernesto@jewel:~$ 
```

You can also install applications on the phone from the computer with the adb install packagepath.apk command: 


Next, a Sudoku application is installed from the computer to the phone. 


```
ernesto@jewel:~$ adb install /home/ernesto/Descargas/OpenSudoku-1.1.1-02.apk 
603 KB/s (223640 bytes in 0.361s) 
pkg: /data/local/tmp/OpenSudoku-1.1.1-02.apk 
Success 
```

You can also copy files from the phone to the computer and from the computer to the phone: 

```
ernesto@jewel:~$ adb push /home/ernesto/varios.mp3 /sdcard/mp3z/ 
1944 KB/s (7768607 bytes in 3.901s) 
```

In this example an mp3 file is copied from the computer to the phone. 

```
ernesto@jewel:~$ adb pull /sdcard/python_scripts_r0.zip ./ 
52 KB/s (4280 bytes in 0.078s)
```

This command brings a file from the phone's sdcard memory to the computer. 

The next article will explain how to connect to the internet from an Android phone. 


===

Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)