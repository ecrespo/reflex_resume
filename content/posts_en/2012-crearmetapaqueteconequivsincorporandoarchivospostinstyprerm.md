Title: Create a metapackage with equivs (including postinst and prerm files)
Date: 2012-01-23 09:00
Category: Linux,Empaquetado 
Tags: 
lang: en
translation: true

Continuing with the articles on metapackaging for Debian/Canaima, here is the last article on the `equivs` tool.

What was left to do was to create a configuration metapackage that copies desktop configuration files when it is installed and stores those settings in the `/etc/skel` directory for when a new user is created on the system.


The Ubuntu Forums tutorial explains how to create the [metapackage with postinst and prerm files](https://ubuntuforums.org/showthread.php?t=726317); the problem is that the example files are not found at the links it references.

The idea is to add the `radiotray` program applet to the gnome desktop for all users. Since the machine normally already has users, the `radiotray` configuration files have to be copied to each user's `home` directory; for users created after the metapackage is installed, the system will copy the configuration files found in the `/etc/skel/` directory.

The first thing to do is create the control file for `equivs` metapackaging with the `equivs-control` command:  

```
$equivs-control canaima-radiotray-conf
```

This file will contain:

```
Section: misc
Priority: optional
Homepage: http://canaima.softwarelibre.gob.ve
Standards-Version: 3.9.1
	
Package: canaima-radiotray-conf
Version: 0.1
Maintainer: Ernesto Nadir Crespo Avila <ecrespo@cenditel.gob.ve>
Pre-Depends: radiotray
Depends: ${misc:Depends}
Architecture: all
Copyright: copyright
Changelog: changelog
Files: ./radiotray/radiotray.desktop /etc/skel/.config/autostart/radiotray.desktop
       ./radiotray/bookmarks.xml   /etc/skel/.local/share/radiotray/bookmarks.xml
File: postinst
 #!/bin/sh -e
 # preinst for main-package-config. Divert some configuration file of main-package.
 .
 set -e
 .
 PKG=canaima-radiotray-conf
 .
     if [ "$1" = configure ] ; then
 .
    for usuario in  /home/*? ; do
 .
        usuario_min=$(basename $usuario)
 .
        case $(grep "${usuario_min}:.*:.*:.*:.*:.*:::" /etc/shadow ) in
 .
                '')
                #no se hace nada
                ;;
 .
                *)
                usuario=${usuario_min}
 .
                if [ -f  /home/${usuario}/.config/autostart/radiotray.desktop ];
 .
                then
 .
                        cp -r /etc/skel/.config/autostart/radiotray.desktop /home/${usuario}/.config/autostart/radiotray.desktop
 .
                        chown ${usuario}.${usuario} /home/${usuario}/.config/autostart/radiotray.desktop

                else
 .
                        mkdir -p  /home/${usuario}/.config; chown -R ${usuario}.${usuario} /home/${usuario}/.config
 .
                        mkdir -p /home/${usuario}/.config/autostart; chown -R ${usuario}.${usuario} /home/${usuario}/.config/autostart
 .
                        cp -r /etc/skel/.config/autostart/radiotray.desktop /home/${usuario}/.config/autostart/radiotray.desktop
 .
                        chown ${usuario}.${usuario} /home/${usuario}/.config/autostart/radiotray.desktop
 .
                fi
 .
                if [ -f /home/${usuario}/.local/share/radiotray/bookmarks.xml ];
 .
                then
 .
                        cp -r /etc/skel/.local/share/radiotray/bookmarks.xml /home/${usuario}/.local/share/radiotray/bookmarks.xml
 .
                        chown ${usuario}.${usuario} /home/${usuario}/.local/share/radiotray/bookmarks.xml
 .
                else
 .
                        mkdir -p /home/${usuario}/.local; chown -R ${usuario}.${usuario} /home/${usuario}/.local
 .
                        mkdir -p /home/${usuario}/.local/share; chown -R ${usuario}.${usuario} /home/${usuario}/.local/share
 .
                        mkdir -p /home/${usuario}/.local/share/radiotray; chown -R ${usuario}.${usuario} /home/${usuario}/.local/share/radiotray
 .
                        cp -r /etc/skel/.local/share/radiotray/bookmarks.xml /home/${usuario}/.local/share/radiotray/bookmarks.xml
 .
                        chown ${usuario}.${usuario} /home/${usuario}/.local/share/radiotray/bookmarks.xml
 .
                fi
 .
        esac
 .
    done
 .
     fi
 .
    exit 0
File: prerm
 #!/bin/sh -e
 .
 set -e
 .
 PKG=canaima-radiotray-conf
 .
    if [ "$1" = configure ] ; then
 .
        for usuario in  /home/*? ; do
 .
            usuario_min=$(basename $usuario)
 .
             case $(grep "${usuario_min}:.*:.*:.*:.*:.*:::" /etc/shadow ) in
 .
                '')
                    #no se hace nada
                    ;;
 .
                    *)
                    usuario=${usuario_min}
 .
                    if [ -f  /home/${usuario}/.config/autostart/radiotray.desktop ];
 .
                        then
 .
                            rm -f /home/${usuario}/.config/autostart/radiotray.desktop
 .
                    fi
 .
                    if [ -f /home/${usuario}/.local/share/radiotray/bookmarks.xml ];
 .
                        then
 .
                            rm -f /home/${usuario}/.local/share/radiotray/bookmarks.xml
 .
                fi
 .
            esac
 .
        done
 .
    fi
 .
     exit 0
Description: Radiotray bookmarks to Venezuelan radio streaming
Radiotray config to autostart in gnome and radio stream bookmark
```	

The section and priority of the program are defined, along with the program's site and the `policy` version to use; the program name, its version, the program maintainer, and the pre-dependency, which in this case is the `radiotray` program.

The dependency is `${misc:Depends}`; this variable is defined because `debhelper` is used for packaging. The architecture is all, and the `copyright` and `changelog` files are defined.

Then the `Files` option defines the files that will be copied to the `/etc/skel/` directory.

The `File` option defines each script to add to the package, in this case the `postinst` and `prerm` files.

What `postinst` does is find the user accounts on the machine and copy the configuration files into the directories gnome uses to manage settings. In the case of `prerm`, it deletes those files for each user on the machine.

Finally, a short and then a long description of the program are given.

The `changelog` file will hold the changes made to the metapackage:
```
canaima-radiotray-conf (1:0.1) unstable; urgency=low
	
* First release.
	
-- Ernesto Nadir Crespo Avila <ecrespo@cenditel.gob.ve>  Fri, 23 Dec 2011 10:57:05 -0430

```

The `copyright` file will contain the following:
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
	Public License can be found in `/usr/share/common-licenses/GPL-2'.
```

Create the `radiotray` directory that will hold the configuration files:  

```
$mkdir radiotray
```

Create the `bookmarks.xml` and `radiotray.desktop` files. The first defines the Internet radio stations you want in your favorites and the second defines that the `radiotray` program is placed as an applet on the Gnome desktop.

The `bookmarks.xml` file. The contents of this file are shown in the following figure:

![Alternative text](./images/crearmetapaqueteconequivsincorporandoarchivospostinstyprerm-1.png)

	
The `radiotray.desktop` file:  

```
[Desktop Entry]
Type=Application
Exec=radiotray
Hidden=false
X-GNOME-Autostart-enabled=true
Name[es_VE]=radiotray
Name=radiotray
Comment[es_VE]=Cliente de radio por internet
Comment=Cliente de radio por internet
```

`Equivs` takes the file definition (File) and creates the files for the installation process. The following figure shows the file structure of the DEBIAN directory inside the deb package:

![Alternative text](./images/crearmetapaqueteconequivsincorporandoarchivospostinstyprerm-2.png)


After uploading the metapackage to a repository and installing it, the following figure shows the radio stations that appear in the favorites of `radiotray`:

![Alternative text](./images/crearmetapaqueteconequivsincorporandoarchivospostinstyprerm-3.png)


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)