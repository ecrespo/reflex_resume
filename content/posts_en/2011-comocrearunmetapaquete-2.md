Title: How to create a metapackage (version 2)
Date: 2011-09-21 09:00
Category: Linux,Empaquetado
Tags: Canaima,Debian,Empaquetado,General,Linux,Ubuntu
lang: en
translation: true

This article is an update of the article about **how to create a metapackage**, which you can read [here](/blog/comocrearmetapaquete).

This article adds the `changelog` and `copyright` files for the `canaima-caribay-radio` metapackage.

Create a working directory:  

```
mkdir canaima-caribay-radio
```

Now create the `control` file with the `equivs-control` command:

```
equivs-control canaima-caribay-radio
```

Now the file will be modified so that it has the dependencies for `jackd2, icecast2, audacity, easytag` and `idjc`. The package maintainer, its `homepage`, and a short and long description of the metapackage are added.

The modified file:

```
Section: misc
Priority: optional
Homepage: http://canaima.softwarelibre.gob.ve
Standards-Version: 3.6.2


Package: canaima-caribay-radio
Version: 1.0
Maintainer: Ernesto Nadir Crespo Avila <ecrespo@cenditel.gob.ve>
Depends: jackd2, libjack-jackd2-0, libjack-jackd2-dev, pulseaudio-module-jack, qjackctl, libjack-jackd2-0,  
libjack-jackd2-dev, vorbis-tools, libvorbis-dev, libogg-dev, libmad0-dev, libsamplerate0-dev, libflac-dev,   
libsndfile1-dev, libavcodec-dev, libavformat-dev, libspeex-dev, python-gtk2-dev, python-mutagen, libdbus-1-dev, ffmpeg,  
libshout3-dev, libtwolame-dev, twolame, idjc, audacity, audacity-data, audacity-dbg, icecast2, easytag
Architecture: all
Copyright: copyright
Changelog: changelog 
Description: Metapaquete para la instalacion de radio streaming
Metapaquete para la instalacion de radio streaming con icecast2 e idjc.
```

Compared with the previous article, the `Copyright` and `Changelog` fields were added.

These files contain the following:

Copyright:

```
Authors:

Copyright (C) 2011 Ernesto Nadir Crespo Avila <ecrespo@cenditel.gob.ve>
Copyright (C) 2011 David Hernández <david.vzla@gmail.com>


License:


This package is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 dated June, 1991.


This package is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.


You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA


On Debian GNU/Linux systems, the complete text of the GNU General
Public License can be found in `/usr/share/common-licenses/GPL-2'.

```

Changelog:

```
canaima-caribay-radio (1:1.0) unstable; urgency=low


* First release.


