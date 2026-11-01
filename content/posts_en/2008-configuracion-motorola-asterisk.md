Title: Configuring a Motorola X100P card
Date: 2008-04-13 10:10
lang: en
Category: Asterisk, Debian, Linux

Asterisk is already installed, and now comes the configuration 
of the Motorola X100P card.

### Configuration procedure: 

1. Edit the file /etc/default/zaptel so that it only handles 
the module that should be used (wcfxo). This is done by commenting out 
all the modules that will not be used.

2. View the device

```
zaptel_hardware -v
pci:0000:01:00.0 wcfxo- 1057:5608 Wildcard X100P
```

3. Check that the card works

```
ztcfg -vvvvvvvvvvvvvv
Zaptel Version: 1.4.9.2
Echo Canceller: MG2
Configuration
======================


Channel map:

Channel 01: FXS Kewlstart (Default) (Slaves: 01)

1 channels to configure.
```

4. Edit the file /etc/asterisk/zapata.conf. Add the following lines:

```
[channels]
language=es
context=entrantes
signalling=fxs_ks
usecallerid=yes
hidecallerid=no
callwaiting=yes
callwaitingcallerid=yes
threewaycalling=yes
transfer=yes
cancallforward=yes
callreturn=yes
echocancel=yes
echocancelwhenbridged=yes
rxgain=0.0
txgain=0.0
group=1
pickupgroup=1
immediate=yes
musiconhold=default channel => 1
```

5. Reload modules

```
asterisk -rx "module reload"
```

6. Add an extension that allows calling through the card. Edit /etc/asterisk/extension.conf

```
[entrantes]
exten => s,1,Dial(SIP/1000,60,tr)
exten => s,2,Voicemail,u1000
exten => s,102,Voicemail,b1000 
```

These lines tell Asterisk to route every call the card receives 
to the phone "1000", and after 60 seconds the voicemail kicks in.

To make outgoing calls we will add the following lines:

```
[salientes]
exten => _[9]XXXXXXXX,1,Dial,Zap/1/${EXTEN}
```

All numbers that start with 9 are dialed using the card.


Still to be configured: the extensions, call waiting, conference calls, 
among other things.

===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC) 
using the digital wallet of your choice to the following 
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)