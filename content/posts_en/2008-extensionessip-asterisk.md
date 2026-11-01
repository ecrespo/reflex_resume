Title: Creating SIP extensions
Date: 2008-04-14 10:00
lang: en
Category: Asterisk, Debian, Linux

To create the SIP extensions you need to modify the 
file /etc/asterisk/sip.conf. 10 extensions will be created. 

These extensions run from 1000 to 1010.

Before creating the extensions, the structure 
of the sip.conf file will be explained.

### The sip.conf file

The sip.conf file is read from top to bottom.

1. The [general] section contains the global options. These options are:

* allow: Enables a given codec. The all option can be used.
* bindaddr: IP address that asterisk will use to listen.
* disallow: Disables a given codec. The all option can be used.
* bindport: Port where asterisk waits for connections.
* maxexpirey: Maximum registration time in seconds.
* defaultexpirey: Default registration time in seconds.
* register: Registers Asterisk with another host. The format is a SIP address optionally followed by a slash / and an extension.

* language: Defines the language to use.

An example follows:
```
[general]
bindport = 5060
bindaddr = 10.1.30.45
context = default
disallow = all
allow = ulaw
maxexpirey = 120
defaultexpirey = 80
```

2. Options for each phone.

The options for each phone are:

* [name]: The user name part of the SIP user.
* peer: Entity to which asterisk sends calls.
* user: Entity that makes calls through asterisk.
* type: Sets the kind of connection; the options are peer (receives calls from asterisk), user (makes calls to asterisk) and friend (receives and makes calls).

* host: IP address or host name of the device that connects to asterisk. The dynamic option can also be used, in which case the phone is expected to register.

* secret: A password shared between the phone and the asterisk server to authenticate peers and users when making a call.

An example follows:
```
[polycom]
type=friend
secret=1234
host=10.58.254.15
context=trusted
[ekiga]
type=friend
secret=1234
host=dynamic
```

3. Dial plan.

The dial plan defines how asterisk will handle 
calls. The dial plan is configured in the file 
/etc/asterisk/extensions.conf, and it is structured in 4 parts:

* Applications. Applications are an important part of asterisk. 
They act on the voice channel, playing sounds, accepting digits or 
hanging up a call.

* Contexts: They let you organize the dial plan and improve its security. Contexts are tied to channels.
* Extensions: A string that triggers an event. There are 3 types: literal, standard or special.
* Priority: Numbered execution steps of each extension. Each priority calls a specific application. They start at 1 and increase by 1.

An example follows:
```
exten=>8580,1,Dial(SIP/8580,20)
exten=>8580,2,voicemail(u8580)
exten=>8580,101,voicemail(b8580)
exten=> número (nombre), prioridad, aplicación
```

### Configuration files

1. File /etc/asterisk/sip.conf

```
[1000] 
type=friend
username=1000
secret=1234
host=dynamic
context=sip
mailbox=100

[1001] 
type=friend
username=1001
secret=1234
host=dynamic
context=sip
mailbox=101

[1002] 
type=friend
username=1002
secret=1234
host=dynamic
context=sip
mailbox=102

[1003] 
type=friend
username=1003
secret=1234
host=dynamic
context=sip
mailbox=103

[1004] 
type=friend
username=1004
secret=1234
host=dynamic
context=sip
mailbox=104

[1005] 
type=friend
username=1005
secret=1234
host=dynamic
context=sip
mailbox=105

[1006] 
type=friend
username=1006
secret=1234
host=dynamic
context=sip
mailbox=106

[1007] 
type=friend
username=1007
secret=1234
host=dynamic
context=sip
mailbox=107

[1008] 
type=friend
username=1008
secret=1234
host=dynamic
context=sip
mailbox=108

[1009] 
type=friend
username=1009
secret=1234
host=dynamic
context=sip
mailbox=109

[1010] 
type=friend
username=1010
secret=1234
host=dynamic
context=sip
mailbox=110
```

