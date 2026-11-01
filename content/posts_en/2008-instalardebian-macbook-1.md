Title: Installing Debian on a MacBook. Part One
Date: 2008-06-08 10:00
lang: en
Category: Debian, Linux, Mac Book

### Preparations 

The first thing to do is download the [rEFIT](http://refit.sourceforge.net/) application and install it
on MacOSX. Repartition the hard drive from MacOSX and restart the machine.

At this point the rEFIT boot menu appears; in this menu there is a console icon
labeled refit, which you have to select, and once refit finishes booting you need to
run gptsync to synchronize the hard drive partitions with the refit application. Answer
Y (yes) and then restart the machine to boot from the Debian installation CD.


### Which version should I use?

It depends on the processor in the machine. In my case, on the MacBook I have I cannot
install with the amd64 CD, only with the i386 CD. But if the machine has a latest-generation
Core Duo processor, you will use the AMD64 one.

I prefer to install a laptop with lenny rather than etch right now, especially since lenny is
already being stabilized.

If you are going to use lenny, I recommend installing in expert mode, because this version
has a problem when configuring the video: the installation environment is lost and it becomes
necessary to do a remote installation via ssh.

### Installation process

Restart the machine with the Debian Lenny CD inserted, select booting from the cdrom in refit and
then type expert.

1. Language selection: Spanish
2. Country selection: Venezuela
3. Keyboard selection: Latin American (for the time being)
4. Select UTF-8 venezuela.
5. CD verification and selection of cdrom components: select the ssh options.
6. Network card configuration (of course, for now do the installation over a network cable).
7. Network configuration via DHCP.
8. Remote installation via ssh configuration: a password is created for the installer user and then it gives us the IP to use.
9. From a second machine, connect via ssh to the machine's IP, e.g.: ssh installer@x.x.x.x
10. Select install debian (first option).
11. At this point steps 1, 2, 3 and 4 are repeated.
12. Hard drive detection and partitioning (there are many possibilities). I created only 3 partitions: /, /home and swap, and the size you assign to the partitions depends on the size of the hard drive.
13. Formatting the hard drive and installing a base system
14. Create the machine's administrator password.
15. Create a user account.
16. Select a repository.
17. Choose whether to take part in the package popularity survey of installed programs; you can say yes or no.
18. Selection of the packages to install (Base system, Desktop and Laptop). With this option you will have a base laptop with everything a user needs to work.

19. The package installation process starts.
20. Screen resolution configuration (depends on the laptop): select 1280x800.
21. Boot configuration (if you try grub it will give an error); in this case you have to install lilo as the boot manager on the root partition.

22. After installing the boot loader it is a good idea to synchronize the hard drive again:
Open a second console (control+alt+F2) from the installation CD and run
```
chroot /target aptitude install refit
 /target/sbin/gptsync /dev/sda
```

23. At this point Debian will be installed and all that is left is to remove the installation CD and restart the machine.

The second part of the post will cover configuring and tuning the machine.

===

Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)