Title: Creating a gpg key from Python
Date: 2012-03-03 09:00
Category: Tutorial de Python
Tags: Canaima,Debian,General,Python,Seguridad,Ubuntu
lang: en
translation: true

There are several tools to create and manipulate `gpg` keys.

Those who do not know `GPG` can read the following [tutorial](http://personales.upv.es/%7Ealalbiol/pages/Mini_Tutorial_GPG.html).

The Python package that handles `gpg` keys is `python-pyme`.  

```
#apt-get install python-pyme python-pyme-doc
```

You can find the pyme library documentation at the following [link](http://pyme.sourceforge.net/doc/pyme/index.html).

The documentation has a list of examples; copy the `genkey.py` file to the user's home:  

```
cp /usr/share/doc/python-pyme-doc/examples/genkey.py ~/
```

Edit the `genkey.py` file: change the key type to RSA, set the key length (1024, 2048 or 4096), the subkey length (the same value as the key length), the real name, the name comment, the email, the key passphrase and the key expiration date.  
```python 
#!/usr/bin/env python
# $Id: genkey.py,v 1.6 2008/03/08 18:21:08 belyi Exp $
# Copyright (C) 2004 Igor Belyi <belyi@users.sourceforge.net>
# Copyright (C) 2002 John Goerzen <jgoerzen@complete.org>
#
#    This program is free software; you can redistribute it and/or #modify
#    it under the terms of the GNU General Public License as #published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty #of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  #See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public #License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  #02111-1307  #USA
	 
	
#Importar pyme
from pyme import core, callbacks
	
# Initialize our context.
#Inicializa el contexto.
core.check_version(None)
c = core.Context()
#Se define algunas configuraciones
c.set_armor(1)
c.set_progress_cb(callbacks.progress_stdout, None)
	
# This example from the GPGME manual
#Este es un ejemplo desde el manual gpgme.
	
parms = """<GnupgKeyParms format="internal">
Key-Type: RSA
Key-Length: 2048
Subkey-Type: ELG-E
Subkey-Length: 2048
Name-Real: Ernesto Nadir Crespo Avila
Name-Comment: seraph1
Name-Email: ecrespo@gmail.com
Passphrase: frasedelallave
Expire-Date: 2020-08-15
</GnupgKeyParms>
"""
#Se genera la llave pasandole los parámetros.
c.op_genkey(parms, None, None)
#Se imprime en patanalla el resultado de la generación.
print c.op_genkey_result().fpr
```	

To create the key, run the `genkey.py` file:  
```python 
$python genkey.py
......
PROGRESS UPDATE: what = primegen, type = 46, current = 0, total = 0
PROGRESS UPDATE: what = primegen, type = 46, current = 0, total = 0
PROGRESS UPDATE: what = primegen, type = 43, current = 0, total = 0
PROGRESS UPDATE: what = primegen, type = 43, current = 0, total = 0
PROGRESS UPDATE: what = primegen, type = 43, current = 0, total = 0
PROGRESS UPDATE: what = primegen, type = 43, current = 0, total = 0
PROGRESS UPDATE: what = primegen, type = 43, current = 0, total = 0
PROGRESS UPDATE: what = primegen, type = 94, current = 0, total = 0
PROGRESS UPDATE: what = primegen, type = 94, current = 0, total = 0
PROGRESS UPDATE: what = primegen, type = 94, current = 0, total = 0
PROGRESS UPDATE: what = primegen, type = 94, current = 0, total = 0
FFF598686F3ADE35C52BF65E4478C8341643F0EB
```
	
Listing the keys gives the following:  
```python 
$gpg --list-keys
...
pub   2048R/1643F0EB 2012-03-04 [caduca: 2020-08-15]
uid                  Ernesto Nadir Crespo Avila (seraph1) <ecrespo@gmail.com>
sub   2048g/9F8E9C20 2012-03-04 [caduca: 2020-08-15]
```
The last 8 hexadecimal digits are the identifier of the `gpg` key. Then you export it to a key server, and you can share the public key to sign or encrypt emails.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)