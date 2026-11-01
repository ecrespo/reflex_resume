Title: Installing Debian on a MacBook. Part two
Date: 2008-06-08 10:10
lang: en
Category: Debian, Linux, Mac Book

Continuing with the installation process.

After rebooting the machine, select booting from Linux in
rEFIt. Log in with the account you created and open a console
or run synaptic to select the repositories.

In my case I prefer to use the velug ones:
```
deb http://debian.velug.org.ve/debian lenny main contrib non-free
deb http://debian.velug.org.ve/debian-multimedia lenny main
```

Run aptitude update.

The first thing to configure is the wireless network card, whose
chipset is madwifi.

The kernel that lenny ships in its repositories is 2.6.24-1 and the machine
currently has 2.6.22-3, so a more recent kernel is installed. Additionally,
subversion will be installed so that madwifi can be installed from the repository on its official page.

```
aptitude install linux-image-2.6.24-1-amd64 linux-headers-2.6.24-1-amd64 svn subversion
```

When the installation finishes, run lilo to update the boot loader and
reboot the machine.

Now the newest kernel is in place; to verify it, run:

```
debian:~# uname -a
Linux debian 2.6.24-1-amd64 #1 SMP Sat May 10 09:28:10 UTC 2008 x86_64 GNU/Linux
```

Next, configure the wireless network card:

1. Download the madwifi svn trunk:

```
# svn co http://svn.madwifi.org/madwifi/trunk madwifi
```

2. Download hal from people.freebsd.org:

```
# wget http://people.freebsd.org/~sam/ath_hal-20080528.tgz
```

3. Change to the madwifi directory and rename the hal directory:

```
# cd madwifi
# mv hal hal.old
```

4. Extract the contents of the freebsd hal and rename it:

```
# tar -xvzf ../ath_hal-20080528.tgz

# mv ath_hal-20080528 hal
```

5. Compile and install madwifi in the respective directories:

```
#make install BINDIR=/usr/bin MANDIR=/usr/share/man
```

6. Rebuild the module dependency list:

```
#depmod -ae
```

7. Load the madwifi module:

```
#modprobe ath_pci
```

8. Verify that the module loads by checking the output of the dmesg command:

```
ath_hal: module license 'Proprietary' taints kernel.
ath_hal: 0.10.5.6 (AR5210, AR5211, AR5212, AR5416, RF5111, RF5112, RF2413, RF5413, RF2133, RF2425, RF2417)
wlan: svn r3711
ath_pci: svn r3711
ACPI: PCI Interrupt 0000:02:00.0[A] -> GSI 17 (level, low) -> IRQ 17
PCI: Setting latency timer of device 0000:02:00.0 to 64
MadWifi: ath_attach: HAL managed transmit power control (TPC) disabled.
MadWifi: ath_attach: Interference mitigation is supported. Currently disabled.
MadWifi: ath_attach: Switching rfkill capability off.
ath_rate_sample: 1.2 (svn r3711)
wifi0: 11a rates: 6Mbps 9Mbps 12Mbps 18Mbps 24Mbps 36Mbps 48Mbps 54Mbps
wifi0: 11b rates: 1Mbps 2Mbps 5.5Mbps 11Mbps
wifi0: 11g rates: 1Mbps 2Mbps 5.5Mbps 11Mbps 6Mbps 9Mbps 12Mbps 18Mbps 24Mbps 36Mbps 48Mbps 54Mbps
wifi0: turboA rates: 6Mbps 9Mbps 12Mbps 18Mbps 24Mbps 36Mbps 48Mbps 54Mbps
wifi0: turboG rates: 6Mbps 9Mbps 12Mbps 18Mbps 24Mbps 36Mbps 48Mbps 54Mbps
wifi0: H/W encryption support: WEP AES AES_CCM TKIP
wifi0: Atheros AR5418 chip found (MAC 12.10, PHY SChip 8.1, Radio 12.0)
wifi0: Use hw queue 1 for WME_AC_BE traffic
wifi0: Use hw queue 0 for WME_AC_BK traffic
wifi0: Use hw queue 2 for WME_AC_VI traffic
wifi0: Use hw queue 3 for WME_AC_VO traffic
wifi0: Use hw queue 4 for XR traffic
wifi0: Use hw queue 7 for UAPSD traffic
wifi0: Use hw queue 8 for CAB traffic
wifi0: Use hw queue 9 for beacons
ath_pci: wifi0: Atheros 5418: mem=0x50100000, irq=17
```

9. All that is left is to select the wireless network
10. The configured interface is shown below:

```
debian:~# iwconfig ath0
ath0 IEEE 802.11g ESSID:"ROOMSERVER" Nickname:""
Mode:Managed Frequency:2.432 GHz Access Point: 00:14:78:C5:87:0E 
Bit Rate:54 Mb/s Tx-Power:14 dBm Sensitivity=1/1 
Retry:off RTS thr:off Fragment thr:off
Encryption key:off
Power Management:off
Link Quality=73/70 Signal level=-23 dBm Noise level=-96 dBm
Rx invalid nwid:835 Rx invalid crypt:0 Rx invalid frag:0
Tx excessive retries:0 Invalid misc:0 Missed beacon:0
```

You can now free yourself from the network cable and use the laptop over its wireless connection.

The next post will continue with the laptop's configuration.

===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)