2. File extensions.conf

```
[sip] #; aqui defino la seccion sip
exten => 1000,1,Dial(SIP/1000,20); Si el número a llamar es 1000, se llama al usuario 1000, mediante canal sip, dejar que suene por 20 segundos, si no hay respuesta se procede a la prioridad 2.
exten => 1000,2,Voicemail(u1000); La prioridad 2 llama al buzon de voz. y se da el mensaje que el usuario 1000 no está disponible. La única forma de salir de acá es colgando la llamada.
exten => 1000,102,Voicemail(b1000); Si el número de marcado en la prioridad 1 devuelve un estado "busy" entonces el dial saltará a la prioridad 101+ prioridad actual, resultando 102.
exten => 1000,103,Hangup

exten => 1001,1,Dial(SIP/1001,20)
exten => 1001,2,Voicemail(u1001)
exten => 1001,102,Voicemail(b1001)
exten => 1001,103,Hangup

exten => 1002,1,Dial(SIP/1002,20)
exten => 1002,2,Voicemail(u1002)
exten => 1002,102,Voicemail(b1002)
exten => 1002,103,Hangup

exten => 1003,1,Dial(SIP/1003,20)
exten => 1003,2,Voicemail(u1003)
exten => 1003,102,Voicemail(b1003)
exten => 1003,103,Hangup

exten => 1004,1,Dial(SIP/1004,20)
exten => 1004,2,Voicemail(u1004)
exten => 1004,102,Voicemail(b1004)
exten => 1004,103,Hangup

exten => 1005,1,Dial(SIP/1005,20)
exten => 1005,2,Voicemail(u1005)
exten => 1005,102,Voicemail(b1005)
exten => 1005,103,Hangup

exten => 1006,1,Dial(SIP/1006,20)
exten => 1006,2,Voicemail(u1006)
exten => 1006,102,Voicemail(b1006)
exten => 1006,103,Hangup

exten => 1007,1,Dial(SIP/1007,20)
exten => 1007,2,Voicemail(u1007)
exten => 1007,102,Voicemail(b1007)
exten => 1007,103,Hangup

exten => 1008,1,Dial(SIP/1008,20)
exten => 1008,2,Voicemail(u1008)
exten => 1008,102,Voicemail(b1008)
exten => 1008,103,Hangup

exten => 1009,1,Dial(SIP/1009,20)
exten => 1009,2,Voicemail(u1009)
exten => 1009,102,Voicemail(b1009)
exten => 1009,103,Hangup

exten => 1010,1,Dial(SIP/1010,20)
exten => 1010,2,Voicemail(u1010)
exten => 1010,102,Voicemail(b1010)
exten => 1010,103,Hangup
```


Imagine having to create 100 extensions!!!!!

To solve this you can define a set of extensions using patterns.

An extension name is a pattern if it starts with an 
underscore character "_".

The following characters have a special meaning:

* X: Matches any digit from 0-9.
* Z: Matches any digit from 1-9.
* N: Matches any digit from 2-9.
* 1237-9]: Matches any digit in the range.
* . : Matches one or more characters.

Asterisk also uses some extension names for special purposes:

* ¡ : Invalid.
* s: Start.
* h: Hangup.
* t: Timeout.
* T: Absolute timeout.
* o: Operator.
* a: Called when the user presses "*" during the initial voicemail greeting.
* fax: Used for fax detection on zap channels.

Additionally, variables will be used to simplify the extensions.

This example covers extensions 1000 through 1019. It uses the variable 
EXTEND, which holds the extension number.

```
exten => _10[0-1]X,1,Dial(SIP/${EXTEND},20)
exten => _10[0-1]X,2,Voicemail(u${EXTEN})
exten => _10[0-1]X,102,Voicemail(b${EXTEN})
exten => _10[0-1]X,103,Hangup
```

===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC) 
using the digital wallet of your choice to the following 
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)