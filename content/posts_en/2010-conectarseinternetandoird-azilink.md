Title: Connecting to the internet through an Android phone (AziLink)
Date: 2010-05-29 13:00
Category: Tutorial Linux
Tags: Linux, Android, Debian
lang: en
translation: true


Unlike applications that use an http proxy, AziLink lets you connect through the phone using openvpn.

You can find the AziLink project page at this [link](http://code.google.com/p/azilink/).

The link to download openvpn is openvpn.net. On Debian and Ubuntu, running aptitude is enough:

```
aptitude install openvpn-blacklist openvpn

```

The steps are the following:
1. Enable USB debugging mode on the phone. From the phone's applications home, go to Settings->Applications->Development->USB debugging.

2. Install the Android SDK; you can find the procedure at this [link](/blog/instalacionsdkandroiddebian).
3. Install AziLink from the phone's market.
4. On the computer, do the port forwarding:

```
adb forward tcp:41927 tcp:41927
```

5. On the phone, run AziLink and verify that its service is active.
6. Download and unzip azilink.zip, which contains the configuration file.

The openvpn configuration is the following:

```
#Define tun como dispositivo
dev tun
#Define la IP y puerto remoto, el que se configuro en la redirección con adb
remote 127.0.0.1 41927 tcp-client
#Define la IP punto a punto de la conexión openvpn
ifconfig 192.168.56.2 192.168.56.1
#Define rutas
route 0.0.0.0 128.0.0.0
route 128.0.0.0 128.0.0.0
#Define flags del socket.
socket-flags TCP_NODELAY
#keepalive 10 30
ping 10
#Define el DNS por medio de las opciones de dhcp
dhcp-option DNS 192.168.56.1
```

7. Add the following DNS to /etc/resolv.conf:

```
nameserver 192.168.56.1
```

8. Start openvpn with the configuration file:

```
sudo openvpn --config azilink.ovpn 
```

```
Sat May 29 23:28:18 2010 OpenVPN 2.1.0 i486-pc-linux-gnu [SSL] [LZO2] [EPOLL] [PKCS11] [MH] [PF_INET6] [eurephia] built on Apr 10 2010
Sat May 29 23:28:18 2010 WARNING: --ping should normally be used with --ping-restart or --ping-exit
Sat May 29 23:28:18 2010 NOTE: OpenVPN 2.1 requires '--script-security 2' or higher to call user-defined scripts or executables
Sat May 29 23:28:18 2010 ******* WARNING *******: all encryption and authentication features disabled -- all data will be tunnelled as cleartext
Sat May 29 23:28:18 2010 TUN/TAP device tun0 opened
Sat May 29 23:28:18 2010 /sbin/ifconfig tun0 192.168.56.2 pointopoint 192.168.56.1 mtu 1500
Sat May 29 23:28:18 2010 Attempting to establish TCP connection with [AF_INET]127.0.0.1:41927 [nonblock]
Sat May 29 23:28:18 2010 TCP connection established with [AF_INET]127.0.0.1:41927
Sat May 29 23:28:18 2010 TCPv4_CLIENT link local: [undef]
Sat May 29 23:28:18 2010 TCPv4_CLIENT link remote: [AF_INET]127.0.0.1:41927
Sat May 29 23:28:21 2010 Peer Connection Initiated with [AF_INET]127.0.0.1:41927
Sat May 29 23:28:22 2010 Initialization Sequence Completed
```

Checking on whatismyip.com, the IP being used is 201.239.27.224.

Personally I prefer this option over using an http proxy. The openvpn configuration file could be improved, for example by copying the resolv.conf file when bringing up the vpn and restoring the previous file when stopping the vpn.


===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)