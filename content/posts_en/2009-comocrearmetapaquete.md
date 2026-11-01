Title: How to create a metapackage
Date: 2009-03-29 11:00
Category: Linux
Tags: Debian,paquetes
lang: en
translation: true

Metapackages make it easier to select programs. For
example, Debian has a list of educational programs, and to install
all of them by selecting a single program you use the debianedu package, which is a
metapackage that has all the educational packages as dependencies.

That is how Ubuntu works with Kubuntu, Xubuntu and its other flavors:
simply a metapackage that handles each version of Ubuntu.

The program in Debian for creating metapackages is called equivs.

To install it, run aptitude install equivs.

This package provides two programs:

* equivs-control: Creates a file like the control file of Debian packages,
where the maintainer information, the package version, the dependencies and
other things are handled.
* equivs-build: Builds the metapackage from the file created by equivs-control.

To create the template, run the command with the package name: equivs-control accesibilidad.
This creates the following template:

```
### Commented entries have reasonable defaults.
### Uncomment to edit them.
Section: misc
Priority: optional
Standards-Version: 3.6.2

Package:
# Version:
# Maintainer: Your Name
# Pre-Depends:
# Depends:
# Recommends:
# Suggests:
# Provides:
# Replaces:
# Architecture: all
# Copyright:
# Changelog:
# Readme:
# Extra-Files:
Description:
long description and info
.
second paragraph
```

This file handles the package section, the priority, the Debian policy version
(currently 3.8.0), the package name, the version, the maintainer name, the
dependencies (pre-depends, depends, recommends, provides and replaces), copyright, changelog,
readme, extra files and, finally, the package description split into 2 parts:
a short description and a long one.

Next I show the file for accessibility, which will handle the dependencies
of the following packages:

* brltty: Braille
* brltty-x11: Braille
* libcolorblind-dev: Color blindness
* libcolorblind0: Color blindness
* gnome-orca: Orca screen reader

```
Section: misc
Priority: optional
Standards-Version: 3.8.0

Package: accesibilidad
Version: 1.0
Maintainer: Ernesto Nadir Crespo Avila
Depends: brltty, brltty-x11, libcolorblind-dev, libcolorblind0, gnome-orca
Architecture: all
Description: Metapaquete para la instalacion de aplicaciones de accesibilidad
Metapaquete para la instalacion de aplicaciones de accesibilidad para personas invidentes
```

To build the package, run the command equivs-build accesibilidad:

```
ecrespo@canaima:~/canaima2/accesibilidad$ equivs-build accesibilidad
dh_testdir
dh_testroot
dh_clean -k
dh_testdir
dh_testroot
dh_install
dh_installdocs
dh_installchangelogs
dh_compress
dh_fixperms
dh_installdeb
dh_gencontrol
dh_md5sums
dh_builddeb
dpkg-deb: construyendo el paquete `accesibilidad' en `../accesibilidad_1.0_all.deb'.

The package has been created.
Attention, the package has been created in the current directory,
not in ".." as indicated by the message above!
```

Then running ls shows the package accesibilidad_1.0_all.deb.

This package cannot be installed with dpkg because it will fail: dpkg does not
handle dependencies. It is more useful to use apt-get or aptitude, but
to do that the package has to be uploaded to a local repository so that it
can be installed with apt-get or aptitude (how to create a local repository in
the next post).

===

Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)