Title: How to create a metapackage (metapackage with configuration files)
Date: 2011-09-23 09:00
Category: Linux,Empaquetado
Tags: Accesibilidad,Debian,Empaquetado,General,Linux,tiflotecnologia,Ubuntu
lang: en
translation: true

Continuing with the packaging articles, this time I will explain how to add configuration files to the metapackage.

The idea is to add the orca configuration files that are stored in `.orca` in the users' home. To do this, the `.orca` directory will be copied, along with the files it contains, to `/etc/skell/` 

Run the `equivs-control` command:

```
equivs-control canaima-accesibilidad-escritorio
```

The file will contain the following:

```
Section: misc
Priority: optional
Homepage: http://canaima.softwarelibre.gob.ve
Standards-Version: 3.9.1

Package: canaima-accesibilidad-visual-escritorio
Version: 1:0.1
Maintainer: Ernesto Nadir Crespo Avila <ecrespo@centitel.gob.ve>
Depends: at-spi, brltty, brltty-flite, brltty-speechd, brltty-x11, listen, espeak, festival, festvox-sflpc16k, festvox-palpc16k,  
gnome-orca, gnome-accessibility-themes, gnome-accessibility, libcolorblind0, gnome-mag, libgail-common, mousetweaks, dots,  
${misc:Depends}
Architecture: any
Copyright: copyright
Changelog: changelog
Files: ./conf/.orca/user-settings.py /etc/skell/.orca/user-settings.py
	   ./conf/.orca/app-settings/__init__.py /etc/skell/.orca/app-settings/__init__.py
	   ./conf/.orca/orca-scripts/__init__.py /etc/skell/.orca/orca-scripts/__init__.py
	   ./conf/.orca/user-settings.pyc /etc/skell/.orca/user-settings.pyc
	   ./conf/.orca/app-settings/__init__.pyc /etc/skell/.orca/app-settings/__init__.pyc
	   ./conf/.orca/orca-scripts/__init__.pyc /etc/skell/.orca/orca-scripts/__init__.pyc
Description: Programas de Accesibilidad para Canaima GNU/Linux
Este metapaquete provee los programas de accesibilidad y configuraciones para que las personas con discapacidad puedan utilizar  
canaima GNU/Linux.
```

Now there is the `Files` parameter, where the first path is the source where the file is located and the second is the path it will be copied to. Each pair is separated by a new line.


The `changelog` file contains the following:

```
canaima-accesibilidad-visual-escritorio (1.0:0.1) unstable; urgency=low


* First release.

-- Ernesto Nadir Crespo Avila  <ecrespo@cenditel.gob.ve>  Thu, 22 Sep 2011 22:33:15 -0430
```


The copyright file contains:

```
Authors:


Copyright (C) 2011 Ernesto Nadir Crespo Avila <ecrespo@cenditel.gob.ve>


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
Public License can be found in `usr/share/common-licenses/GPL-2'
```

Now all that is left is to run the `equivs-build` command:  

```
equivs-build -f canaima-accesibilidad-visual-escritorio
```


Running `ls -l` shows the files created and the `.deb`:
```
total 40
-rw-r--r-- 1 ernesto ernesto 1275 sep 23 08:40 canaima-accesibilidad-visual-escritorio
-rw-r--r-- 1 ernesto ernesto 1824 sep 23 08:41 canaima-accesibilidad-visual-escritorio_0.1_amd64.changes
-rw-r--r-- 1 ernesto ernesto 6836 sep 23 08:41 canaima-accesibilidad-visual-escritorio_0.1_amd64.deb
-rw-r--r-- 1 ernesto ernesto  909 sep 23 08:41 canaima-accesibilidad-visual-escritorio_0.1.dsc
-rw-r--r-- 1 ernesto ernesto 6378 sep 23 08:41 canaima-accesibilidad-visual-escritorio_0.1.tar.gz
-rw-r--r-- 1 ernesto ernesto  184 sep 23 08:41 changelog
drwxr-xr-x 3 ernesto ernesto 4096 sep 23 08:15 conf
 -rw-r--r-- 1 ernesto ernesto  896 sep 23 08:41 copyright
```
Running `dpkg -c` on the `.deb` file shows what the metapackage will install:

```
dpkg -c canaima-accesibilidad-visual-escritorio_0.1_amd64.deb
drwxr-xr-x root/root 0 2011-09-23 08:41 ./
drwxr-xr-x root/root 0 2011-09-23 08:41 ./usr/
drwxr-xr-x root/root 0 2011-09-23 08:41 ./usr/share/
drwxr-xr-x root/root 0 2011-09-23 08:41 ./usr/share/doc/
drwxr-xr-x root/root 0 2011-09-23 08:41 ./usr/share/doc/canaima-accesibilidad-visual-escritorio/
-rw-r--r-- root/root  1044 2011-09-23 08:41 ./usr/share/doc/canaima-accesibilidad-visual-escritorio/README.Debian
-rw-r--r-- root/root   171 2011-09-23 08:41 ./usr/share/doc/canaima-accesibilidad-visual-escritorio/changelog.gz
-rw-r--r-- root/root   896 2011-09-23 08:41 ./usr/share/doc/canaima-accesibilidad-visual-escritorio/copyright
drwxr-xr-x root/root 0 2011-09-23 08:41 ./etc/
drwxr-xr-x root/root 0 2011-09-23 08:41 ./etc/skell/
drwxr-xr-x root/root 0 2011-09-23 08:41 ./etc/skell/.orca/
drwxr-xr-x root/root 0 2011-09-23 08:41 ./etc/skell/.orca/app-settings/
-rwxr-xr-x root/root 0 2011-09-23 08:41 ./etc/skell/.orca/app-settings/__init__.py
-rw-r--r-- root/root   111 2011-09-23 08:41 ./etc/skell/.orca/app-settings/__init__.pyc
-rw-r--r-- root/root  7291 2011-09-23 08:41 ./etc/skell/.orca/user-settings.py
-rw-r--r-- root/root  6193 2011-09-23 08:41 ./etc/skell/.orca/user-settings.pyc
drwxr-xr-x root/root 0 2011-09-23 08:41 ./etc/skell/.orca/orca-scripts/
-rwxr-xr-x root/root 0 2011-09-23 08:41 ./etc/skell/.orca/orca-scripts/__init__.py
-rw-r--r-- root/root   111 2011-09-23 08:41 ./etc/skell/.orca/orca-scripts/__init__.pyc
```

Note that the `.orca` directory is created inside `/etc/skell`

Run `lintian` to check that the metapackage has no errors or warnings:  

```
lintian -i canaima-accesibilidad-visual-escritorio_0.1.dsc
```

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)