-- Ernesto Nadir Crespo Avila <ecrespo@cenditel.gob.ve>  Tue, 20 Sep 2011 16:12:45 -0430
```

Now, to create and sign the metapackage, use the `equivs-build` command with the `-f` option, which runs a full `debuild` and signs the metapackage.

It is important to note that the `gpg` key must contain the maintainer name that appears in the control and changelog files in order to sign the metapackage.

The gpg key is shown below:
`gpg --list-keys | less`

```
--------------------------------
pub   1024D/C97E7015 2005-08-15
uid  Ernesto Nadir Crespo Avila (seraph1) <ecrespo@debian.org.ve>
uid  Ernesto Nadir Crespo Avila (seraph1) <ecrespo@debianvenezuela.org>
uid  Ernesto Nadir Crespo Avila (seraph1) <ecrespo@uc.edu.ve>
uid  Ernesto Nadir Crespo Avila (seraph1) <ecrespo@cantv.net>
uid  Ernesto Nadir Crespo Avila (seraph1) <ecrespo@gmail.com>
uid  Ernesto Crespo (seraph1) <ecrespoa@yahoo.es>
uid  Ernesto Nadir Crespo Avila (seraph) <ernesto@crespo.info.ve>
uid  [jpeg image of size 11184]
uid  Ernesto Nadir Crespo Avila <ecrespo@cenditel.gob.ve>
uid  Ernesto Nadir Crespo Avila <ernesto@crespo.org.ve>
```

Now the metapackage (`metapaquete`) will be created: the procedure will ask twice for the `gpg` key passphrase.

```
equivs-build -f canaima-caribay-radio
```

```
dpkg-buildpackage: exportar «CFLAGS» de dpkg-buildflags (origen: «vendor»): «-g -O2»
dpkg-buildpackage: exportar «CPPFLAGS» de dpkg-buildflags (origen: «vendor»): «»
dpkg-buildpackage: exportar «CXXFLAGS» de dpkg-buildflags (origen: «vendor»): «-g -O2»
dpkg-buildpackage: exportar «FFLAGS» de dpkg-buildflags (origen: «vendor»): «-g -O2»
dpkg-buildpackage: exportar «LDFLAGS» de dpkg-buildflags (origen: «vendor»): «»
dpkg-buildpackage: paquete fuente canaima-caribay-radio
dpkg-buildpackage: versión de las fuentes 1:1.0
dpkg-buildpackage: fuentes modificadas por Ernesto Nadir Crespo Avila <ecrespo@cenditel.gob.ve>
dpkg-buildpackage: arquitectura del sistema amd64
dpkg-source --before-build equivs.nAXaSZ
fakeroot debian/rules clean
dh_testdir
dh_testroot
dh_clean
dh_clean: Compatibility levels before 5 are deprecated.
dpkg-source -b equivs.nAXaSZ
dpkg-source: aviso: no se ha definido un formato de fuentes en «debian/source/format», consulte dpkg-source(1)
dpkg-source: información: usando el formato de fuente «1.0»
dpkg-source: aviso: el directorio de fuentes «equivs.nAXaSZ» no es <paquete-fuente>-<versión-desarrollador-original> «canaima-caribay-radio-1.0»
dpkg-source: información: construyendo canaima-caribay-radio en canaima-caribay-radio_1.0.tar.gz
dpkg-source: información: construyendo canaima-caribay-radio en canaima-caribay-radio_1.0.dsc
debian/rules build
make: No se hace nada para `build'.
fakeroot debian/rules binary
dh_testdir
dh_testroot
dh_clean -k
dh_clean: dh_clean -k is deprecated; use dh_prep instead
dh_clean: Compatibility levels before 5 are deprecated.
dh_testdir
dh_testroot
dh_install
dh_install: Compatibility levels before 5 are deprecated.
dh_installdocs
dh_installdocs: Compatibility levels before 5 are deprecated.
dh_installchangelogs
dh_installchangelogs: Compatibility levels before 5 are deprecated.
dh_compress
dh_compress: Compatibility levels before 5 are deprecated.
dh_fixperms
dh_fixperms: Compatibility levels before 5 are deprecated.
dh_installdeb
dh_installdeb: Compatibility levels before 5 are deprecated.
dh_gencontrol
dh_gencontrol: Compatibility levels before 5 are deprecated.
dh_md5sums
dh_md5sums: Compatibility levels before 5 are deprecated.
dh_builddeb
dh_builddeb: Compatibility levels before 5 are deprecated.
dpkg-deb: construyendo el paquete `canaima-caribay-radio' en `../canaima-caribay-radio_1.0_all.deb'.
signfile canaima-caribay-radio_1.0.dsc

Necesita una frase contraseña para desbloquear la clave secreta
del usuario: "Ernesto Nadir Crespo Avila (seraph1) <ecrespo@debian.org.ve>"
clave DSA de 1024 bits, ID C97E7015, creada el 2005-08-15

  
dpkg-genchanges  >../canaima-caribay-radio_1.0_amd64.changes
dpkg-genchanges: incluyendo el código fuente completo en la subida
signfile canaima-caribay-radio_1.0_amd64.changes

Necesita una frase contraseña para desbloquear la clave secreta
del usuario: "Ernesto Nadir Crespo Avila (seraph1) <ecrespo@debian.org.ve>"
clave DSA de 1024 bits, ID C97E7015, creada el 2005-08-15

  
dpkg-source --after-build equivs.nAXaSZ
dpkg-buildpackage: subida completa; paquete nativo de Debian (se incluye la fuente completa)

The package has been created.
Attention, the package has been created in the current directory,
not in ".." as indicated by the message above!
```

Now run `ls -l` and you get the following:
```
ernesto@zeath:~/canaima/canaima-caribay-radio$ ls -l
total 28
-rw-r--r-- 1 ernesto ernesto  849 sep 20 17:03 canaima-caribay-radio
-rw-r--r-- 1 ernesto ernesto 2528 sep 21 08:48 canaima-caribay-radio_1.0_all.deb
-rw-r--r-- 1 ernesto ernesto 1583 sep 21 08:49 canaima-caribay-radio_1.0_amd64.changes
-rw-r--r-- 1 ernesto ernesto  819 sep 21 08:49 canaima-caribay-radio_1.0.dsc
-rw-r--r-- 1 ernesto ernesto 2170 sep 21 08:48 canaima-caribay-radio_1.0.tar.gz
-rw-r--r-- 1 ernesto ernesto  164 sep 20 17:03 changelog
-rw-r--r-- 1 ernesto ernesto  957 sep 20 17:03 copyright
```

The file `canaima-caribay-radio_1.0_amd64.changes` contains the following:  

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

Format: 1.8
Date: Tue, 20 Sep 2011 16:12:45 -0430
Source: canaima-caribay-radio
Binary: canaima-caribay-radio
Architecture: source all
Version: 1:1.0
Distribution: unstable
Urgency: low
Maintainer: Ernesto Nadir Crespo Avila <ecrespo@cenditel.gob.ve>
Changed-By: Ernesto Nadir Crespo Avila <ecrespo@cenditel.gob.ve>
Description: 
 canaima-caribay-radio - Metapaquete para la instalacion de radio streaming
Changes: 
 canaima-caribay-radio (1:1.0) unstable; urgency=low
 .
   * First release.
Checksums-Sha1: 
 2234f6f5d8808e0ae425eb3164632b01bc94251a 819 canaima-caribay-radio_1.0.dsc
 8851015c0174d5126127328776e35174e361cc21 2170 canaima-caribay-radio_1.0.tar.gz
 104312d9eb56eb623ad1f901a2801e096f4021be 2528 canaima-caribay-radio_1.0_all.deb
Checksums-Sha256: 
 3be03f102f6ef9dab2525ac384a265e9761ca2f5f4fb7d48fdbd0b38fee4e22f 819 canaima-caribay-radio_1.0.dsc
 75cb5c5b95d14d995776a035925c2cfe5ee77873d091ef9e238b000fb4b1375b 2170 canaima-caribay-radio_1.0.tar.gz
 74540c21659c774a12d5162886f59b974b155c47d5471fac40ff7fece11cd282 2528 canaima-caribay-radio_1.0_all.deb
Files: 
 3f563e110433652011cf0d32fe96a0f6 819 misc optional canaima-caribay-radio_1.0.dsc
 e53b6a60fd0961a6b161a61b5a107e77 2170 misc optional canaima-caribay-radio_1.0.tar.gz
 4ac58a93d2e4160f378093909d687967 2528 misc optional canaima-caribay-radio_1.0_all.deb

 -----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.10 (GNU/Linux)

iEYEARECAAYFAk555EYACgkQh+iQYcl+cBW/kQCeOZzpeHCAYomqczO7kkR6+nvT
fWIAniK+uWLpndvqEJmz2IUA7JNe8Nng
=qVVe
 -----END PGP SIGNATURE-----
```

The file `canaima-caribay-radio_1.0.dsc` contains the following:

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

Format: 1.0
Source: canaima-caribay-radio
Binary: canaima-caribay-radio
Architecture: all
Version: 1:1.0
Maintainer: Ernesto Nadir Crespo Avila <ecrespo@cenditel.gob.ve>
Homepage: http://canaima.softwarelibre.gob.ve
Standards-Version: 3.6.2
Build-Depends: debhelper (>= 4)
Checksums-Sha1: 
 8851015c0174d5126127328776e35174e361cc21 2170 canaima-caribay-radio_1.0.tar.gz
Checksums-Sha256: 
 75cb5c5b95d14d995776a035925c2cfe5ee77873d091ef9e238b000fb4b1375b 2170 canaima-caribay-radio_1.0.tar.gz
Files: 
 e53b6a60fd0961a6b161a61b5a107e77 2170 canaima-caribay-radio_1.0.tar.gz

 -----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.10 (GNU/Linux)

iEYEARECAAYFAk555EIACgkQh+iQYcl+cBVLqgCdGA+DXaVjyDrcGNfxcITL9sCP
oY0An1hC/e7UIQiiTZ4DQUysYHs8sTS9
=6NcI
-----END PGP SIGNATURE-----
```

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)